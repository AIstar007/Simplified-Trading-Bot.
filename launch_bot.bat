@echo off
title 💱 Trading Bot
color 0A
echo ==============================================
echo        🚀 Starting Trading Bot...
echo ==============================================

REM Check if dependencies are installed
python -c "import sys; sys.exit(0 if all(map(lambda m: m in sys.modules or __import__(m, fromlist=['']), ['flask', 'PIL', 'eel', 'pystray', 'plyer'])) else 1)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Launch the Trading Bot app
python app.py

echo.
echo Press any key to exit...
pause >nul