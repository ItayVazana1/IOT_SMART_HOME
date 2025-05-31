"""
Project: IoT Smart Home
File: db_client.py
Updated: 2025-05-31 🕒

Description:
MySQL client module using mysql-connector-python.
Handles connection to Dockerized MySQL database and provides read/write operations.
"""

import mysql.connector
from iot_app.app.utils.logger import logger


class DBClient:
    def __init__(self,
                 host="localhost",
                 port=3307,
                 user="iotuser",
                 password="iotpass",
                 database="iot_data"):
        """
        Initialize the DB client with connection parameters.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            logger.info(f"[DB] Connecting to MySQL at {self.host}:{self.port}...")
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin="mysql_native_password"
            )
            if self.conn.is_connected():
                logger.success("[DB] Connected to MySQL database ✔")
        except mysql.connector.InterfaceError as e:
            logger.error(f"[DB] InterfaceError: {e}")
        except mysql.connector.DatabaseError as e:
            logger.error(f"[DB] DatabaseError: {e}")
        except Exception as e:
            logger.error(f"[DB] Unexpected connection error: {e}")

    def reconnect(self):
        """
        Reconnect to the database.
        """
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
                logger.info("[DB] Previous connection closed.")
        except Exception as e:
            logger.warning(f"[DB] Error while closing existing connection: {e}")

        self.connect()

    def insert_sensor_data(self, device_type: str, value: str, timestamp):
        """
        Insert a record into device_data table.
        """
        if not self.conn or not self.conn.is_connected():
            logger.warning("[DB] Cannot insert — no active connection.")
            return

        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO device_data (device_type, value, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(query, (device_type, value, timestamp))
            self.conn.commit()
            cursor.close()
            logger.info(f"[DB] Inserted: {device_type} | {value} | {timestamp}")
        except mysql.connector.ProgrammingError as e:
            logger.error(f"[DB] ProgrammingError: {e}")
        except mysql.connector.DatabaseError as e:
            logger.error(f"[DB] Insert DatabaseError: {e}")
        except Exception as e:
            logger.error(f"[DB] Unexpected insert error: {e}")

    def fetch_latest_records(self, limit=10):
        """
        Retrieve recent device data from DB.
        """
        if not self.conn or not self.conn.is_connected():
            logger.warning("[DB] Cannot fetch — no active connection.")
            return []

        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM device_data ORDER BY timestamp DESC LIMIT %s"
            cursor.execute(query, (limit,))
            records = cursor.fetchall()
            cursor.close()
            logger.info(f"[DB] Fetched {len(records)} records.")
            return records
        except mysql.connector.ProgrammingError as e:
            logger.error(f"[DB] Fetch ProgrammingError: {e}")
        except mysql.connector.DatabaseError as e:
            logger.error(f"[DB] Fetch DatabaseError: {e}")
        except Exception as e:
            logger.error(f"[DB] Unexpected fetch error: {e}")
            return []

    def test_connection(self):
        """
        Try to ping the DB, and reconnect automatically if needed.
        """
        try:
            if self.conn is None or not self.conn.is_connected():
                logger.warning("[DB] No active connection. Attempting to reconnect...")
                self.connect()

            if self.conn is None or not self.conn.is_connected():
                logger.error("[DB] Reconnection failed ✖")
                return False

            self.conn.ping(reconnect=True)
            logger.success("[DB] Ping successful ✔")
            return True

        except mysql.connector.Error as e:
            logger.error(f"[DB] Ping or reconnect error: {e}")
            return False

    def close(self):
        """Close the DB connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.info("[DB] Connection closed.")
