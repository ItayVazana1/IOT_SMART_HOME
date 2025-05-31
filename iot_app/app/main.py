"""
Project: IoT Smart Home
File: main.py
Updated: 2025-05-31 🕒

Description:
Main GUI window for the IoT Smart Home app.
Includes tab-based layout with Dashboard, Emulator Control,
Logs, Room View Visualization, and Settings.
Handles MQTT and DB connections, and manages periodic status pings.
"""

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QStatusBar, QLabel
from iot_app.app.ui.dashboard_tab import DashboardTab
from iot_app.app.ui.emulators_tab import EmulatorsTab
from iot_app.app.ui.logs_tab import LogsTab
from iot_app.app.ui.room_view_tab import RoomViewTab
from iot_app.app.ui.settings_tab import SettingsTab
from iot_app.app.utils.logger import logger
from iot_app.app.core.db_client import DBClient
from iot_app.app.core.mqtt_client import MQTTClient


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Smart Home")
        self.setFixedSize(1140, 720)

        self.db = None
        self.mqtt = None
        self.next_ping_secs = 30

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._init_status_bar()
        self._init_tabs_placeholder()

        self.status_counter = 3
        self.status_bar.showMessage("Connecting to services in 3 seconds...")
        self._start_connection_countdown()

    def _init_status_bar(self):
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #111111;
                color: white;
                font-size: 12px;
                padding-left: 10px;
            }
        """)
        self.setStatusBar(self.status_bar)

        self.ping_timer_label = QLabel("Next update in: 30s")
        self.ping_timer_label.setStyleSheet("color: #cccccc; padding-right: 14px;")
        self.status_bar.addPermanentWidget(self.ping_timer_label)

    def _init_tabs_placeholder(self):
        self.dashboard_tab = DashboardTab(None, None)
        self.emulators_tab = EmulatorsTab(None, None)
        self.logs_tab = LogsTab()
        self.room_view_tab = RoomViewTab(None, None)
        self.settings_tab = SettingsTab(None, None)

        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.emulators_tab, "🧪 Emulators")
        self.tabs.addTab(self.logs_tab, "📜 Logs")
        self.tabs.addTab(self.room_view_tab, "🏠 Room View")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

    def _start_connection_countdown(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_status_countdown)
        self.timer.start(1000)

    def _update_status_countdown(self):
        if self.status_counter > 1:
            self.status_counter -= 1
            self.status_bar.showMessage(f"Connecting to services in {self.status_counter} seconds...")
        else:
            self.timer.stop()
            self._init_connections()

    def _init_connections(self):
        self.db = DBClient()
        self.db.connect()

        self.mqtt = MQTTClient(
            broker_host="localhost",
            broker_port=1883,
            topics=["group42/#"],
            on_message_callback=self._handle_mqtt_message
        )
        self.mqtt.start()

        QTimer.singleShot(1500, self._finalize_tabs)

    def _finalize_tabs(self):
        mqtt_ok = getattr(self.mqtt, "is_connected", False)
        db_ok = self.db.test_connection() if self.db else False

        self.tabs.clear()
        self.dashboard_tab = DashboardTab(self.db, self.mqtt)
        self.emulators_tab = EmulatorsTab(self.db, self.mqtt)
        self.room_view_tab = RoomViewTab(self.db, self.mqtt)
        self.settings_tab = SettingsTab(self.db, self.mqtt)

        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.emulators_tab, "🧪 Emulators")
        self.tabs.addTab(self.logs_tab, "📜 Logs")
        self.tabs.addTab(self.room_view_tab, "🏠 Room View")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

        # ✅ Run first ping immediately after setup
        self.dashboard_tab.update_status()

        # 🔁 Start recurring ping every 30 seconds
        self._start_ping_loop()

        mqtt_text = "Connected" if mqtt_ok else "Disconnected"
        db_text = "Synced" if db_ok else "No Connection"
        self.status_bar.showMessage(f"MQTT: {mqtt_text} | DB: {db_text}")

        logger.info("🚀 System initialized and GUI loaded.")

    def _start_ping_loop(self):
        self.ping_timer = QTimer(self)
        self.ping_timer.timeout.connect(self._do_ping)
        self.ping_timer.start(30_000)  # Every 30s

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self._tick_ping_countdown)
        self.countdown_timer.start(1000)  # Every second

    def _tick_ping_countdown(self):
        self.next_ping_secs -= 1
        if self.next_ping_secs <= 0:
            self.next_ping_secs = 30
        self.ping_timer_label.setText(f"Next update in: {self.next_ping_secs}s")

    def _do_ping(self):
        self.next_ping_secs = 30
        if self.dashboard_tab:
            self.dashboard_tab.update_status()

    def _handle_mqtt_message(self, topic, payload):
        logger.debug(f"[MainWindow] MQTT message routed | Topic: '{topic}' | Payload: {payload}")


def run_gui():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e2f;
            color: #f1f1f1;
            font-family: 'Segoe UI', sans-serif;
        }
        QWidget {
            background-color: #1e1e2f;
            color: #f1f1f1;
        }
        QLabel {
            color: #f1f1f1;
        }
        QPushButton {
            background-color: #3b82f6;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #60a5fa;
        }
        QTabBar::tab {
            background: #2c2c2c;
            color: white;
            padding: 8px 16px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #3b82f6;
            color: white;
        }
        QTabWidget::pane {
            border: 1px solid #444;
        }
        QGroupBox {
            border: 1px solid #3a3a4a;
            border-radius: 8px;
            margin-top: 10px;
            padding: 10px;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
