import eventlet
eventlet.monkey_patch()
from flask import Flask, request, jsonify, session, send_from_directory
from flask_mysqldb import MySQL
from config import Config
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
from datetime import datetime
import logging
import time
import threading
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Setup MySQL
mysql = MySQL(app)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    password = data.get('Password')

    logging.info(f"Attempting login for Email: {email}")

    cur = mysql.connection.cursor()
    cur.execute("SELECT Email, Password FROM login WHERE Email=%s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        logging.info(f"User found: {user[0]}")
        if user[1] == password:
            logging.info("Password match successful")
            session['email'] = user[0]
            return jsonify(message="Login successful", email=user[0]), 200
        else:
            logging.warning("Password mismatch")
            return jsonify(message="Invalid username or password"), 401
    else:
        logging.warning("User not found")
        return jsonify(message="Invalid username or password"), 401


# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    Email = data.get('Email')
    Password = data.get('Password')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO login (Email, Password) VALUES (%s, %s)", (Email, Password))
    mysql.connection.commit()
    cur.close()

    return jsonify(message="User registered successfully!"), 201


# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)  # Ensure key matches the one used in login
    return jsonify(message="Logged out successfully"), 200

# Initialize SocketIO
socketio = SocketIO(app, async_mode='eventlet', logger=True,
    engineio_logger=True,cors_allowed_origins="http://localhost:5173")

# Alpha Vantage (Finnhub) API configuration
ALPHA_VANTAGE_API_KEY = 'cs9bk0pr01qoa9gbnb4gcs9bk0pr01qoa9gbnb50'
ALPHA_VANTAGE_URL = 'https://finnhub.io/api/v1/quote'

# Store active stock symbols
active_symbols = set()

def fetch_stock_data(symbol):
    """Fetch real-time stock data from Finnhub API"""
    try:
        params = {
            'symbol': symbol,
            'token': ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(ALPHA_VANTAGE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'symbol': symbol,
                'current_price': data.get('c'),
                'change': data.get('d'),
                'percent_change': data.get('dp'),
                'high_price': data.get('h'),
                'low_price': data.get('l'),
                'open_price': data.get('o'),
                'prev_close': data.get('pc'),
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
    return None

def background_task():
    """Background task to emit stock updates"""
    while True:
        for symbol in active_symbols.copy():
            data = fetch_stock_data(symbol)
            if data:
                socketio.emit('stock_update', data)
        eventlet.sleep(5)  # Wait 5 seconds between updates

# Start background task
def start_background_task():
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')

@socketio.on('subscribe')
def handle_subscribe(data):
    symbol = data.get('symbol')
    if symbol:
        active_symbols.add(symbol.upper())
        logging.info(f'Subscribed to {symbol}')
        # Emit initial data
        initial_data = fetch_stock_data(symbol)
        if initial_data:
            emit('stock_update', initial_data)

@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    symbol = data.get('symbol')
    if symbol:
        active_symbols.discard(symbol.upper())
        logging.info(f'Unsubscribed from {symbol}')

@app.route('/api/stock-data', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol', 'AAPL')
    data = fetch_stock_data(symbol)
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch stock data"}), 500

if __name__ == '__main__':
    start_background_task()
    socketio.run(app, debug=True, port=5000)