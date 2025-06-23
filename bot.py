#bot.py
import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import time
from binance.client import Client
from dotenv import load_dotenv
import csv

load_dotenv()

# Setup logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

# Binance API Setup
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
logging.info("Binance Futures client initialized.")

# DB setup
DB_FILE = 'trading_bot.db'

# CSV Order History Setup
CSV_ORDER_FILE = 'order_history.csv'
CSV_HEADERS = [
    'timestamp', 'order_id', 'symbol', 'side', 'type', 'quantity', 'price',
    'stop_price', 'status', 'time_in_force', 'commission', 'commission_asset',
    'executed_qty', 'fills'
]

def init_csv():
    if not os.path.exists(CSV_ORDER_FILE):
        with open(CSV_ORDER_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
        logging.info(f"Created new order history CSV: {CSV_ORDER_FILE}")

def save_order_to_csv(order_data):
    try:
        csv_row = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'order_id': order_data.get('orderId', ''),
            'symbol': order_data.get('symbol', ''),
            'side': order_data.get('side', ''),
            'type': order_data.get('type', ''),
            'quantity': order_data.get('origQty', ''),
            'price': order_data.get('price', ''),
            'stop_price': order_data.get('stopPrice', ''),
            'status': order_data.get('status', ''),
            'time_in_force': order_data.get('timeInForce', ''),
            'commission': '',
            'commission_asset': '',
            'executed_qty': order_data.get('executedQty', ''),
            'fills': json.dumps(order_data.get('fills', [])) if order_data.get('fills') else ''
        }
        if order_data.get('fills'):
            fills = order_data['fills']
            if fills and len(fills) > 0:
                csv_row['commission'] = fills[0].get('commission', '')
                csv_row['commission_asset'] = fills[0].get('commissionAsset', '')

        with open(CSV_ORDER_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writerow(csv_row)

        logging.info(f"Order response: {json.dumps(order_data)}")

    except Exception as e:
        logging.error(f"Error saving order to CSV: {e}")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            order_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL,
            stop_price REAL,
            status TEXT DEFAULT 'filled'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            open_price REAL NOT NULL,
            high_price REAL NOT NULL,
            low_price REAL NOT NULL,
            close_price REAL NOT NULL,
            volume REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
init_csv()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    symbol = data.get("symbol")
    side = data.get("side")
    order_type = data.get("order_type")
    quantity = data.get("quantity")
    price = data.get("price")
    stop_price = data.get("stop_price")

    try:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        logging.info(f"Placing order: {side} {quantity} {symbol} at {order_type} price={price}")

        order = client.futures_create_order(**params)

        save_order_to_csv(order)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (timestamp, symbol, side, order_type, quantity, price, stop_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), symbol, side, order_type, quantity, price, stop_price))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "order": order})

    except Exception as e:
        logging.error(f"API Error: {e}")
        error_order = {
            'orderId': 'ERROR_' + str(int(time.time())),
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'origQty': quantity,
            'price': price,
            'stopPrice': stop_price,
            'status': 'ERROR',
            'error': str(e)
        }
        save_order_to_csv(error_order)
        return jsonify({"status": "error", "message": str(e)})

@app.route("/order_history")
def order_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, symbol, side, order_type, quantity, price, stop_price FROM orders ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/csv_order_history")
def csv_order_history():
    """New endpoint to get order history from CSV"""
    try:
        orders = []
        if os.path.exists(CSV_ORDER_FILE):
            with open(CSV_ORDER_FILE, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert fills back from JSON string if needed
                    if row['fills']:
                        try:
                            row['fills'] = json.loads(row['fills'])
                        except json.JSONDecodeError:
                            pass
                    orders.append(row)
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/csv_stats")
def csv_stats():
    """Get statistics from CSV order history"""
    try:
        orders = []
        if os.path.exists(CSV_ORDER_FILE):
            with open(CSV_ORDER_FILE, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                orders = list(reader)
        
        if not orders:
            return jsonify({"total_orders": 0})
        
        stats = {
            "total_orders": len(orders),
            "symbols": list(set(order['symbol'] for order in orders if order['symbol'])),
            "order_types": list(set(order['type'] for order in orders if order['type'])),
            "statuses": list(set(order['status'] for order in orders if order['status'])),
            "sides": list(set(order['side'] for order in orders if order['side'])),
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/price_data")
def price_data():
    try:
        klines = client.futures_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
        data = [{
            "time": int(k[0]),
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5])
        } for k in klines]

        # Add indicators (SMA, EMA, RSI)
        closes = [d['close'] for d in data]
        data = add_indicators(data, closes)
        return jsonify(data)

    except Exception as e:
        print("Binance error, falling back to mock data:", e)
        return jsonify(get_mock_price_data("BTCUSDT", 100))

def add_indicators(data, closes):
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(data)
    df['SMA20'] = df['close'].rolling(window=20).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()

    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df.fillna(0).to_dict(orient='records')

def get_mock_price_data(symbol="BTCUSDT", limit=100):
    import random
    data = []
    base_price = 101709.60
    now = int(time.time() * 1000)
    for i in range(limit):
        timestamp = now - ((limit - i) * 60000)
        pct_change = (random.random() - 0.5) * 0.02
        new_price = base_price * (1 + pct_change)
        open_price = base_price
        close_price = new_price
        high_price = max(open_price, close_price) * (1 + random.random() * 0.01)
        low_price = min(open_price, close_price) * (1 - random.random() * 0.01)
        volume = random.uniform(500, 2000)
        data.append({
            "time": timestamp,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": round(volume, 2)
        })
        base_price = new_price
    return data

if __name__ == '__main__':
    app.run(debug=True)