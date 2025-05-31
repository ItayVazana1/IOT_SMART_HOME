"""
Project: IoT Smart Home
File: db_client.py
Description:
MySQL client module using mysql-connector-python.
Handles connection to Dockerized MySQL database and provides read/write operations.
"""

import mysql.connector
from iot_app.app.utils.logger import logger


class DBClient:
    """
    MySQL client wrapper for IoT sensor data handling.
    Supports connection, reconnection, insertion, fetching, and testing.
    """
    def __init__(self,
                 host="localhost",
                 port=3307,
                 user="iotuser",
                 password="iotpass",
                 database="iot_data"):
        """
        Initialize the DB client with connection parameters.

        Args:
            host (str): MySQL host address.
            port (int): MySQL port number.
            user (str): MySQL username.
            password (str): MySQL password.
            database (str): Database name to connect to.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        """
        Establish connection to the MySQL database.
        Uses mysql_native_password authentication.
        """
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
        Reconnect to the database after closing any existing connection.
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
        Insert a sensor reading into the database.

        Args:
            device_type (str): Device key (e.g., 'dht').
            value (str): Sensor reading.
            timestamp (datetime): Time of reading.
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
        Fetch the most recent device data records.

        Args:
            limit (int): Number of records to retrieve.

        Returns:
            list[dict]: A list of result rows as dictionaries.
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
        Test the current database connection and reconnect if needed.

        Returns:
            bool: True if ping succeeded, False otherwise.
        """
        try:
            if not self.conn or not self.conn.is_connected():
                logger.warning("[DB] No active connection. Attempting to reconnect...")
                self.connect()

            self.conn.ping(reconnect=True)
            logger.success("[DB] Ping successful ✔")
            return True

        except mysql.connector.Error as e:
            logger.error(f"[DB] Ping or reconnect error: {e}")
            return False

    def close(self):
        """
        Close the current database connection.
        """
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.info("[DB] Connection closed.")
