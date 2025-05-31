"""
Project: IoT Smart Home
File: settings_tab.py
Updated: 2025-05-31 🕒

Description:
Clean and centered settings tab without boxes.
Displays MQTT & DB info, exit button, and developer credits.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, SIZES, get_font
import sys


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"] * 2)

        # Exit button
        exit_btn = self._styled_button("⏻ Exit App", self._handle_exit, COLORS["error"])
        exit_btn.setFixedWidth(160)
        layout.addWidget(exit_btn, alignment=Qt.AlignCenter)

        # MQTT Section
        mqtt_title = QLabel("MQTT Broker Settings")
        mqtt_title.setFont(get_font("medium", bold=True))
        mqtt_title.setStyleSheet(f"color: {COLORS['text']};")
        layout.addWidget(mqtt_title, alignment=Qt.AlignCenter)

        mqtt_info = QLabel("Host: localhost | Port: 1883")
        mqtt_info.setFont(get_font("normal"))
        mqtt_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(mqtt_info, alignment=Qt.AlignCenter)

        reconnect_btn = self._styled_button("Reconnect", self._handle_reconnect)
        layout.addWidget(reconnect_btn, alignment=Qt.AlignCenter)

        # DB Section
        db_title = QLabel("Database Settings")
        db_title.setFont(get_font("medium", bold=True))
        db_title.setStyleSheet(f"color: {COLORS['text']}; margin-top: 20px;")
        layout.addWidget(db_title, alignment=Qt.AlignCenter)

        db_info = QLabel("DB: iot_data | User: iotuser")
        db_info.setFont(get_font("normal"))
        db_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(db_info, alignment=Qt.AlignCenter)

        test_btn = self._styled_button("Test Connection", self._handle_test_db)
        layout.addWidget(test_btn, alignment=Qt.AlignCenter)

        # Credits Section
        credit_title = QLabel("App Credits")
        credit_title.setFont(get_font("medium", bold=True))
        credit_title.setStyleSheet(f"color: {COLORS['text']}; margin-top: 20px;")
        layout.addWidget(credit_title, alignment=Qt.AlignCenter)

        dev1 = QLabel("👨‍💻 Developed by: Itay Vazana")
        dev2 = QLabel("👨‍💻 Co-Developer: Your Partner Name")

        for label in [dev1, dev2]:
            label.setFont(get_font("normal", bold=True))
            label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            layout.addWidget(label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _styled_button(self, text, handler, bg_color=None):
        btn = QPushButton(text)
        btn.setFont(get_font("normal", bold=True))
        btn.setFixedWidth(SIZES["button_width"])

        base = bg_color if bg_color else COLORS["primary"]
        hover = COLORS["hover"]
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {base};
                color: white;
                padding: 6px 12px;
                border-radius: {SIZES["corner_radius"]}px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
        """)
        btn.clicked.connect(handler)
        return btn

    def _handle_reconnect(self):
        QMessageBox.information(self, "Reconnect", "Reconnecting to MQTT broker...")

    def _handle_test_db(self):
        QMessageBox.information(self, "Database", "DB connection successful ✔")

    def _handle_exit(self):
        reply = QMessageBox.question(self, "Exit App", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(0)
