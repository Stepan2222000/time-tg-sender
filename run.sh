#!/bin/bash
# Telegram Multi-Account Message Sender - Launch Script
# ======================================================

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"

    echo "Installing dependencies..."
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please configure your Telegram API credentials in .env file"
    echo "See QUICK_START_RU.md for instructions"
fi

# Launch the application
echo "🚀 Starting Telegram Multi-Account Message Sender..."
venv/bin/python main.py

# Check exit code
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Application exited with error code: $EXIT_CODE"
    echo "Check logs in app_data/logs/ for details"
else
    echo "✅ Application closed successfully"
fi
