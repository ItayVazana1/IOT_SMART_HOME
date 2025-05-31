"""
Project: IoT Smart Home
File: mqtt_listener.py
Description:
MQTT listener and message router for updating Room View
based on received sensor data and device states.
"""

import json
from iot_app.app.utils.logger import logger


class MQTTListener:
    def __init__(self, room_view):
        """
        Initialize the MQTTListener with a reference to the Room View tab.

        Args:
            room_view: Instance of RoomViewTab responsible for updating UI elements.
        """
        self.room_view = room_view

    def route_message(self, topic: str, payload: str):
        """
        Route incoming MQTT messages to the appropriate handler and update the Room View accordingly.

        Args:
            topic (str): The MQTT topic the message was received on.
            payload (str): The message content as a string.
        """
        logger.debug(f"[Listener] Received → {topic}: {payload}")

        # ===== Validate topic prefix =====
        if not topic.startswith("Home/"):
            return

        key = topic.split("/")[-1].lower()

        # ===== Handle empty or invalid payload =====
        if payload in ("None", "null", "", None):
            self.room_view.update_device_state(key, active=False, reading=None)
            return

        reading = None
        active = False

        try:
            # ===== DHT Sensor =====
            if key == "dht":
                data = json.loads(payload)
                temp = data.get("temperature", "?")
                hum = data.get("humidity", "?")
                reading = f"{temp}, {hum}"
                active = True

            # ===== Light Sensor =====
            elif key == "light":
                reading = payload
                active = True

            # ===== Motion Sensor =====
            elif key == "motion":
                reading = payload
                active = "motion" in payload.lower()

            # ===== Button Press =====
            elif key == "button":
                self.room_view.pulse_button()
                return

            # ===== Relay State =====
            elif key == "relay":
                if payload == "1":
                    reading = "ON"
                    active = True
                elif payload == "0":
                    reading = "OFF"
                    active = False
                else:
                    self.room_view.update_device_state(key, active=False, reading=None)
                    return

            # ===== Unknown Key =====
            else:
                return

            # ===== Final Update =====
            self.room_view.update_device_state(key, active, reading)

        except Exception as e:
            logger.warning(f"[Listener] Failed to handle {topic}: {e}")
