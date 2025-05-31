"""
Project: IoT Smart Home
File: logger.py
Updated: 2025-05-31 🕒

Description:
Centralized logger configuration using Loguru.
Supports colored output, file logging, and optional GUI sink.
"""

from loguru import logger
import sys
import os
from datetime import datetime

# Logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name based on current date
log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Remove existing handlers to avoid duplicates
logger.remove()

# Console logging (with color)
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

# File logging (rotated weekly, kept 2 weeks, zipped)
logger.add(
    log_file,
    rotation="1 week",
    retention="2 weeks",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


def add_gui_sink(gui_callback):
    """
    Add a custom sink for GUI components like QTextEdit.

    :param gui_callback: A callable (e.g., append_log method) to handle log messages.
    """
    logger.add(gui_callback, format="{level.icon} [{level}] {message}", level="INFO")
