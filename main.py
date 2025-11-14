"""
Main entry point for the Telegram Multi-Account Message Sender.

This is the new production-grade version with GUI support.
"""

import sys
import asyncio
import platform
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from app.services import initialize_database, get_settings, get_logger
from app.gui.main import MainWindow

# Import all models to ensure they are registered with SQLModel
from app.models import Account, Campaign, Recipient, SendLog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


def main():
    """Main application entry point."""
    # CRITICAL: Set Qt attributes BEFORE creating QApplication
    # Enable High DPI scaling for Retina displays (macOS)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Initialize services
    initialize_database()
    settings = get_settings()
    logger = get_logger()

    logger.info("Starting Telegram Multi-Account Message Sender")
    logger.info(f"Platform: {platform.system()}")

    # Create Qt application
    logger.info("Creating QApplication...")
    app = QApplication(sys.argv)
    logger.info("QApplication created")
    app.setApplicationName("Telegram Multi-Account Message Sender")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("VoxHash")
    logger.info("Application metadata set")

    # Set application icon
    icon_path = Path(__file__).parent / "assets" / "icons" / "favicon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Set application style
    app.setStyle('Fusion')

    # Create main window
    logger.info("Creating MainWindow...")
    main_window = MainWindow()
    logger.info("MainWindow created")

    # Show window initially
    main_window.show()
    logger.info("Window initially shown")

    # macOS-specific window activation workaround
    # Use QTimer to activate window AFTER event loop starts
    if platform.system() == "Darwin":  # macOS
        def activate_window_delayed():
            """Delayed window activation for macOS - workaround for focus issues."""
            logger.info("Applying delayed macOS window activation workaround...")

            # Save original window flags
            original_flags = main_window.windowFlags()

            # Temporarily set WindowStaysOnTopHint to force window to front
            main_window.setWindowFlags(original_flags | Qt.WindowStaysOnTopHint)
            main_window.show()
            logger.info("Window shown with StaysOnTop flag")

            # Remove the always-on-top flag
            main_window.setWindowFlags(original_flags)
            main_window.show()
            logger.info("Window shown with normal flags")

            # Additional activation attempts
            main_window.raise_()
            main_window.activateWindow()

            # Force window to active state
            main_window.setWindowState((main_window.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
            logger.info("macOS window activation completed")

        # Schedule activation 200ms after event loop starts
        QTimer.singleShot(200, activate_window_delayed)
        logger.info("Scheduled delayed window activation")
    else:
        # Standard activation for other platforms
        main_window.raise_()
        main_window.activateWindow()
        logger.info("Window activated")

    logger.info("Starting Qt event loop...")
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()