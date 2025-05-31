"""
Project: IoT Smart Home
File: main.py

Description:
Main GUI window for the IoT Smart Home app.
Includes tab-based layout with Dashboard, Emulator Control,
Logs, Room View Visualization, and Settings.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QStatusBar
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

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._init_tabs()
        self._init_status_bar()

        # Lock window size
        self.setFixedSize(1140, 720)

        # Optional: add tracking for responsive breakpoints
        self.responsive_columns = 3 if self.width() > 1100 else 2

    def _init_tabs(self):
        self.tabs.addTab(DashboardTab(), "📊 Dashboard")
        self.tabs.addTab(EmulatorsTab(), "🧪 Emulators")
        self.tabs.addTab(LogsTab(), "📜 Logs")
        self.tabs.addTab(RoomViewTab(), "🏠 Room View")
        self.tabs.addTab(SettingsTab(), "⚙️ Settings")

    def _init_status_bar(self):
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #111111;
                color: white;
                font-size: 12px;
                padding-left: 10px;
            }
        """)
        status_bar.showMessage("MQTT: Connected | DB: Synced")
        self.setStatusBar(status_bar)


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
