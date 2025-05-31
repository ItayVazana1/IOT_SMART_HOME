"""
Project: IoT Smart Home
File: light_emulator.py
Description:
Emulator for Light Sensor. Simulates ambient light intensity (0–1000 lx).
"""

import random
from iot_app.app.emulators.base_emulator import BaseEmulator


class LightEmulator(BaseEmulator):
    """
    Emulator class for a light sensor that generates synthetic lux readings.
    Publishes data to MQTT and logs to the database.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize the light sensor emulator with a 2-second polling interval.

        Args:
            mqtt_client: MQTTClient instance for publishing.
            db_client: DBClient instance for logging.
        """
        super().__init__(
            device_type="light",
            mqtt_client=mqtt_client,
            db_client=db_client,
            interval_ms=2000
        )

    def generate_value(self):
        """
        Generate a random ambient light intensity value (0–1000 lx).
        Sets self.current_value to a formatted string.
        """
        lux = random.randint(0, 1000)
        self.current_value = f"{lux} lx"

    def build_payload(self) -> str:
        """
        Build the MQTT payload for the current lux value.

        Returns:
            str: Light intensity in lux as string.
        """
        return str(self.current_value)
