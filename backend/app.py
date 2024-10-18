from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    # Sample stock data using an external API
    api_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=YOUR_API_KEY"
    response = requests.get(api_url)
    data = response.json()

    return jsonify({
        'symbol': data.get('Symbol'),
        'name': data.get('Name'),
        'pe_ratio': data.get('PERatio'),
        'pb_ratio': data.get('PriceToBookRatio')
    })

if __name__ == '__main__':
    app.run(debug=True)
