"""
Project: IoT Smart Home
File: logger.py
Description:
Centralized logger configuration using Loguru.
Supports colored output, file logging, and optional GUI sink.
"""

from loguru import logger
import sys
import os
from datetime import datetime

# ==================== Log Directory & File Setup ====================

LOG_DIR = "sys_logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log filename with current date and time
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = os.path.join(LOG_DIR, f"{timestamp}.log")

# ==================== Handlers Setup ====================

# Remove any existing handlers to avoid duplication
logger.remove()

# Console handler with colored output and detailed formatting
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

# File handler with rotation and compression
logger.add(
    log_file,
    rotation="1 week",
    retention="2 weeks",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# ==================== GUI Sink Support ====================

def add_gui_sink(gui_callback):
    """
    Add a custom log sink for GUI components (e.g., QTextEdit).

    Args:
        gui_callback (Callable): Function to handle log messages.
    """
    logger.add(gui_callback, format="{level.icon} [{level}] {message}", level="INFO")
