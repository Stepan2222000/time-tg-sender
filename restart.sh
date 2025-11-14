#!/bin/bash
# Telegram Multi-Account Message Sender - Restart Script
# ========================================================
# Usage: ./restart.sh [stop]
#   Without arguments: Restart (stop old + start new)
#   With 'stop': Only stop the application

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if running
IS_RUNNING=$(pgrep -f "python.*main.py" > /dev/null && echo "yes" || echo "no")

# If 'stop' argument provided, just stop and exit
if [ "$1" == "stop" ]; then
    if [ "$IS_RUNNING" == "no" ]; then
        echo "ℹ️  Application is not running"
        exit 0
    fi

    echo "🛑 Stopping Telegram Multi-Account Message Sender..."
    pkill -f "python.*main.py" 2>/dev/null
    killall -9 Python python python3 2>/dev/null
    sleep 1

    if pgrep -f "python.*main.py" > /dev/null; then
        pkill -9 -f "python.*main.py"
        sleep 1
    fi

    echo "✅ Application stopped"
    exit 0
fi

echo "🔄 Restarting Telegram Multi-Account Message Sender..."
echo ""

# Step 1: Kill all running instances
echo "📛 Stopping all running instances..."
pkill -f "python.*main.py" 2>/dev/null
killall -9 Python python python3 2>/dev/null
sleep 1

# Verify all processes are stopped
if pgrep -f "python.*main.py" > /dev/null; then
    echo "⚠️  Warning: Some processes may still be running"
    echo "   Forcing termination..."
    pkill -9 -f "python.*main.py"
    sleep 1
fi

echo "✅ All previous instances stopped"

# Step 2: Clean up database lock files
echo "🧹 Cleaning up database lock files..."
rm -f app_data/app.db-shm app_data/app.db-wal 2>/dev/null
echo "✅ Lock files removed"

# Step 3: Wait a moment for system cleanup
echo "⏳ Waiting for cleanup..."
sleep 2

# Step 4: Start fresh instance
echo ""
echo "🚀 Starting fresh instance..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./run.sh first to set up the environment"
    exit 1
fi

# Create logs directory if not exists
mkdir -p app_data/logs

# Launch the application
echo "Starting GUI application..."

# Set environment variables for PyQt5
export QT_MAC_WANTS_LAYER=1
export QT_AUTO_SCREEN_SCALE_FACTOR=1

# Launch in foreground
exec venv/bin/python main.py
