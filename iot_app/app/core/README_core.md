# 🧠 Core Communication Modules – IoT Smart Home

This module contains the **core infrastructure** for communication between devices and the backend in the IoT Smart Home system.

It includes:
- 📡 `MQTTClient` — a wrapper for managing MQTT connections, publishing/subscribing to messages
- 🗄️ `DBClient` — a lightweight MySQL interface for storing and retrieving sensor data

---

## 📦 Modules Overview

### 1. `mqtt_client.py` – MQTT Communication 🔄
This file defines the `MQTTClient` class, which:
- Connects to a Mosquitto MQTT broker
- Subscribes to one or more topics
- Publishes messages to specific topics
- Routes received messages to a callback (e.g., to update the GUI or Room View)
- Handles automatic reconnection in case of disconnect

> ✅ Built on top of `paho-mqtt`  
> 🧵 Runs the MQTT client loop in a background thread  
> 🔁 Includes a `test_connection()` method to check or restore connectivity

---

### 2. `db_client.py` – MySQL Database Interface 🗃️
This file defines the `DBClient` class, which:
- Connects to a MySQL 8.x database (native password plugin)
- Inserts new sensor data into the `device_data` table
- Retrieves the most recent sensor records
- Automatically reconnects if the connection is lost
- Supports test pinging to verify DB health

> ✅ Uses `mysql-connector-python`  
> 🔐 Fully compatible with Dockerized MySQL  
> ⚠️ Gracefully handles missing or broken connections

---

## 🧪 Typical Usage

```python
# MQTT Setup
mqtt = MQTTClient(
    broker_host="localhost",
    broker_port=1883,
    topics=["Home/#"],
    on_message_callback=my_handler
)
mqtt.start()

# DB Setup
db = DBClient()
db.connect()
db.insert_sensor_data("light", "300 lx", datetime.now())
```

---

## ✅ Requirements

Make sure your environment includes:
- `paho-mqtt`
- `mysql-connector-python`
- MySQL running (e.g., via Docker on port 3307)
- MQTT broker (e.g., Mosquitto on ports 1883 / 9001)

---

## 📁 Location
These files should be placed under:

```
iot_app/app/core/
├── db_client.py
└── mqtt_client.py
```

---

## 🧩 Connected To
These modules are tightly integrated with:
- 🧪 Emulators (via `publish()`)
- 📊 GUI Room View (via `on_message_callback`)
- 📦 Logger (`loguru`) for rich debugging

---

## 🧠 Designed for...
> Modular use inside a PyQt-based GUI for real-time IoT emulation, visualization, and analysis.