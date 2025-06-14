"""
Project: IoT Smart Home
File: dashboard_tab.py
Description:
UI module for the DashboardTab screen.
Displays general system status: MQTT, emulators, DB, etc.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from iot_app.app.ui.theme import COLORS, SIZES


class DashboardTab(QWidget):
    """
    Main dashboard UI displaying connection status for MQTT, DB, and emulators.
    """
    def __init__(self, db_client=None, mqtt_client=None, manager=None):
        """
        Initialize the dashboard tab with references to MQTT, DB, and emulator manager.

        Args:
            db_client: Optional DBClient instance.
            mqtt_client: Optional MQTTClient instance.
            manager: Optional EmulatorsManager instance.
        """
        super().__init__()
        self.setStyleSheet(f"background-color: {COLORS['background']}; color: {COLORS['text']};")

        self.db_client = db_client
        self.mqtt_client = mqtt_client
        self.manager = manager

        self.mqtt_status_label = None
        self.db_status_label = None
        self.emulator_status_label = None

        self._build_ui()

    # ============================ UI Construction ============================

    def _build_ui(self):
        """
        Build the main layout and status card components for the dashboard.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(SIZES["margin"], SIZES["margin"], SIZES["margin"], SIZES["margin"])
        layout.setSpacing(SIZES["padding"] * 3)

        emoji = QLabel("📊")
        emoji.setAlignment(Qt.AlignCenter)
        emoji.setStyleSheet("font-size: 48px; margin-bottom: -5px;")
        layout.addWidget(emoji)

        title = QLabel("System Overview")
        title_font = QFont("Segoe UI", 30)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['highlight']}; margin-bottom: 10px;")
        layout.addWidget(title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(SIZES["padding"] * 2)
        cards_layout.setAlignment(Qt.AlignCenter)

        self.mqtt_status_label = self._build_status_card("📡", "MQTT", "Disconnected", "#991b1b")
        self.db_status_label = self._build_status_card("🗄️", "Database", "No Connection", "#991b1b")
        self.emulator_status_label = self._build_status_card("🧪", "Emulators", "Unavailable", "#6b7280")

        cards_layout.addWidget(self.mqtt_status_label)
        cards_layout.addWidget(self.db_status_label)
        cards_layout.addWidget(self.emulator_status_label)

        container = QWidget()
        container.setLayout(cards_layout)
        container.setMaximumWidth(1000)

        layout.addStretch()
        layout.addWidget(container, alignment=Qt.AlignHCenter)
        layout.addStretch()

        self.setLayout(layout)

    def _build_status_card(self, icon, title_text, default_status, default_color):
        """
        Create a single status card widget with icon, title, and banner.

        Args:
            icon (str): Emoji or icon string.
            title_text (str): The title of the card (e.g. MQTT).
            default_status (str): Initial status text.
            default_color (str): Background color for banner.

        Returns:
            QFrame: Configured status card widget.
        """
        frame = QFrame()
        frame.setObjectName("card")
        frame.setFixedSize(240, 200)
        frame.setStyleSheet(f"""
            #card {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['corner_radius']}px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 46px;")
        icon_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)

        status_banner = QLabel(default_status)
        status_banner.setAlignment(Qt.AlignCenter)
        status_banner.setFont(QFont("Segoe UI", 12, QFont.Bold))
        status_banner.setStyleSheet(f"""
            background-color: {default_color};
            color: {self._get_dark_variant(default_color)};
            padding: 6px 18px;
            border-radius: 8px;
        """)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(status_banner)
        layout.addStretch()

        frame.setLayout(layout)
        frame.status_banner = status_banner
        return frame

    # ============================ Status Update ============================

    def update_status(self):
        """
        Update the status of each card (MQTT, DB, Emulators) based on current connection states.
        """
        mqtt_ok = self.mqtt_client.test_connection() if self.mqtt_client else False
        if mqtt_ok:
            self._update_card(self.mqtt_status_label, "Connected", COLORS["success"])
        else:
            self._update_card(self.mqtt_status_label, "Disconnected", "#991b1b")

        db_ok = False
        if self.db_client:
            try:
                db_ok = self.db_client.test_connection()
            except Exception:
                db_ok = False
        if db_ok:
            self._update_card(self.db_status_label, "Synced", COLORS["success"])
        else:
            self._update_card(self.db_status_label, "No Connection", "#991b1b")

        try:
            if self.manager and hasattr(self.manager, "emulators"):
                active = [em for em in self.manager.emulators.values() if em.active]
                self._update_card(self.emulator_status_label, f"{len(active)} Active", COLORS["highlight"])
            else:
                raise AttributeError
        except Exception:
            self._update_card(self.emulator_status_label, "Unavailable", "#6b7280")

    def _update_card(self, card, text, bg_color):
        """
        Update a specific card's banner text and background color.

        Args:
            card (QFrame): The card widget to update.
            text (str): New status text.
            bg_color (str): Background color to apply.
        """
        card.status_banner.setText(text)
        card.status_banner.setStyleSheet(f"""
            background-color: {bg_color};
            color: {self._get_dark_variant(bg_color)};
            padding: 6px 18px;
            border-radius: 8px;
        """)

    def _get_dark_variant(self, base_color):
        """
        Return a dark font color variant based on background color.

        Args:
            base_color (str): The background color.

        Returns:
            str: Corresponding dark font color.
        """
        mapping = {
            COLORS["success"]: "#065f46",
            COLORS["primary"]: "#1e40af",
            COLORS["highlight"]: "#92400e",
            "#991b1b": "#ffffff",
            "#6b7280": "#ffffff",
        }
        return mapping.get(base_color, "#111111")
