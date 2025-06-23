# 🪙 Trading Bot 

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Binance API](https://img.shields.io/badge/Binance-API-orange.svg)](https://binance-docs.github.io/apidocs/)

A Python-based trading bot for Binance Futures with a modern web interface that runs as a native desktop application using PyWebView. Built for both beginners and advanced traders with comprehensive order management and real-time market data.

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Security Best Practices](#-security-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Building Executable](#-building-standalone-executable)
- [Contributing](#-contributing)

---

## 🚀 Features

### Core Trading Features

- ✅ **Multiple Order Types** - Market, Limit, Stop-Market, and OCO orders
- ✅ **Real-time Market Data** - Live BTC/USDT and 50+ trading pairs via WebSocket
- ✅ **Advanced Charts** - Candlestick charts with 20+ technical indicators
- ✅ **Risk Management** - Stop-loss, take-profit, and position sizing tools
- ✅ **Order Management** - Complete order history with filtering and CSV export
- ✅ **Portfolio Tracking** - Real-time P&L, balance updates, and performance metrics

### Desktop Experience

- ✅ **Native Desktop App** - Runs like a real desktop application (no browser needed)
- ✅ **Modern Web UI** - Beautiful, responsive Flask-based interface
- ✅ **System Tray Integration** - Minimize to system tray with context menu
- ✅ **Desktop Notifications** - Trade confirmations and price alerts
- ✅ **Keyboard Shortcuts** - Quick order placement and navigation
- ✅ **Multi-monitor Support** - Remember window position and size

### Data & Analytics

- ✅ **Persistent Data Storage** - SQLite database for trades and settings
- ✅ **Export Capabilities** - CSV, JSON export for trading history
- ✅ **Performance Analytics** - Win rate, profit/loss analysis, drawdown metrics
- ✅ **Comprehensive Logging** - Debug logs with rotation and error tracking
- ✅ **Backup & Restore** - Settings and data backup functionality

---

## ⚡ Quick Start

Get up and running in under 5 minutes:

```bash
# 1. Clone or download the project
git clone https://github.com/yourusername/trading-bot-desktop.git
cd trading-bot-desktop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your API configuration
cp .env.example .env
# Edit .env with your Binance API credentials

# 4. Run the application
python app.py
```

---

## 🛠️ Installation

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB free space

### Method 1: Using pip (Recommended)

```bash
# Install core dependencies
pip install python-binance==1.0.19 python-dotenv==1.0.0 websocket-client==1.6.4 flask==2.3.3

# Install desktop app dependencies
pip install pywebview==4.4.1

# Install optional features
pip install pystray==0.19.4 plyer==2.1.0 matplotlib==3.8.0 pandas==2.1.1
```

### Method 2: Using requirements.txt

```bash
pip install -r requirements.txt
```

### Method 3: Development Installation

```bash
# For contributors and developers
pip install -r requirements-dev.txt
```

### Platform-Specific Dependencies

#### Windows

```bash
# Usually works out of the box
# For system tray: pip install pystray[win32]
```

#### macOS

```bash
# Install Homebrew dependencies
brew install python-tk

# For notifications
pip install plyer[macos]
```

#### Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# For notifications
sudo apt-get install libnotify-dev
```

---

## 🔐 Configuration

### 1. API Keys Setup

Create a `.env` file in the project root:

```env
# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true  # Set to false for live trading

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///trading_bot.db

# Desktop App Settings
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
ENABLE_SYSTEM_TRAY=true
ENABLE_NOTIFICATIONS=true

# Security Settings
SESSION_SECRET_KEY=your_random_secret_key_here
API_RATE_LIMIT=1200  # requests per minute
```

### 2. Binance API Setup

1. **Create Binance Account**: Sign up at [binance.com](https://binance.com)
2. **Enable 2FA**: Set up Two-Factor Authentication
3. **Create API Key**:
   - Go to Account → API Management
   - Create API Key with these permissions:
      - ✅ Enable Reading
      - ✅ Enable Futures
      - ✅ Enable Spot & Margin Trading (if needed)

   4. **Testnet Setup** (Recommended for beginners):

   - Visit [testnet.binancefuture.com](https://testnet.binancefuture.com)
   - Generate testnet API keys for safe testing

### 3. Icon Customization

Place your custom icons in the project folder:

- `icon.png` - System tray icon (64x64 px recommended)
- `icon.ico` - Windows executable icon
- `icon.icns` - macOS application icon

---

## 📖 Usage Guide

### Starting the Application

```bash
# Standard launch
python app.py

# With custom settings
python app.py --width 1400 --height 900 --debug

# Headless mode (web only)
python app.py --headless
```

### Basic Trading Workflow

1. **Connect to Binance**

   - Verify API connection (green indicator)
   - Check account balance and permissions

2. **Select Trading Pair**

   - Default: BTC/USDT
   - Search and select from 50+ available pairs

3. **Place Orders**

   - **Market Order**: Instant execution at current price
   - **Limit Order**: Set your desired price
   - **Stop Order**: Risk management tool

4. **Monitor Positions**

   - Real-time P&L updates
   - Position size and margin usage
   - Exit strategies and alerts

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + N` | New Market Order |
| `Ctrl + L` | New Limit Order |
| `Ctrl + S` | New Stop Order |
| `Ctrl + H` | Toggle Order History |
| `Ctrl + R` | Refresh Data |
| `F11` | Toggle Fullscreen |
| `Ctrl + Q` | Quick Exit |

### Advanced Features

#### Custom Trading Pairs

```python
# Add custom pairs in bot.py
CUSTOM_PAIRS = [
    'ETH/USDT', 'ADA/USDT', 'DOT/USDT'
]
```

#### Price Alerts

```python
# Set price alerts via API
POST /api/alerts
{
    "symbol": "BTCUSDT",
    "price": 45000,
    "condition": "above"
}
```

---

## 🔌 API Documentation

### REST API Endpoints

#### Trading Operations

```http
# Place Market Order
POST /api/orders/market
Content-Type: application/json

{
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.001
}
```

```http
# Place Limit Order
POST /api/orders/limit
Content-Type: application/json

{
    "symbol": "BTCUSDT",
    "side": "SELL",
    "quantity": 0.001,
    "price": 45000
}
```

```http
# Get Order History
GET /api/orders/history?symbol=BTCUSDT&limit=50
```

#### Account Information

```http
# Get Account Balance
GET /api/account/balance

# Get Open Positions
GET /api/account/positions

# Get Trading History
GET /api/account/trades?start_time=2024-01-01&end_time=2024-12-31
```

#### Market Data

```http
# Get Current Price
GET /api/market/price/{symbol}

# Get 24hr Statistics
GET /api/market/stats/{symbol}

# Get Order Book
GET /api/market/depth/{symbol}?limit=100
```

### WebSocket Streams

```javascript
// Price Updates
ws://localhost:5000/ws/price/{symbol}

// Order Updates
ws://localhost:5000/ws/orders

// Account Updates
ws://localhost:5000/ws/account
```

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 1001 | Invalid API Key | Check your .env file |
| 1002 | Insufficient Balance | Add funds or reduce quantity |
| 1003 | Invalid Symbol | Use correct trading pair format |
| 1004 | Rate Limit Exceeded | Wait and retry |
| 1005 | Order Size Too Small | Increase quantity |

---

## 🔒 Security Best Practices

### API Key Security

- ✅ **Never share** your API keys or `.env` file
- ✅ **Use testnet** for learning and development
- ✅ **Restrict IP access** in Binance API settings
- ✅ **Regularly rotate** API keys (monthly recommended)
- ✅ **Enable 2FA** on your Binance account
- ✅ **Use minimal permissions** - only enable required features

### Application Security

```env
# Strong session secret (generate new for production)
SESSION_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# API rate limiting
API_RATE_LIMIT=1200  # Prevent abuse

# Secure logging (no sensitive data)
LOG_SENSITIVE_DATA=false
```

### Network Security

- ✅ **Firewall rules** - Block unnecessary ports
- ✅ **VPN usage** - Consider VPN for trading
- ✅ **HTTPS only** - Never use HTTP in production
- ✅ **Local hosting** - Don't expose Flask server publicly

### Data Protection

```python
# Encrypt sensitive data
from cryptography.fernet import Fernet

# Backup important data
python scripts/backup_data.py

# Regular security audits
python scripts/security_check.py
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. PyWebView Installation Problems

**Windows:**

```bash
# If you get DLL errors
pip install --upgrade pywebview
# Or try conda
conda install -c conda-forge pywebview
```

**Linux:**

```bash
# Missing dependencies
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# For newer Ubuntu versions
sudo apt-get install python3-webkitgtk-4.0-dev
```

**macOS:**

```bash
# Install Xcode command line tools
xcode-select --install

# Install via Homebrew
brew install python-tk
```

#### 2. Binance API Connection Issues

**Error: "Invalid API Key"**

```python
# Verify your .env file
cat .env | grep BINANCE_API_KEY

# Test API connection
python scripts/test_api.py
```

**Error: "IP Restriction"**

- Add your IP to Binance API whitelist
- Use VPN if connecting from restricted region
- Check firewall settings

**Error: "Signature Invalid"**

```python
# Check system time synchronization
import time
print(f"System time: {time.time()}")

# Sync time on Windows
w32tm /resync

# Sync time on Linux
sudo ntpdate -s time.nist.gov
```

#### 3. System Tray Issues

**Tray icon not appearing:**

```bash
# Install system tray support
pip install pystray[gtk]  # Linux
pip install pystray[win32]  # Windows
```

**Icon not loading:**

```python
# Check icon file
if not os.path.exists('icon.png'):
    print("Icon file missing - using default")
```

#### 4. Performance Issues

**Slow chart loading:**

```python
# Reduce chart history
CHART_HISTORY_LIMIT = 500  # Default: 1000

# Optimize WebSocket updates
WS_UPDATE_INTERVAL = 1000  # milliseconds
```

**High memory usage:**

```python
# Enable garbage collection
import gc
gc.collect()

# Limit order history
MAX_ORDER_HISTORY = 1000
```

#### 5. Database Issues

**SQLite locked:**

```bash
# Check for zombie processes
ps aux | grep python

# Reset database
python scripts/reset_database.py
```

**Data corruption:**

```bash
# Restore from backup
python scripts/restore_backup.py --date 2024-01-01
```

### Debugging Tools

```bash
# Enable debug mode
export DEBUG_MODE=true
python app.py

# Check logs
tail -f trading_bot.log

# Test individual components
python scripts/test_websocket.py
python scripts/test_database.py
python scripts/test_orders.py
```

### Getting Help

1. __Check logs__: Always check `trading_bot.log` first
2. **Test mode**: Use testnet for troubleshooting
3. **Minimal reproduction**: Create simple test case
4. **System info**: Include OS, Python version, error message
5. **GitHub Issues**: Submit detailed bug reports

---

## 🚀 Building Standalone Executable

### Prerequisites

```bash
pip install pyinstaller>=5.13.0
```

### Build Options

#### 1. Basic Executable

```bash
pyinstaller --onefile --windowed app.py
```

#### 2. Advanced Build (Recommended)

```bash
pyinstaller \
    --onefile \
    --windowed \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --add-data "icon.png:." \
    --add-data "icon.ico:." \
    --icon="icon.ico" \
    --name="TradingBot" \
    --clean \
    app.py
```

#### 3. Development Build (with console)

```bash
pyinstaller \
    --onefile \
    --console \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --name="TradingBot-Debug" \
    app.py
```

### Build Script

```bash
# Use the provided build script
chmod +x build.sh
./build.sh
```

### Cross-Platform Building

**Windows on Linux (using Wine):**

```bash
# Install Wine and Python for Windows
sudo apt-get install wine
# Install Python in Wine environment
# Build with PyInstaller in Wine
```

**macOS App Bundle:**

```bash
# Create .app bundle
python setup.py py2app
```

### Optimization Tips

```bash
# Exclude unnecessary modules
--exclude-module tkinter \
--exclude-module matplotlib \
--exclude-module PIL

# Optimize file size
--strip \
--optimize 2
```

---

## 📦 Distribution

### For End Users

#### Option 1: Standalone Executable

```ini
TradingBot-v1.0.0/
├── TradingBot.exe       # Main executable
├── .env.example         # Configuration template
├── README-USER.md       # User guide
└── icon.png            # Optional custom icon
```

#### Option 2: Installer Package

```bash
# Windows: Create MSI installer
python setup.py bdist_msi

# macOS: Create DMG
python setup.py bdist_dmg

# Linux: Create DEB/RPM
python setup.py bdist_deb
```

### For Developers

#### GitHub Release Package

```ini
trading-bot-desktop-v1.0.0.zip
├── Source code
├── Documentation
├── Example configurations
└── Build scripts
```

#### Docker Distribution

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py", "--headless"]
```

### Security Checklist for Distribution

- ✅ Remove all `.env` files
- ✅ Clear logs and temporary files
- ✅ Remove development dependencies
- ✅ Verify no hardcoded secrets
- ✅ Test executable on clean system
- ✅ Include proper documentation

---

## 🎨 Customization

### UI Themes

```css
/* Create custom theme in static/css/themes/ */
.theme-dark {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
    --accent-color: #007bff;
}

.theme-trading {
    --profit-color: #00d4aa;
    --loss-color: #ff6b6b;
    --neutral-color: #ffd93d;
}
```

### Window Configuration

```python
# In app.py
webview.create_window(
    title="Custom Trading Bot",
    url="http://127.0.0.1:5000",
    width=1400,              # Custom width
    height=900,              # Custom height
    min_size=(800, 600),     # Minimum size
    resizable=True,          # Allow resizing
    fullscreen=False,        # Start fullscreen
    on_top=False,           # Always on top
    shadow=True,            # Window shadow
    transparent=False,       # Transparent window
)
```

### Trading Pairs

```python
# Add custom trading pairs in bot.py
SUPPORTED_PAIRS = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
    'ADA/USDT', 'DOT/USDT', 'LINK/USDT',
    'XRP/USDT', 'LTC/USDT', 'BCH/USDT',
    # Add your preferred pairs
]
```

### Notifications

```python
# Customize notification settings
NOTIFICATION_SETTINGS = {
    'order_filled': True,
    'price_alerts': True,
    'connection_status': False,
    'system_errors': True,
    'sound_enabled': True,
    'sound_file': 'notification.wav'
}
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/trading-bot-desktop.git
cd trading-bot-desktop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest tests/

# Start development server
python app.py --debug
```

### Code Standards

- **Python**: Follow PEP 8, use Black formatter
- **JavaScript**: Follow ESLint rules
- **HTML/CSS**: Use Prettier formatter
- **Documentation**: Update README for new features
- **Testing**: Add tests for new functionality

### Contribution Types

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🎨 **UI/UX enhancements**
- ⚡ **Performance optimizations**
- 🔒 **Security improvements**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```md
MIT License

Copyright (c) 2024 Trading Bot Desktop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🌟 Support

### Getting Help

- 📖 **Documentation**: Check this README and `/docs` folder
- 🐛 **Bug Reports**: Use GitHub Issues with detailed information
- 💬 **Discussions**: Join our GitHub Discussions
- 📧 **Email**: support@tradingbot-desktop.com

### Support the Project

- ⭐ **Star** this repository
- 🍴 **Fork** and contribute
- 📢 **Share** with other traders
- ☕ **Buy us a coffee**: [Sponsor Link]

---

## ⚠️ Disclaimer

**This software is for educational and informational purposes only.**

- ⚠️ **Trading Risk**: Cryptocurrency trading involves substantial risk
- ⚠️ **No Guarantees**: Past performance doesn't guarantee future results
- ⚠️ **Use Testnet**: Always test with Binance Testnet first
- ⚠️ **Your Responsibility**: You are responsible for your trading decisions
- ⚠️ **No Financial Advice**: This software doesn't provide financial advice

**Trade responsibly and never invest more than you can afford to lose.**

---

<div align="center">

**Built By Me**

*Happy Trading! 🚀*

</div>
