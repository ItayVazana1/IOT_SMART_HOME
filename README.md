
# 🏡 IoT Smart Home System

A full-stack **IoT simulation platform** built with Python, MQTT, MySQL, and PyQt5.  
Simulates sensors and devices, visualizes real-time data, logs events, and offers full GUI control.

---

## 📌 Project Overview

This smart home system includes:

- 🧠 **Emulators** for common devices (DHT, light sensor, motion, button, relay)
- 💬 **MQTT communication** via Mosquitto (Docker)
- 🛢️ **MySQL database** with real-time inserts and logging
- 🖥️ **Interactive GUI** (PyQt5) with dashboards, room view, log console, and more
- 📜 **Dockerized infrastructure** for reproducible local deployment

---

## 🧱 Folder Structure

```
iot_app/
├── app/
│   ├── core/              # MQTT + DB clients
│   ├── emulators/         # Device emulator logic
│   ├── ui/                # All PyQt5 UI tabs + theme
│   ├── utils/             # Logger configuration
│   ├── emulators_manager.py
│   ├── mqtt_listener.py
│   └── main.py
├── requirements.txt
mosquitto/
├── config/                # mosquitto.conf
mysql/
├── init.sql               # DB schema + user creation
├── my.cnf                 # Force mysql_native_password plugin
├── mysql_native_password_fix_guide.txt
```

---

## 🧪 Modules Breakdown

### 🧠 Emulators (`iot_app/app/emulators`)
Simulates 5 device types:
- `DHT`: temperature & humidity (every 5s)
- `Light`: lux value (every 2s)
- `Motion`: motion detection (every 3s)
- `Button`: "pressed" event + resets (5s)
- `Relay`: manually toggle ON/OFF

All inherit from a shared base class with:
- MQTT publishing
- DB logging
- Auto-polling (via QTimer)

### 💬 Core Services (`iot_app/app/core`)
- `MQTTClient`: wraps Paho client for pub/sub + callbacks + reconnect logic
- `DBClient`: MySQL client with insert/test/fetch methods, reconnect support

### 🎛 Main Controllers (`iot_app/app`)
- `main.py`: Entry point for the app
- `emulators_manager.py`: Manages all emulator instances and interface methods
- `mqtt_listener.py`: Subscribes to topics and routes incoming messages to UI

### 🧠 UI Tabs (`iot_app/app/ui`)
- `DashboardTab`: system status (MQTT, DB, emulators)
- `EmulatorsTab`: toggle buttons and feedback for all devices
- `RoomViewTab`: visual map of active devices
- `LogsTab`: real-time logger with color-coded messages
- `SettingsTab`: reconnect, exit, test DB
- `theme.py`: global styling and color palette

### 📚 Logging (`iot_app/app/utils/logger.py`)
Uses **Loguru** for clean, color-coded logging to:
- Console
- GUI logs tab
- Optional log file (`iot_logs.txt`)

### 🧱 MQTT Broker (Mosquitto)
Runs via Docker with:
- Port `1883` for standard clients
- Port `9001` for WebSocket access
- Logging to stdout
- Anonymous access (for dev only — 🔐 disable in production)

### 🗄️ MySQL Setup
- Dockerized MySQL (port `3307`)
- Auto-creates:
  - `iot_data` database
  - `iotuser` with full privileges
  - `device_data` table
- Uses `mysql_native_password` for full compatibility  
  ➕ Includes manual fix script if needed

---

## 🐳 Docker Setup

To run services locally:

```bash
docker-compose up -d
```

- Mosquitto: `localhost:1883` (MQTT), `localhost:9001` (WebSocket)
- MySQL: `localhost:3307`
- Adminer UI: `localhost:8080`

---

## 🖥 GUI Startup

1. Activate virtual environment:

```bash
call setup_env.bat
```

2. Run the app:

```bash
python iot_app/app/main.py
```

---

## 👥 Contributors

- **Itay Vazana** – [GitHub](https://github.com/ItayVazana1) | [LinkedIn](https://www.linkedin.com/in/itayvazana/)
- **Omer Trabulski** – [GitHub](https://github.com/OmerTrb) | [LinkedIn](https://www.linkedin.com/in/omer-trabulski-73b374264/)

---

## 🎓 Academic Note

This project was developed as part of the **"Software Development for IoT Systems in a Smart City Environment"** course,  
within the **Bachelor’s Degree in Computer Science**.

---

## ✅ Status

- ✅ Fully modular structure
- ✅ Tested on Windows 10 + Docker Desktop
- ✅ MQTT + MySQL integration verified
- ✅ GUI responsive and animated
- ✅ Emulators synchronized with DB and broker

---

## 📬 Questions?

Feel free to open an issue or contact us.

---
