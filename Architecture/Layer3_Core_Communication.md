# 🔌 Part 3 – Core Layer: Communication and Data

## 📄 Key Files

| File             | Role Description |
|------------------|------------------|
| `mqtt_client.py` | Manages the MQTT connection: connect, publish, subscribe, handle messages |
| `db_client.py`   | Manages MySQL connection: connect, insert, fetch, auto-reconnect |

---

## 📡 MQTTClient – Full MQTT Management

### 🧠 Connection Initialization
```python
self.client = mqtt.Client(...)
self.client.on_connect = self._on_connect
self.client.on_message = self._on_message
```
- Uses `paho-mqtt` library
- Detects connection success and subscribes to all topics (`Home/#`)

---

### 🧾 Publishing Messages
```python
self.client.publish(topic, message)
```
- Called from emulators
- Checks for success and logs accordingly

---

### 📥 Receiving Messages
```python
def _on_message(...):
    self.on_message_callback(topic, payload)
```
- Receives incoming MQTT messages
- Routes them via `MainWindow._handle_mqtt_message → MQTTListener.route_message`

---

### 🔄 Reconnection Logic
- `reconnect()` resets and restarts the client
- `test_connection()` sends ping and reconnects if needed

---

## 🗄️ DBClient – MySQL Integration

### 🧠 Connecting to the Database
```python
mysql.connector.connect(..., auth_plugin="mysql_native_password")
```
- Connects to `localhost:3307` (Docker-based MySQL)
- Supports auto-reconnection

---

### 📥 Inserting Data
```python
insert_sensor_data(device_type, value, timestamp)
```
- Called from emulators
- Stores data into `device_data` table
- Logs each insert with timestamp

---

### 📤 Fetching Data
```python
fetch_latest_records(limit=10)
```
- Retrieves the latest N records
- Used by Dashboard or Settings tab

---

### 🧪 Testing Connection
```python
test_connection()
```
- Reconnects if not connected
- Uses `conn.ping()` to validate connection health

---

## 🔁 Full Integration Flow

1. An emulator (e.g., `LightEmulator`) generates a value  
2. `self.publish()` sends it to MQTT  
3. `MQTTClient._on_message()` triggers callback  
4. `MQTTListener` processes it and updates Room View  
5. At the same time, `self.save_to_db()` writes to MySQL

---

## ✅ Core Layer Summary Table

| Component     | Purpose                    | Used By             | Interacts With           |
|---------------|-----------------------------|----------------------|---------------------------|
| MQTTClient    | Publish, subscribe, receive | Emulators / GUI      | Mosquitto, GUI            |
| DBClient      | Insert / fetch from DB      | Emulators / GUI      | MySQL, DashboardTab       |
| MainWindow    | Coordinator for services     | At startup           | Initializes MQTT, DB, Tabs |