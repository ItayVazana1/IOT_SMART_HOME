"""
Project: IoT Smart Home
File: relay_emulator.py
Description:
Emulator for Relay device. Toggles ON/OFF state and sends signal accordingly.
"""

from iot_app.app.emulators.base_emulator import BaseEmulator


class RelayEmulator(BaseEmulator):
    """
    Emulator for a binary relay switch (ON/OFF).
    Publishes state immediately when toggled.
    """
    def __init__(self, mqtt_client, db_client):
        """
        Initialize the relay emulator with polling disabled.

        Args:
            mqtt_client: MQTTClient instance for publishing.
            db_client: DBClient instance for logging.
        """
        super().__init__(
            device_type="relay",
            mqtt_client=mqtt_client,
            db_client=db_client,
            interval_ms=0
        )

    def generate_value(self):
        """
        Unused for relay. State is controlled manually via turn_on/turn_off.
        """
        pass

    def turn_on(self):
        """
        Set relay state to ON, publish and log the event.
        """
        self.active = True
        self.current_value = "1"
        self.publish()
        self.save_to_db()

    def turn_off(self):
        """
        Set relay state to OFF, publish and log the event.
        """
        self.active = False
        self.current_value = "0"
        self.publish()
        self.save_to_db()

    def build_payload(self) -> str:
        """
        Return the current relay state as string payload.

        Returns:
            str: '1' if ON, '0' if OFF.
        """
        return self.current_value
