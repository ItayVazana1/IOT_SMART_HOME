"""
Project: IoT Smart Home
File: emulators_manager.py
Description:
Central manager for all emulators. Initializes and stores instances for shared use.
"""

from iot_app.app.emulators.button_emulator import ButtonEmulator
from iot_app.app.emulators.dht_emulator import DHTEmulator
from iot_app.app.emulators.light_emulator import LightEmulator
from iot_app.app.emulators.motion_emulator import MotionEmulator
from iot_app.app.emulators.relay_emulator import RelayEmulator


class EmulatorsManager:
    """
    Manages and stores all emulator instances in a centralized dictionary.
    Used to access emulator logic across the application.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize all emulator instances and assign them to a shared dictionary.

        Args:
            mqtt_client: Instance of the MQTTClient for publishing messages.
            db_client: Instance of the DBClient for data logging.
        """
        self.emulators = {
            "button": ButtonEmulator(mqtt_client, db_client),
            "dht": DHTEmulator(mqtt_client, db_client),
            "light": LightEmulator(mqtt_client, db_client),
            "motion": MotionEmulator(mqtt_client, db_client),
            "relay": RelayEmulator(mqtt_client, db_client),
        }

    def get(self, device_type: str):
        """
        Retrieve an emulator instance by its type key (e.g., "relay", "dht").

        Args:
            device_type (str): The device type key to retrieve.

        Returns:
            Emulator instance if found, otherwise None.
        """
        return self.emulators.get(device_type)
