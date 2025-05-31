"""
Project: IoT Smart Home
File: logger.py

Description:
Centralized logger configuration using Loguru.
Supports colored output and per-module logging.
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

# Clear previous handlers (for safe reimporting)
logger.remove()

# Console handler with colors
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

# File handler
logger.add(
    log_file,
    rotation="1 week",
    retention="2 weeks",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
