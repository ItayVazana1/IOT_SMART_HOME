"""
Project: IoT Smart Home
File: room_view_tab.py
Description:
GUI tab for visualizing smart devices in a room layout.
Displays active status and latest reading for each emulator.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from iot_app.app.ui.theme import COLORS, get_font, SIZES
from iot_app.app.utils.logger import logger


class RoomViewTab(QWidget):
    """
    Visual interface for showing device status in a smart room layout.
    Includes live updates from the EmulatorsManager.
    """
    def __init__(self, db_client, mqtt_client, manager):
        """
        Initialize the Room View with connections to services.

        Args:
            db_client: The database client instance.
            mqtt_client: The MQTT client instance.
            manager: The emulators manager instance.
        """
        super().__init__()
        self.db = db_client
        self.mqtt = mqtt_client
        self.manager = manager

        self.device_boxes = {}
        self.reading_labels = {}
        self._doorbell_seconds_left = 0

        self._doorbell_timer = QTimer()
        self._doorbell_timer.setInterval(1000)
        self._doorbell_timer.timeout.connect(self._tick_doorbell_timer)

        self.init_ui()

        self._refresh_timer = QTimer()
        self._refresh_timer.timeout.connect(self.refresh)
        self._refresh_timer.start(500)

    # ==================== UI Layout ====================

    def init_ui(self):
        """
        Build the split-screen layout: left (text info) and right (visual map).
        """
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(SIZES["margin"], SIZES["margin"],
                                       SIZES["margin"], SIZES["margin"])
        main_layout.setSpacing(SIZES["padding"])

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        self.setLayout(main_layout)

    def _build_left_panel(self):
        """
        Build the left text-based panel with device names and values.
        """
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(SIZES["padding"])

        title = QLabel("🏠 Visual Room Overview")
        title.setFont(get_font("title", bold=True))
        title.setStyleSheet(f"color: {COLORS['highlight']};")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        for key in ["doorbell", "light", "motion", "dht", "relay"]:
            row = QHBoxLayout()
            name = QLabel(f"{key.capitalize()}:")
            name.setStyleSheet("background-color: black; color: white; padding: 3px 8px;")
            name.setFont(get_font("normal", bold=True))

            value = QLabel("🔄 Waiting...")
            value.setStyleSheet("color: white; font-weight: bold; padding-left: 6px;")
            value.setFont(get_font("small"))

            row.addWidget(name)
            row.addWidget(value)
            self.reading_labels[key] = value
            layout.addLayout(row)

        layout.addStretch()
        panel.setLayout(layout)
        panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        return panel

    def _build_right_panel(self):
        """
        Build the right visual grid layout with device boxes.
        """
        panel = QWidget()
        grid = QGridLayout()
        grid.setSpacing(25)

        positions = {
            (0, 0): ("🔔 Door Bell", "doorbell"),
            (0, 2): ("💡 Light", "light"),
            (1, 1): ("🧍 Motion", "motion"),
            (2, 0): ("🌡️ DHT", "dht"),
            (2, 2): ("🔌 Relay", "relay"),
        }

        for (row, col), (text, key) in positions.items():
            box = QFrame()
            box.setStyleSheet(self._style_inactive())
            box.setFixedSize(120, 100)

            label = QLabel(text)
            label.setFont(get_font("normal", bold=True))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; border: none;")

            layout = QVBoxLayout()
            layout.addStretch()
            layout.addWidget(label)
            layout.addStretch()
            box.setLayout(layout)

            grid.addWidget(box, row, col)
            self.device_boxes[key] = box

        panel.setLayout(grid)
        panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return panel

    # ==================== Style Helpers ====================

    def _style_inactive(self):
        return """
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #444;
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

    # ==================== Refresh and Update ====================

    def _tick_doorbell_timer(self):
        """
        Countdown handler for doorbell visual indicator.
        """
        self._doorbell_seconds_left -= 1
        if self._doorbell_seconds_left <= 0:
            self._doorbell_timer.stop()
        self.refresh()

    def refresh(self):
        """
        Refresh UI with latest emulator states and readings.
        """
        if self.manager is None:
            return

        key_map = {
            "button": "doorbell",
            "light": "light",
            "motion": "motion",
            "dht": "dht",
            "relay": "relay",
        }

        for emu_key, gui_key in key_map.items():
            emulator = self.manager.get(emu_key)
            if emulator is None:
                continue

            active = getattr(emulator, "active", False)
            reading = getattr(emulator, "current_value", None)

            if emu_key == "button":
                if active and self._doorbell_seconds_left > 0:
                    reading = f"Pressed ({self._doorbell_seconds_left})"
                else:
                    reading = None

            if emu_key == "relay":
                if not active:
                    reading = None
                elif reading == "1":
                    reading = "ON"
                elif reading == "0":
                    reading = "OFF"

            if isinstance(reading, dict):
                reading = f"{reading.get('temperature', '')}, {reading.get('humidity', '')}".strip(", ")

            if reading is not None and not isinstance(reading, str):
                reading = str(reading)

            self.update_device_state(gui_key, active, reading)

    def update_device_state(self, device_key: str, active: bool, reading: str = None):
        """
        Update the visual box and label for a given device.

        Args:
            device_key (str): The device ID used in the GUI.
            active (bool): Whether the device is considered active.
            reading (str): Latest reading text, if any.
        """
        changed = False

        if device_key in self.device_boxes:
            box = self.device_boxes[device_key]
            new_style = self._style_active() if active else self._style_inactive()
            if box.styleSheet() != new_style:
                box.setStyleSheet(new_style)
                changed = True

        if device_key in self.reading_labels:
            label = self.reading_labels[device_key]
            new_text = reading if reading is not None else "🔄 Waiting..."
            if label.text() != new_text:
                label.setText(new_text)
                changed = True

            if reading:
                label.setStyleSheet("color: white; font-weight: bold; padding-left: 6px;")
            else:
                label.setStyleSheet("color: gray; font-weight: normal;")

        if changed:
            logger.info(f"[ROOM] {device_key} updated → {'ON' if active else 'OFF'}, Reading: {reading or '-'}")

    def pulse_doorbell(self, duration_ms: int = 7000):
        """
        Trigger a visual doorbell animation for a given duration.

        Args:
            duration_ms (int): Time in milliseconds for the bell to stay active.
        """
        self._doorbell_seconds_left = duration_ms // 1000
        QTimer.singleShot(0, self._start_doorbell_timer_safe)

    def _start_doorbell_timer_safe(self):
        """
        Ensure doorbell timer is started within GUI thread context.
        """
        self._doorbell_timer.start()

    def pulse_button(self):
        """
        Compatibility alias for external MQTT calls.
        Triggers the doorbell pulse animation.
        """
        self.pulse_doorbell()
