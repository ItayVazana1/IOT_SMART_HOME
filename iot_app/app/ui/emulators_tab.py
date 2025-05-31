"""
Project: IoT Smart Home
File: emulators_tab.py

Description:
UI module for the EmulatorsTab screen.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class EmulatorsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🧪 Emulators control panel will be displayed here."))
        self.setLayout(layout)
