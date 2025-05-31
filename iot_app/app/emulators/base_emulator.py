"""
Project: IoT Smart Home
File: base_emulator.py
Description:
Base logic class for all emulators. Handles value generation, MQTT publishing,
DB logging, and periodic polling with QTimer support.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from PyQt5.QtCore import QTimer
from iot_app.app.utils.logger import logger

TOPIC_BASE = "Home"


class BaseEmulator(ABC):
    """
    Abstract base class for IoT device emulators.
    Supports MQTT publishing, DB logging, and timed polling.
    """

    def __init__(self, device_type: str, mqtt_client, db_client, interval_ms=5000):
        """
        Initialize emulator with device type, MQTT and DB clients, and interval.

        Args:
            device_type (str): Unique key of the device (e.g., 'dht').
            mqtt_client: Connected instance of MQTTClient.
            db_client: Connected instance of DBClient.
            interval_ms (int): Polling frequency in milliseconds.
        """
        self.device_type = device_type
        self.topic = f"{TOPIC_BASE}/{device_type}"
        self.mqtt = mqtt_client
        self.db = db_client
        self.active = False
        self.current_value = None
        self.interval_ms = interval_ms

        self.timer = QTimer()
        self.timer.setInterval(self.interval_ms)
        self.timer.timeout.connect(self._tick)

        logger.debug(f"[Emulator] Initialized: {device_type} → {self.topic}")

    # ========================== State Control ==========================

    def turn_on(self):
        """
        Activate emulator and start periodic polling.
        """
        self.active = True
        self.timer.start()
        self._tick()
        logger.info(f"[Emulator] {self.device_type} turned ON")

    def turn_off(self):
        """
        Deactivate emulator and stop polling.
        """
        self.active = False
        self.timer.stop()
        self.current_value = None
        self.publish()
        logger.info(f"[Emulator] {self.device_type} turned OFF")

    # ========================== Core Logic ==========================

    def _tick(self):
        """
        Perform one emulator cycle: generate value, publish, and save to DB.
        """
        if not self.active:
            return
        self.generate_value()
        self.publish()
        self.save_to_db()

    def publish(self):
        """
        Publish the current value to the MQTT broker on the associated topic.
        """
        payload = self.build_payload()
        if self.mqtt:
            self.mqtt.publish(self.topic, payload)
        logger.debug(f"[MQTT] Published to '{self.topic}': {payload}")

    def save_to_db(self):
        """
        Save the current value to the database with a timestamp.
        """
        if self.db and self.current_value is not None:
            now = datetime.now()
            self.db.insert_sensor_data(self.device_type, str(self.current_value), now)

    # ========================== Abstracts ==========================

    @abstractmethod
    def generate_value(self):
        """
        Generate a new sensor value. Must set self.current_value.
        """
        pass

    @abstractmethod
    def build_payload(self) -> str:
        """
        Format the current value as an MQTT-compatible payload.

        Returns:
            str: The payload string to be published.
        """
        pass
