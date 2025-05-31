from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, get_font, SIZES, FONT_SIZES
from iot_app.app.utils.logger import logger  # ✅ Logger import

EMULATORS = [
    {"name": "DHT Sensor", "icon": "🌡️", "topic": "group42/dht"},
    {"name": "Light Sensor", "icon": "💡", "topic": "group42/light"},
    {"name": "Motion Sensor", "icon": "🧍", "topic": "group42/motion"},
    {"name": "Door Bell (Button)", "icon": "🔔", "topic": "group42/button"},
    {"name": "Relay", "icon": "🔌", "topic": "group42/relay"},
]


class EmulatorsTab(QWidget):
    def __init__(self, db_client, mqtt_client):
        super().__init__()
        self.db = db_client
        self.mqtt = mqtt_client
        self.setStyleSheet(f"background-color: {COLORS['background']}; color: {COLORS['text']};")
        self.grid = QGridLayout()
        self._build_ui()

    def _build_ui(self):
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
        super().resizeEvent(event)
        self._populate_cards()

    def _populate_cards(self):
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

    def _on_start_clicked(self, name, topic, label):
        logger.info(f"[EMULATOR] '{name}' started")
        self._set_status(label, "ON", True)
        if self.mqtt:
            self.mqtt.publish(topic, "start")

    def _on_stop_clicked(self, name, topic, label):
        logger.info(f"[EMULATOR] '{name}' stopped")
        self._set_status(label, "OFF", False)
        if self.mqtt:
            self.mqtt.publish(topic, "stop")

    def _on_button_pressed(self, button, topic):
        button.setStyleSheet(self._press_button_style(True))
        logger.info(f"[EMULATOR] button pressed")
        if self.mqtt:
            self.mqtt.publish(topic, "pressed")

    def _on_button_released(self, button):
        button.setStyleSheet(self._press_button_style(False))

    def _set_status(self, label, text, is_on):
        color = "#10b981" if is_on else "#ef4444"
        label.setText(text)
        label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _press_button_style(self, pressed):
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
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 14px;
            }}
        """
