"""
Project: IoT Smart Home
File: dashboard_tab.py

Description:
UI module for the DashboardTab screen.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📊 Dashboard overview will be shown here."))
        self.setLayout(layout)
