# 🚀 Simplified Binance Futures Trading Bot

This is a simplified trading bot built using Python and the Binance Futures Testnet API.  
It supports both **MARKET** and **LIMIT** orders for `USDT-M Futures` trading pairs.

---

## ✅ Features

- ✅ Place **MARKET** and **LIMIT** orders (Buy/Sell)
- ✅ Secure API credential handling using `.env` and `python-dotenv`
- ✅ Logging of all API requests/responses to `trading_bot.log`
- ✅ CLI interface with `argparse`
- ✅ `.bat` files for quick auto-run (optional)
- ✅ Clean and reusable Python code with error handling

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 .env File Setup

Create a `.env` file in the project root:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

---

## 🧪 Example Usage (Command Line)

**Market BUY Order:**

```bash
python "Simplified Trading Bot.py" --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit SELL Order:**

```bash
python "Simplified Trading Bot.py" --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 61000
```

---

## 🚀 Auto-Run with `.bat` Files

Use `run_market_order.bat` or `run_limit_order.bat` for one-click execution.

---

## 📂 Files Included

- `Simplified Trading Bot.py` – Main trading bot script
- `run_market_order.bat` – Market order runner
- `run_limit_order.bat` – Limit order runner
- `requirements.txt` – Python dependencies
- `trading_bot.log` – Execution logs
- `.gitignore` – Prevents secrets/logs from being committed

---

## ⚠️ Warning

Never share your real API keys. Use **Binance Futures Testnet** for testing:
👉 https://testnet.binancefuture.com

---

## 👨‍💻 Author

**Alen Thomas**  
Junior Python Developer Candidate
