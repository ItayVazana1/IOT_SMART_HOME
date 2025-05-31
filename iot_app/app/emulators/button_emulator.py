"""
Project: IoT Smart Home
File: button_emulator.py
Description:
Emulator for a doorbell button. Publishes 'pressed' on each trigger and logs the event to the database.
Includes internal timer to reset active state.
"""

from PyQt5.QtCore import QTimer
from iot_app.app.emulators.base_emulator import BaseEmulator


class ButtonEmulator(BaseEmulator):
    """
    Emulator for a momentary button (doorbell).
    Sends a 'pressed' signal and automatically resets after a short interval.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize the button emulator with no polling and reset timer.

        Args:
            mqtt_client: MQTTClient instance for publishing.
            db_client: DBClient instance for logging.
        """
        super().__init__(
            device_type="button",
            mqtt_client=mqtt_client,
            db_client=db_client,
            interval_ms=0
        )
        self._active_for_ms = 7000
        self._reset_timer = QTimer()
        self._reset_timer.setSingleShot(True)
        self._reset_timer.timeout.connect(self._reset_state)

    def press(self):
        """
        Simulate a button press: publish 'pressed' state and start reset timer.
        """
        self.current_value = "pressed"
        self.active = True
        self.publish()
        self.save_to_db()
        self._reset_timer.start(self._active_for_ms)

    def _reset_state(self):
        """
        Reset the button state back to inactive.
        """
        self.current_value = None
        self.active = False
        self.publish()

    def generate_value(self):
        """
        Unused for button emulator. No automatic value generation.
        """
        pass

    def build_payload(self) -> str:
        """
        Return the current button state payload.

        Returns:
            str: 'pressed' or 'idle' depending on current state.
        """
        return self.current_value if self.current_value else "idle"
