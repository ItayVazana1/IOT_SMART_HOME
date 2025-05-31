"""
Project: IoT Smart Home
File: emulators_tab.py
Description:
UI module for the EmulatorsTab screen.
Allows toggling emulators and displaying their status via EmulatorsManager.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, get_font, SIZES, FONT_SIZES
from iot_app.app.utils.logger import logger

EMULATORS = [
    {"name": "DHT Sensor", "icon": "🌡️", "topic": "Home/dht"},
    {"name": "Light Sensor", "icon": "💡", "topic": "Home/light"},
    {"name": "Motion Sensor", "icon": "🧍", "topic": "Home/motion"},
    {"name": "Door Bell (Button)", "icon": "🔔", "topic": "Home/button"},
    {"name": "Relay", "icon": "🔌", "topic": "Home/relay"},
]


class EmulatorsTab(QWidget):
    """
    Emulator control panel for managing and interacting with virtual devices.
    """
    def __init__(self, db_client, mqtt_client, emulators_manager):
        """
        Initialize the Emulators tab with references to clients and emulator manager.

        Args:
            db_client: The database client instance.
            mqtt_client: The MQTT client instance.
            emulators_manager: The emulator manager instance.
        """
        super().__init__()
        self.db = db_client
        self.mqtt = mqtt_client
        self.manager = emulators_manager

        self.setStyleSheet(f"background-color: {COLORS['background']}; color: {COLORS['text']};")
        self.grid = QGridLayout()
        self._build_ui()

    # ===================== UI Construction =====================

    def _build_ui(self):
        """
        Build the emulator control panel UI layout.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"] * 2)

        title = QLabel("🧪 Emulator Control Panel")
        title.setFont(get_font("title", bold=True))
        layout.addWidget(title, alignment=Qt.AlignHCenter)

        self.grid.setSpacing(25)
        layout.addLayout(self.grid)
        layout.addStretch()
        self.setLayout(layout)

        self._populate_cards()

    def resizeEvent(self, event):
        """
        Rebuild emulator cards layout on resize.
        """
        super().resizeEvent(event)
        self._populate_cards()

    def _populate_cards(self):
        """
        Clear and repopulate emulator cards based on current screen size.
        """
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        width = self.width()
        columns = 3 if width >= 1100 else 2

        for idx, emulator in enumerate(EMULATORS):
            row, col = divmod(idx, columns)
            card = self._build_emulator_card(emulator)
            self.grid.addWidget(card, row, col)

    def _build_emulator_card(self, emulator):
        """
        Build a single emulator card with icon, name, and control buttons.

        Args:
            emulator (dict): Emulator configuration dict.

        Returns:
            QFrame: The emulator card widget.
        """
        name = emulator["name"]
        icon = emulator["icon"]
        topic = emulator["topic"]

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        frame.setFixedSize(320, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 40px; border: none;")
        icon_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(name)
        title_label.setFont(get_font("medium", bold=True))
        title_label.setStyleSheet("border: none;")
        title_label.setAlignment(Qt.AlignCenter)

        if "Button" in name:
            press_btn = QPushButton("Press")
            press_btn.setFixedWidth(160)
            press_btn.setStyleSheet(self._press_button_style(False))
            press_btn.pressed.connect(lambda: self._on_button_pressed(press_btn, topic))
            press_btn.released.connect(lambda: self._on_button_released(press_btn))

            layout.addWidget(icon_label)
            layout.addWidget(title_label)
            layout.addStretch()
            layout.addWidget(press_btn, alignment=Qt.AlignCenter)
        else:
            status_label = QLabel("OFF")
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(icon_label)
            layout.addWidget(title_label)
            layout.addWidget(status_label)

            btn_layout = QHBoxLayout()
            start_btn = QPushButton("Start")
            stop_btn = QPushButton("Stop")
            start_btn.setFixedWidth(90)
            stop_btn.setFixedWidth(90)

            start_btn.setStyleSheet(self._alt_button_style("black", "white"))
            stop_btn.setStyleSheet(self._alt_button_style("white", "black"))

            start_btn.clicked.connect(lambda: self._on_start_clicked(name, topic, status_label))
            stop_btn.clicked.connect(lambda: self._on_stop_clicked(name, topic, status_label))

            btn_layout.addWidget(start_btn)
            btn_layout.addWidget(stop_btn)
            layout.addLayout(btn_layout)

        frame.setLayout(layout)
        return frame

    # ===================== Event Handlers =====================

    def _on_start_clicked(self, name, topic, label):
        """
        Handle emulator start event and update UI.

        Args:
            name (str): Device name.
            topic (str): MQTT topic.
            label (QLabel): Status label to update.
        """
        logger.info(f"[EMULATOR] '{name}' started")
        self._set_status(label, "ON", True)
        if self.manager:
            key = self._get_device_key_from_topic(topic)
            self.manager.get(key).turn_on()

    def _on_stop_clicked(self, name, topic, label):
        """
        Handle emulator stop event and update UI.

        Args:
            name (str): Device name.
            topic (str): MQTT topic.
            label (QLabel): Status label to update.
        """
        logger.info(f"[EMULATOR] '{name}' stopped")
        self._set_status(label, "OFF", False)
        if self.manager:
            key = self._get_device_key_from_topic(topic)
            self.manager.get(key).turn_off()

    def _on_button_pressed(self, button, topic):
        """
        Handle virtual button press event.

        Args:
            button (QPushButton): The button widget.
            topic (str): MQTT topic for the button.
        """
        button.setStyleSheet(self._press_button_style(True))
        logger.info(f"[EMULATOR] button pressed")
        if self.manager:
            key = self._get_device_key_from_topic(topic)
            self.manager.get(key).press()

    def _on_button_released(self, button):
        """
        Handle virtual button release event.

        Args:
            button (QPushButton): The button widget.
        """
        button.setStyleSheet(self._press_button_style(False))

    # ===================== Helpers =====================

    def _get_device_key_from_topic(self, topic: str) -> str:
        """
        Extract device key from MQTT topic.

        Args:
            topic (str): MQTT topic.

        Returns:
            str: Device key string.
        """
        return topic.split("/")[-1].lower()

    def _set_status(self, label, text, is_on):
        """
        Update status label text and color.

        Args:
            label (QLabel): The status label.
            text (str): The status text ("ON"/"OFF").
            is_on (bool): Whether the device is active.
        """
        color = "#10b981" if is_on else "#ef4444"
        label.setText(text)
        label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _press_button_style(self, pressed):
        """
        Return stylesheet for the press button based on its state.

        Args:
            pressed (bool): Whether the button is currently pressed.

        Returns:
            str: Stylesheet string.
        """
        return f"""
            QPushButton {{
                background-color: {'white' if pressed else '#555'};
                color: {'black' if pressed else 'white'};
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }}
        """

    def _alt_button_style(self, bg, fg):
        """
        Return stylesheet for Start/Stop buttons.

        Args:
            bg (str): Background color.
            fg (str): Font color.

        Returns:
            str: Stylesheet string.
        """
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 14px;
            }}
        """
