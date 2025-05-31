"""
Project: IoT Smart Home
File: settings_tab.py

Description:
UI module for the SettingsTab screen.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ Settings panel for configuration."))
        self.setLayout(layout)
