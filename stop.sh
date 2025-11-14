#!/bin/bash
# Telegram Multi-Account Message Sender - Stop Script
# ====================================================

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if running
if ! pgrep -f "python.*main.py" > /dev/null; then
    echo "ℹ️  Application is not running"
    exit 0
fi

echo "🛑 Stopping Telegram Multi-Account Message Sender..."

# Kill all instances
pkill -f "python.*main.py" 2>/dev/null
killall -9 Python python python3 2>/dev/null
sleep 1

# Force kill if still running
if pgrep -f "python.*main.py" > /dev/null; then
    echo "⚠️  Forcing termination..."
    pkill -9 -f "python.*main.py"
    sleep 1
fi

# Clean up database locks
rm -f app_data/app.db-shm app_data/app.db-wal 2>/dev/null

echo "✅ Application stopped successfully"
