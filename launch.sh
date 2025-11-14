#!/bin/bash
# Telegram Multi-Account Message Sender - GUI Launcher
# This script launches the app with proper GUI display on macOS

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing instances
pkill -f "python.*main.py" 2>/dev/null
sleep 1

# Clean database locks
rm -f app_data/app.db-shm app_data/app.db-wal 2>/dev/null

# Set PyQt5 environment variables
export QT_MAC_WANTS_LAYER=1
export QT_AUTO_SCREEN_SCALE_FACTOR=1

# Launch application
exec venv/bin/python main.py
