"""
Project: IoT Smart Home
File: dht_emulator.py
Description:
Emulator for DHT sensor. Simulates temperature and humidity readings.
"""

import random
import json
from iot_app.app.emulators.base_emulator import BaseEmulator


class DHTEmulator(BaseEmulator):
    """
    Emulator class for DHT sensor that generates synthetic temperature and humidity values.
    Publishes readings to MQTT and logs them to the database.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize the DHT emulator with a fixed polling interval.

        Args:
            mqtt_client: MQTTClient instance for publishing.
            db_client: DBClient instance for logging.
        """
        super().__init__(
            device_type="dht",
            mqtt_client=mqtt_client,
            db_client=db_client,
            interval_ms=5000
        )

    def generate_value(self):
        """
        Generate random temperature and humidity values.

        Sets:
            self.current_value (dict): A dictionary with temperature and humidity keys.
        """
        temperature = round(random.uniform(18.0, 32.0), 1)
        humidity = round(random.uniform(30.0, 90.0), 1)
        self.current_value = {
            "temperature": f"{temperature} °C",
            "humidity": f"{humidity} %"
        }

    def build_payload(self) -> str:
        """
        Build a JSON-formatted string payload from current temperature and humidity.

        Returns:
            str: JSON string with temperature and humidity.
        """
        return json.dumps(self.current_value)
