"""
Project: IoT Smart Home
File: gui_main.py

Description:
Main GUI window for the IoT Smart Home app.
Includes tab-based layout with Dashboard, Emulator Control,
Logs, Room View Visualization, and Settings.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QStatusBar
)

from ui.dashboard_tab import DashboardTab
from ui.emulators_tab import EmulatorsTab
from ui.logs_tab import LogsTab
from ui.room_view_tab import RoomViewTab
from ui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Smart Home")
        self.setGeometry(100, 100, 1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._init_tabs()
        self._init_status_bar()

    def _init_tabs(self):
        self.tabs.addTab(DashboardTab(), "Dashboard")
        self.tabs.addTab(EmulatorsTab(), "Emulators")
        self.tabs.addTab(LogsTab(), "Logs")
        self.tabs.addTab(RoomViewTab(), "Room View")
        self.tabs.addTab(SettingsTab(), "Settings")

    def _init_status_bar(self):
        status_bar = QStatusBar()
        status_bar.showMessage("MQTT: Connected | DB: Synced")
        self.setStatusBar(status_bar)


def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
