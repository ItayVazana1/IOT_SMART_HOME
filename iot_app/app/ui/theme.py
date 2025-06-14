"""
Project: IoT Smart Home
File: theme.py
Description:
Centralized visual constants for fonts, colors, spacing and sizing.
Does not override stylesheet – intended for code-level usage.
"""

from PyQt5.QtGui import QFont

COLORS = {
    "background": "#1e1e2f",
    "secondary": "#2c2c3c",
    "text": "#f1f1f1",
    "text_secondary": "#a0a0a0",
    "primary": "#3b82f6",
    "hover": "#60a5fa",
    "success": "#10b981",
    "error": "#ef4444",
    "border": "#3a3a4a",
    "highlight": "#facc15",
    "card": "#27293d",
}

FONT_SIZES = {
    "small": 11,
    "normal": 13,
    "medium": 15,
    "large": 18,
    "title": 22,
}

SIZES = {
    "margin": 30,
    "padding": 15,
    "button_width": 200,
    "corner_radius": 6,
}


def get_font(size="normal", bold=False):
    """
    Return a configured QFont based on size keyword and bold flag.

    Args:
        size (str): One of 'small', 'normal', 'medium', 'large', or 'title'.
        bold (bool): Whether to return a bold font.

    Returns:
        QFont: Configured font object.
    """
    font = QFont("Segoe UI")
    font.setPointSize(FONT_SIZES.get(size, 13))
    font.setBold(bold)
    return font
