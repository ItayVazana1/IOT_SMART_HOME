"""
Project: IoT Smart Home
File: logs_tab.py

Description:
UI module for the LogsTab screen.
Displays a live console for event logs.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📜 Live Logs"))
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("background-color: #1e1e1e; color: #f1f1f1; font-family: Consolas;")
        layout.addWidget(self.log_console)
        self.setLayout(layout)

    def append_log(self, message: str):
        self.log_console.append(message)
