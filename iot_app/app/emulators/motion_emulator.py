"""
Project: IoT Smart Home
File: motion_emulator.py
Description:
Emulator for Motion Sensor. Randomly simulates motion detection.
"""

import random
from iot_app.app.emulators.base_emulator import BaseEmulator


class MotionEmulator(BaseEmulator):
    """
    Emulator class for a motion sensor that randomly simulates movement detection.
    Publishes results to MQTT and logs them to the database.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize the motion emulator with a 3-second polling interval.

        Args:
            mqtt_client: MQTTClient instance for publishing.
            db_client: DBClient instance for logging.
        """
        super().__init__(
            device_type="motion",
            mqtt_client=mqtt_client,
            db_client=db_client,
            interval_ms=3000
        )

    def generate_value(self):
        """
        Generate a motion reading.
        80% chance to detect motion, 20% chance of no motion.
        """
        self.current_value = "motion detected" if random.random() < 0.8 else "no motion"

    def build_payload(self) -> str:
        """
        Return the current motion state as a payload string.

        Returns:
            str: Either 'motion detected' or 'no motion'.
        """
        return self.current_value
