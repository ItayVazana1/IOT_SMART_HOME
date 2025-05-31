from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, get_font, SIZES, FONT_SIZES

EMULATORS = [
    {"name": "DHT Sensor", "icon": "🌡️"},
    {"name": "Light Sensor", "icon": "💡"},
    {"name": "Motion Sensor", "icon": "🎯"},
    {"name": "Button", "icon": "🔘"},
    {"name": "Relay", "icon": "🔌"},
]


class EmulatorsTab(QWidget):
    def __init__(self):
        super().__init__()
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
            card = self._build_emulator_card(emulator["name"], emulator["icon"])
            self.grid.addWidget(card, row, col)

    def _build_emulator_card(self, name, icon):
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

        if name == "Button":
            press_btn = QPushButton("Press")
            press_btn.setFixedWidth(160)
            press_btn.setStyleSheet(self._press_button_style(False))
            press_btn.pressed.connect(lambda: press_btn.setStyleSheet(self._press_button_style(True)))
            press_btn.released.connect(lambda: press_btn.setStyleSheet(self._press_button_style(False)))
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

            start_btn.clicked.connect(lambda: self._set_status(status_label, "ON", True))
            stop_btn.clicked.connect(lambda: self._set_status(status_label, "OFF", False))

            btn_layout.addWidget(start_btn)
            btn_layout.addWidget(stop_btn)
            layout.addLayout(btn_layout)

        frame.setLayout(layout)
        return frame

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
