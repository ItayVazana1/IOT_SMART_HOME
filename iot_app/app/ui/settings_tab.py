"""
Project: IoT Smart Home
File: settings_tab.py
Description:
GUI tab for application settings.
Includes MQTT and DB controls, exit button, and app credits.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, SIZES, get_font
from iot_app.app.utils.logger import logger
import sys


class SettingsTab(QWidget):
    """
    Tab for application settings: reconnection, database testing, exit, and credits.
    """
    def __init__(self, db_client, mqtt_client):
        """
        Initialize the Settings tab with MQTT and DB client references.

        Args:
            db_client: Instance of DBClient.
            mqtt_client: Instance of MQTTClient.
        """
        super().__init__()
        self.db = db_client
        self.mqtt = mqtt_client
        self._build_ui()

    # ====================== UI Construction ======================

    def _build_ui(self):
        """
        Build and style the settings layout and controls.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"] * 2)

        exit_btn = self._styled_button("⏻ Exit App", self._handle_exit, COLORS["error"])
        exit_btn.setFixedWidth(160)
        layout.addWidget(exit_btn, alignment=Qt.AlignCenter)

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

        credit_title = QLabel("App Credits")
        credit_title.setFont(get_font("medium", bold=True))
        credit_title.setStyleSheet(f"color: {COLORS['text']}; margin-top: 20px;")
        layout.addWidget(credit_title, alignment=Qt.AlignCenter)

        dev1 = QLabel("👨‍💻 Developed by: Itay Vazana")
        dev2 = QLabel("👨‍💻 Co-Developer: Omer Trabulski")

        for label in [dev1, dev2]:
            label.setFont(get_font("normal", bold=True))
            label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            layout.addWidget(label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _styled_button(self, text, handler, bg_color=None):
        """
        Create a styled QPushButton and connect it to a handler.

        Args:
            text (str): Button label.
            handler (callable): Function to run on click.
            bg_color (str): Optional background color.

        Returns:
            QPushButton: Styled button.
        """
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

    # ====================== Handlers ======================

    def _handle_reconnect(self):
        """
        Attempt to reconnect to the MQTT broker.
        """
        logger.info("[SETTINGS] Reconnecting to MQTT broker...")
        if self.mqtt:
            self.mqtt.reconnect()
            QMessageBox.information(self, "Reconnect", "Reconnection attempted.")
        else:
            QMessageBox.warning(self, "Reconnect", "MQTT client not available.")

    def _handle_test_db(self):
        """
        Test the connection to the database and show a result popup.
        """
        logger.info("[SETTINGS] Testing connection to database...")
        if self.db and self.db.test_connection():
            QMessageBox.information(self, "Database", "DB connection successful ✔")
        else:
            QMessageBox.critical(self, "Database", "DB connection failed ✖")

    def _handle_exit(self):
        """
        Prompt user to confirm application exit.
        """
        reply = QMessageBox.question(self, "Exit App", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(0)
