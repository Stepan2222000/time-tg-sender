#!/bin/bash
# Simple GUI launcher - run this script to start the app

cd "$(dirname "$0")"

# Kill existing instances
pkill -f "python.*main.py" 2>/dev/null
sleep 1

# Clean locks
rm -f app_data/app.db-shm app_data/app.db-wal 2>/dev/null

# Set PyQt5 environment
export QT_MAC_WANTS_LAYER=1
export QT_AUTO_SCREEN_SCALE_FACTOR=1

echo "🚀 Launching Telegram Multi-Account Message Sender..."
echo ""
echo "The GUI window will appear in a moment."
echo "If you don't see it, check Cmd+Tab or Mission Control."
echo ""

# Run the application
exec venv/bin/python main.py
