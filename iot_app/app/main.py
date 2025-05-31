"""
Project: IoT Smart Home
File: main.py
Description:
Main GUI window for the IoT Smart Home app.
Includes tab-based layout with Dashboard, Emulator Control,
Logs, Room View Visualization, and Settings.
Handles MQTT and DB connections, and manages periodic status pings.
"""

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QStatusBar, QLabel, QMessageBox
)

from iot_app.app.ui.dashboard_tab import DashboardTab
from iot_app.app.ui.emulators_tab import EmulatorsTab
from iot_app.app.ui.logs_tab import LogsTab
from iot_app.app.ui.room_view_tab import RoomViewTab
from iot_app.app.ui.settings_tab import SettingsTab
from iot_app.app.utils.logger import logger
from iot_app.app.core.db_client import DBClient
from iot_app.app.core.mqtt_client import MQTTClient
from iot_app.app.emulators_manager import EmulatorsManager
from iot_app.app.mqtt_listener import MQTTListener


class MainWindow(QMainWindow):
    """
    Main GUI window for the IoT Smart Home application.
    Initializes all tabs and handles MQTT/DB connections and updates.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Smart Home")
        self.setFixedSize(1140, 720)

        self.db = None
        self.mqtt = None
        self.manager = None
        self.listener = None
        self.next_ping_secs = 30
        self.first_ping_done = False

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._init_status_bar()
        self._init_tabs_placeholder()

        self.status_counter = 3
        self.status_bar.showMessage("Connecting to services in 3 seconds...")
        self._start_connection_countdown()

    # ==================== UI Initialization ====================

    def _init_status_bar(self):
        """
        Initialize the custom status bar with countdown label.
        """
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
        """
        Create placeholder tabs with None values until services are connected.
        """
        self.dashboard_tab = DashboardTab(None, None)
        self.emulators_tab = EmulatorsTab(None, None, None)
        self.logs_tab = LogsTab()
        self.room_view_tab = RoomViewTab(None, None, None)
        self.settings_tab = SettingsTab(None, None)

        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.emulators_tab, "🧪 Emulators")
        self.tabs.addTab(self.logs_tab, "📜 Logs")
        self.tabs.addTab(self.room_view_tab, "🏠 Room View")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

    # ==================== Service Initialization ====================

    def _start_connection_countdown(self):
        """
        Begin countdown before attempting initial connection.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_status_countdown)
        self.timer.start(1000)

    def _update_status_countdown(self):
        """
        Update countdown each second and connect when it reaches zero.
        """
        if self.status_counter > 1:
            self.status_counter -= 1
            self.status_bar.showMessage(f"Connecting to services in {self.status_counter} seconds...")
        else:
            self.timer.stop()
            self._init_connections()

    def _init_connections(self):
        """
        Initialize DB and MQTT connections, and delay tab finalization.
        """
        self.db = DBClient()
        self.mqtt = MQTTClient(
            broker_host="localhost",
            broker_port=1883,
            topics=["Home/#"],
            on_message_callback=self._handle_mqtt_message
        )
        self.mqtt.start()
        self.manager = EmulatorsManager(self.mqtt, self.db)
        QTimer.singleShot(1500, self._finalize_tabs)

    def _finalize_tabs(self):
        """
        After successful connection, replace placeholder tabs with live components.
        """
        self.db.connect()
        logger.info("🚀 System initialized and GUI loaded.")

        mqtt_ok = self.mqtt and self.mqtt.is_connected
        db_ok = self.db and self.db.test_connection

        if not mqtt_ok or not db_ok:
            logger.error("🛑 Connection failed. Prompting retry...")
            self._show_connection_error_popup()
            return

        self.tabs.clear()
        self.dashboard_tab = DashboardTab(self.db, self.mqtt, self.manager)
        self.room_view_tab = RoomViewTab(self.db, self.mqtt, self.manager)
        self.listener = MQTTListener(room_view=self.room_view_tab)
        self.emulators_tab = EmulatorsTab(self.db, self.mqtt, self.manager)
        self.settings_tab = SettingsTab(self.db, self.mqtt)

        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.emulators_tab, "🧪 Emulators")
        self.tabs.addTab(self.logs_tab, "📜 Logs")
        self.tabs.addTab(self.room_view_tab, "🏠 Room View")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

        self.dashboard_tab.update_status()
        self._start_ping_loop()
        self._update_status_bar(mqtt_ok, db_ok)

    # ==================== Ping Loop ====================

    def _start_ping_loop(self):
        """
        Start timers for updating the system status every 30 seconds.
        """
        self.ping_timer = QTimer(self)
        self.ping_timer.timeout.connect(self._do_ping)
        self.ping_timer.start(30_000)

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self._tick_ping_countdown)
        self.countdown_timer.start(1000)

    def _tick_ping_countdown(self):
        """
        Update the visual countdown label for the next status ping.
        """
        self.next_ping_secs -= 1
        if self.next_ping_secs <= 0:
            self.next_ping_secs = 30
        self.ping_timer_label.setText(f"Next update in: {self.next_ping_secs}s")

    def _do_ping(self):
        """
        Perform status check for MQTT and DB, update dashboard and status bar.
        """
        self.next_ping_secs = 30
        if not self.first_ping_done:
            self.first_ping_done = True
            return

        mqtt_ok = self.mqtt and self.mqtt.is_connected
        db_ok = self.db and self.db.test_connection()

        self._update_status_bar(mqtt_ok, db_ok)
        self.dashboard_tab.update_status()

    def _update_status_bar(self, mqtt_ok, db_ok):
        """
        Update the status bar colors and message based on current connection state.
        """
        color = "#10b981" if mqtt_ok and db_ok else "#f43f5e"
        mqtt_text = "Connected" if mqtt_ok else "Disconnected"
        db_text = "Synced" if db_ok else "No Connection"
        self.status_bar.showMessage(f"MQTT: {mqtt_text} | DB: {db_text}")
        self.status_bar.setStyleSheet(f"background-color: #111111; color: {color}; font-size: 12px;")

    # ==================== MQTT Handler ====================

    def _handle_mqtt_message(self, topic, payload):
        """
        Forward incoming MQTT messages to the listener.
        """
        logger.debug(f"[MainWindow] MQTT message routed | Topic: '{topic}' | Payload: {payload}")
        if self.listener:
            try:
                self.listener.route_message(topic, payload)
            except Exception as e:
                logger.warning(f"[MainWindow] Failed to handle message: {e}")

    # ==================== Error Handling ====================

    def _show_connection_error_popup(self):
        """
        Display popup to retry connection if MQTT or DB failed to connect.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Connection Error")
        msg.setText("Failed to connect to MQTT broker or Database.\nPlease check your setup and try again.")
        msg.setStandardButtons(QMessageBox.Retry)
        if msg.exec_() == QMessageBox.Retry:
            self._init_connections()


# ==================== App Entry Point ====================

def run_gui():
    """
    Entry point for launching the PyQt5 GUI application.
    """
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
