"""
Project: IoT Smart Home
File: room_view_tab.py
Updated: 2025-05-31 🕒

Description:
UI module for the RoomViewTab screen.
Displays a visual layout of a room and real-time statuses of IoT devices.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, get_font, SIZES


class RoomViewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.device_boxes = {}  # Holds references to update states later
        self.reading_labels = {}  # Holds references to reading displays
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        main_layout.setSpacing(SIZES["padding"])

        # Left Panel: Status & Readings
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(SIZES["padding"])

        title = QLabel("🏠 Visual Room Overview")
        title.setFont(get_font("title", bold=True))
        title.setStyleSheet(f"color: {COLORS['highlight']};")
        left_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Add static status labels (simulated)
        for name in ["Door", "Light", "Motion", "DHT", "Relay"]:
            label = QLabel(f"{name}: 🔄 Waiting...")
            label.setFont(get_font("normal"))
            label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            left_layout.addWidget(label)
            self.reading_labels[name.lower()] = label

        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        left_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Right Panel: Room Grid
        right_panel = QWidget()
        grid = QGridLayout()
        grid.setSpacing(25)

        # Device positions
        positions = {
            (0, 0): ("🚪 Door", "door"),
            (0, 2): ("💡 Light", "light"),
            (1, 1): ("🧍 Motion", "motion"),
            (2, 0): ("🌡️ DHT", "dht"),
            (2, 2): ("🔌 Relay", "relay"),
        }

        for (row, col), (label, key) in positions.items():
            box = QFrame()
            box.setStyleSheet(self._style_inactive())
            box.setFixedSize(120, 100)

            text = QLabel(label)
            text.setFont(get_font("normal", bold=True))
            text.setAlignment(Qt.AlignCenter)
            text.setStyleSheet("color: black;")

            inner_layout = QVBoxLayout()
            inner_layout.addStretch()
            inner_layout.addWidget(text)
            inner_layout.addStretch()
            box.setLayout(inner_layout)

            grid.addWidget(box, row, col)
            self.device_boxes[key] = box

        right_panel.setLayout(grid)
        right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Combine panels
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        self.setLayout(main_layout)

    def _style_inactive(self):
        return """
            QFrame {
                background-color: white;
                border: 2px solid #999;
                border-radius: 8px;
            }
        """

    def _style_active(self):
        return """
            QFrame {
                background-color: #10b981;
                border: 2px solid #0f766e;
                border-radius: 8px;
            }
        """

    def update_device_state(self, device_key: str, active: bool, reading: str = None):
        """
        Update the visual state of a device in the room.
        :param device_key: "door", "light", etc.
        :param active: True = green box, False = white
        :param reading: Optional text to update on the left
        """
        if device_key in self.device_boxes:
            style = self._style_active() if active else self._style_inactive()
            self.device_boxes[device_key].setStyleSheet(style)

        if reading is not None and device_key in self.reading_labels:
            self.reading_labels[device_key].setText(f"{device_key.capitalize()}: {reading}")
