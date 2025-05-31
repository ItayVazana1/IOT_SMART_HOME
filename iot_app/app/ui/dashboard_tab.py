"""
Project: IoT Smart Home
File: dashboard_tab.py

Description:
UI module for the DashboardTab screen.
Displays general system status: MQTT, emulators, DB, etc.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, SIZES


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {COLORS['background']}; color: {COLORS['text']};")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"] * 3)

        # Large emoji
        emoji = QLabel("📊")
        emoji.setAlignment(Qt.AlignCenter)
        emoji.setStyleSheet("font-size: 48px; margin-bottom: -5px;")
        layout.addWidget(emoji)

        # Main title
        title = QLabel("System Overview")
        title_font = QFont("Segoe UI", 30)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['highlight']}; margin-bottom: 10px;")
        layout.addWidget(title)

        # Card row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(SIZES["padding"] * 2)
        cards_layout.setAlignment(Qt.AlignCenter)

        cards_layout.addWidget(self._build_status_card("🛰️", "MQTT", "Connected", COLORS["success"]))
        cards_layout.addWidget(self._build_status_card("🗄️", "Database", "Synced", COLORS["success"]))
        cards_layout.addWidget(self._build_status_card("🧪", "Emulators", "5 Active", COLORS["highlight"]))

        cards_container = QWidget()
        cards_container.setLayout(cards_layout)
        cards_container.setMaximumWidth(1000)

        layout.addStretch()
        layout.addWidget(cards_container, alignment=Qt.AlignHCenter)
        layout.addStretch()
        self.setLayout(layout)

    def _build_status_card(self, icon, title_text, status_text, status_color):
        frame = QFrame()
        frame.setObjectName("card")
        frame.setFixedSize(240, 200)

        frame.setStyleSheet(f"""
            #card {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['corner_radius']}px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Emoji label
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 46px; margin-bottom: -4px;")
        icon_label.setAlignment(Qt.AlignCenter)

        # Title label
        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)

        # Status banner
        status_banner = QLabel(status_text)
        status_banner.setAlignment(Qt.AlignCenter)
        status_banner.setFont(QFont("Segoe UI", 12, QFont.Bold))
        status_banner.setStyleSheet(f"""
            background-color: {status_color};
            color: {self._get_dark_variant(status_color)};
            padding: 6px 18px;
            border-radius: {SIZES['corner_radius']}px;
        """)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(status_banner)
        layout.addStretch()

        frame.setLayout(layout)
        return frame

    def _get_dark_variant(self, base_color):
        """Returns a darker variant of the given badge color."""
        mapping = {
            COLORS["success"]: "#065f46",
            COLORS["primary"]: "#1e40af",
            COLORS["highlight"]: "#92400e"
        }
        return mapping.get(base_color, "#111111")
