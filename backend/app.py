from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from config import Config
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS to allow requests from the frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

mysql = MySQL(app)
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    password = data.get('Password')

    print(f"Attempting login for Email: {email}")

    cur = mysql.connection.cursor()
    cur.execute("SELECT Email, Password FROM login WHERE Email=%s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        print(f"User found: {user[0]}")
        # Directly compare the provided password with the stored one
        if user[1] == password:
            print("Password match successful")
            session['email'] = user[0]
            return jsonify(message="Login successful", email=user[0]), 200
        else:
            print("Password mismatch")
            return jsonify(message="Invalid username or password"), 401
    else:
        print("User not found")
        return jsonify(message="Invalid username or password"), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    Email = data.get('Email')
    Password = data.get('Password')

    # Store the password as plain text
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO login (Email, Password) VALUES (%s, %s)", (Email, Password))
    mysql.connection.commit()
    cur.close()

    return jsonify(message="User registered successfully!"), 201


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('Email', None)  # Match 'Email' used during login
    return jsonify(message="Logged out successfully"), 200

if __name__ == '__main__':
    app.run(debug=True)
