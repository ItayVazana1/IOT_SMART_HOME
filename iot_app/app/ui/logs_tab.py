"""
Project: IoT Smart Home
File: logs_tab.py
Updated: 2025-05-31  🕒

Description:
UI module for the LogsTab screen.
Displays a live console for event logs, with timestamp, color-coded levels,
clear and save options. Buttons become active only when logs exist.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from datetime import datetime
from iot_app.app.ui.theme import COLORS, get_font, SIZES


class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            background-color: {COLORS['background']};
            color: {COLORS['text']};
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"])

        # Title
        title = QLabel("📜 Live Logs")
        title.setFont(get_font("title", bold=True))
        title.setStyleSheet(f"color: {COLORS['highlight']};")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        # Log Console
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet(f"""
            background-color: {COLORS['secondary']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['border']};
            font-family: Consolas;
            padding: 10px;
            border-radius: {SIZES['corner_radius']}px;
        """)
        layout.addWidget(self.log_console)

        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Unified button style with hover/press/disabled effects
        button_style = f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border-radius: {SIZES['corner_radius']}px;
                padding: 6px 12px;
            }}
            QPushButton:hover:enabled {{
                background-color: {COLORS['highlight']};
                color: {COLORS['background']};
            }}
            QPushButton:pressed:enabled {{
                background-color: {COLORS['secondary']};
            }}
            QPushButton:disabled {{
                background-color: #3a3a3a;
                color: #777777;
            }}
        """

        # Clear Button
        self.clear_button = QPushButton("🧹 Clear Logs")
        self.clear_button.setStyleSheet(button_style)
        self.clear_button.clicked.connect(self.clear_logs)
        self.clear_button.setEnabled(False)
        buttons_layout.addWidget(self.clear_button)

        # Save Button
        self.save_button = QPushButton("💾 Save to File")
        self.save_button.setStyleSheet(button_style)
        self.save_button.clicked.connect(self.save_logs)
        self.save_button.setEnabled(False)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def append_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}"

        # Color by log level
        if "[ERROR]" in message:
            color = COLORS["error"]
        elif "[WARNING]" in message:
            color = COLORS["hover"]
        elif "[INFO]" in message:
            color = COLORS["success"]
        else:
            color = COLORS["text"]

        self.log_console.append(f'<span style="color:{color}">{full_msg}</span>')
        self.log_console.moveCursor(self.log_console.textCursor().End)

        # Enable buttons if needed
        self.clear_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def clear_logs(self):
        self.log_console.clear()
        self.clear_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def save_logs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Log File", "logs.txt", "Text Files (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.log_console.toPlainText())
