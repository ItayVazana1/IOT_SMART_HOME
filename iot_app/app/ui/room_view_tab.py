"""
Project: IoT Smart Home
File: room_view_tab.py

Description:
UI module for the RoomViewTab screen.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class RoomViewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏠 Visual room layout and actuator states go here."))
        self.setLayout(layout)
