# 📐 IoT Smart Home – System Architecture Overview

This document presents a comprehensive technical overview of the **IoT Smart Home** project — a fully modular simulation platform for emulated smart devices, real-time messaging, and persistent data logging. The system is structured into 7 clear architectural layers, each responsible for distinct aspects of the logic, communication, and UI.

---

## 🔁 Layer 1: System Coordinator (Main Control Layer)

This is the **orchestration center**. The file `main.py` initializes the entire runtime by constructing the PyQt5 GUI, setting up connections to the MQTT broker and MySQL database, and passing all service references to GUI tabs.

- `mqtt_listener.py`: Listens for MQTT messages and dispatches updates to the `RoomViewTab`.
- `emulators_manager.py`: Creates and manages instances of each emulator, offering a centralized interface for other components to interact with devices.

All GUI tabs and backend clients are initialized in a structured countdown and startup sequence from within `MainWindow`.

---

## 🤖 Layer 2: Device Emulation Engine

The **emulation layer** is responsible for mimicking hardware devices like sensors and actuators. It is built upon a shared base class, `BaseEmulator`, which abstracts common functionality such as:

- Periodic or manual activation (via QTimer or user interaction)
- MQTT publishing (`Home/<device_type>`)
- Logging to the database with timestamped readings

**Emulators included:**
- `DHTEmulator` – emits temperature and humidity (every 5s)
- `LightEmulator` – emits light levels (every 2s)
- `MotionEmulator` – randomly emits motion detection events (every 3s)
- `RelayEmulator` – manually toggled, emits ON/OFF
- `ButtonEmulator` – press-triggered, auto-resets after 7s

All emulators support centralized control through the `EmulatorsManager`.

---

## 📡 Layer 3: Communication & Persistence (MQTT & DB)

This layer powers **real-time messaging** and **data durability**.

- `mqtt_client.py`: Connects to a local Mosquitto broker, subscribes to `Home/#`, publishes values, and relays messages to the main GUI logic.
- `db_client.py`: Connects to MySQL (`localhost:3307`), supports inserts, queries, and health checks. Compatible with `mysql_native_password` plugin.

MQTT and DB clients are fully decoupled, supporting reconnection logic and error handling.

---

## 🖥️ Layer 4: User Interface Layer (PyQt5 Tabs)

The GUI provides **visual monitoring and control** over the system via five modular tabs:

- `DashboardTab`: Status indicators for MQTT, DB, and emulators
- `EmulatorsTab`: Start/stop/press controls for each device
- `RoomViewTab`: Visual layout with color-coded indicators and animations
- `LogsTab`: Live log view from Loguru (INFO, WARNING, ERROR)
- `SettingsTab`: Allows reconnecting to services, testing DB, and exiting the app

All tabs are themed using a shared design system (`theme.py`) with centralized sizing and color constants.

---

## 🪵 Layer 5: Logging Infrastructure

The system uses **Loguru** for unified logging:

- Colored console logs
- Timestamped and categorized rolling file logs (`sys_logs/`, compressed weekly)
- Optional GUI sink integration that streams logs into the `LogsTab` via `add_gui_sink(...)`

Every critical component logs state transitions, warnings, errors, and connection events.

---

## ⚙️ Layer 6: Configuration Layer (MQTT + MySQL)

This layer defines runtime configuration for backend services, fully containerized in Docker:

**Mosquitto Broker:**
- Configured with persistence enabled and full debug logging to stdout
- Listeners on ports 1883 (MQTT) and 9001 (WebSocket)
- Anonymous access allowed for development

**MySQL Database:**
- Schema and user bootstrapped via `init.sql`
- `iot_data.device_data` stores all emulator readings
- Enforced use of `mysql_native_password` via `my.cnf` to support Python connectors
- Manual reset instructions documented (`mysql_native_password_fix_guide.txt`)

---

## 🚀 Layer 7: Deployment & Environment Operations

**Batch Scripts:**
- `docker-compose.yml`: Launches `mosquitto` and `mysql` with persistent volumes
- `setup_env.bat`: Initializes Python `venv` and installs dependencies
- `run_app.bat`: Activates environment and launches `main.py`
- `clean_env.bat`: Clears logs, Docker volumes, and resets app state

These scripts ensure easy startup for new users and a repeatable local dev experience.

---

## ✅ End-to-End System Flow

1. **Start the backend**:
   ```bash
   docker-compose up -d
   ```

2. **Launch the frontend app**:
   ```bash
   run_app.bat
   ```

3. **Interact with devices** using the Emulators tab.
4. **Monitor statuses** via Dashboard and Room View.
5. **Watch logs** as they stream live in the Logs tab.
6. **Reconnect services or exit** via the Settings tab.

---

## 🧩 Summary

This architecture offers:

- 💡 **Modular Design** – Each layer is independent yet integrated
- 🌐 **Real-Time Communication** – Fully asynchronous device events via MQTT
- 🧠 **Virtual Hardware** – Emulators enable dev/testing with no physical sensors
- 📊 **Persistent Storage** – All readings are stored in a queryable SQL database
- 🎨 **Live GUI Monitoring** – PyQt5 interface shows real-time updates and logs

> The result: a robust, extensible, and fully containerized IoT simulation platform.