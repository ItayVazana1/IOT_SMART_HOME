"""
Project: IoT Smart Home
File: mqtt_client.py
Description:
MQTT client module for subscribing and publishing to the IoT broker.
Connects to Mosquitto broker and interacts with the RoomView GUI.
"""

import socket
import threading
import paho.mqtt.client as mqtt
from iot_app.app.utils.logger import logger


class MQTTClient:
    """
    MQTT client wrapper for managing connection, publishing, subscription, and reconnection.
    """

    def __init__(self, broker_host="localhost", broker_port=1883, topics=None, on_message_callback=None):
        """
        Initialize MQTT client with broker details and optional message handler.

        Args:
            broker_host (str): MQTT broker address.
            broker_port (int): MQTT broker port.
            topics (list): List of topics to subscribe to.
            on_message_callback (callable): Callback function on new message.
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topics = topics or []
        self.on_message_callback = on_message_callback

        hostname = socket.gethostname()
        self.client = mqtt.Client(client_id=f"SmartHomeApp-{hostname}")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        """
        Internal callback for MQTT connection event.

        Args:
            client: MQTT client instance.
            userdata: Unused.
            flags: Connection flags.
            rc: Result code.
        """
        if rc == 0:
            logger.success(f"[MQTT] Connected to broker at {self.broker_host}:{self.broker_port}")
            for topic in self.topics:
                client.subscribe(topic)
                logger.info(f"[MQTT] Subscribed to topic: {topic}")
        else:
            logger.error(f"[MQTT] Failed to connect (RC={rc}) to broker at {self.broker_host}:{self.broker_port}")

    def _on_message(self, client, userdata, msg):
        """
        Internal callback for received messages.

        Args:
            client: MQTT client.
            userdata: Unused.
            msg: Incoming MQTT message.
        """
        try:
            payload = msg.payload.decode()
            topic = msg.topic
            logger.debug(f"[MQTT] Received on '{topic}': {payload}")

            if self.on_message_callback:
                self.on_message_callback(topic, payload)
        except Exception as e:
            logger.warning(f"[MQTT] Error processing message: {e}")

    def start(self):
        """
        Start MQTT client loop in a background thread.
        """
        logger.info(f"[MQTT] Attempting to connect to {self.broker_host}:{self.broker_port}...")
        thread = threading.Thread(target=self._run_loop, daemon=True)
        thread.start()

    def _run_loop(self):
        """
        Internal loop that maintains connection with the broker.
        """
        try:
            logger.debug(f"[MQTT] Running MQTT loop for {self.broker_host}:{self.broker_port}")
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_forever()
        except Exception as e:
            logger.error(f"[MQTT] Connection loop failed: {e}")

    def reconnect(self):
        """
        Reconnect to the MQTT broker by resetting the client.
        """
        try:
            logger.info("[MQTT] Reconnecting to broker...")
            self.client.disconnect()
        except Exception as e:
            logger.warning(f"[MQTT] Disconnect before reconnect failed: {e}")

        hostname = socket.gethostname()
        self.client = mqtt.Client(client_id=f"SmartHomeApp-{hostname}")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.start()

    def publish(self, topic, message):
        """
        Publish a message to a given MQTT topic.

        Args:
            topic (str): Topic to publish to.
            message (str): Message content.
        """
        try:
            result = self.client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"[MQTT] Published to '{topic}': {message}")
            else:
                logger.warning(f"[MQTT] Failed to publish to '{topic}' (rc={result.rc})")
        except Exception as e:
            logger.error(f"[MQTT] Publish exception: {e}")

    def test_connection(self):
        """
        Test connection to the MQTT broker, and reconnect if needed.

        Returns:
            bool: True if connection is active, else False.
        """
        try:
            if self.client is None:
                logger.error("[MQTT] Client not initialized.")
                return False

            if not self.client.is_connected():
                logger.warning("[MQTT] Not connected. Attempting to reconnect...")
                self.reconnect()

            if self.client.is_connected():
                logger.success("[MQTT] Ping successful ✔")
                return True
            else:
                logger.error("[MQTT] Reconnection failed ✖")
                return False

        except Exception as e:
            logger.error(f"[MQTT] Ping or reconnect error: {e}")
            return False

    @property
    def is_connected(self):
        """
        Check if the MQTT client is connected.

        Returns:
            bool: True if connected.
        """
        connected = self.client is not None and self.client.is_connected()
        logger.debug(f"[MQTT] is_connected check: {connected}")
        return connected
