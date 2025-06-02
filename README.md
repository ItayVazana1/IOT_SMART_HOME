# 🏡 IoT Smart Home System

A full-stack **IoT simulation platform** built with Python, MQTT, MySQL, and PyQt5.  
Simulates smart devices, visualizes real-time events, logs data persistently, and provides a modular GUI for user interaction.

---

## 📌 Project Overview

This smart home system includes:

- 🧠 Emulators for common devices (DHT, light sensor, motion, button, relay)
- 💬 MQTT communication via Mosquitto (Docker)
- 🗄️ MySQL database with persistent inserts and live logging
- 🖥️ GUI (PyQt5) with dashboards, device grid, animated indicators, and real-time logs
- 🐳 Dockerized infrastructure for local deployment

---

## 📐 System Architecture

The system is divided into **7 architectural layers**, each with a clear role:

| Layer | Role |
|-------|------|
| **1** | Main controller & orchestration (main.py + managers) |
| **2** | Device emulation engine (sensors/actuators) |
| **3** | Communication & persistence (MQTT + MySQL) |
| **4** | User interface via modular PyQt5 tabs |
| **5** | Logging infrastructure (Loguru + GUI sink) |
| **6** | Configuration (Mosquitto, MySQL settings) |
| **7** | Runtime & deployment (Docker, scripts) |

See full documentation: [`IoT_Smart_Home_Architecture.md`](IoT_Smart_Home_Architecture.md)

---

## 🧱 Folder Structure

```
iot_app/
├── app/
│   ├── core/              # MQTT + DB clients
│   ├── emulators/         # Emulated device classes
│   ├── ui/                # PyQt5 tabs + GUI theme
│   ├── utils/             # Loguru logger
│   ├── emulators_manager.py
│   ├── mqtt_listener.py
│   └── main.py
├── requirements.txt
mosquitto/
├── config/                # mosquitto.conf
mysql/
├── init.sql               # Schema + user bootstrap
├── my.cnf                 # Enforces mysql_native_password
├── mysql_native_password_fix_guide.txt
```

---

## 🧪 Module Breakdown

### 🔁 Emulators (`iot_app/app/emulators`)
Each emulator simulates a real device:

| Device  | Frequency     | Output Format             |
|---------|---------------|---------------------------|
| DHT     | Every 5 sec   | `{temperature, humidity}` |
| Light   | Every 2 sec   | `"723 lx"`                |
| Motion  | Every 3 sec   | `"motion detected"`       |
| Button  | On click      | `"pressed"` → `"idle"`    |
| Relay   | Manual        | `"1"` / `"0"`             |

All inherit `BaseEmulator`:
- MQTT publishing
- MySQL logging
- Timer or manual triggers

### 💬 Core Services (`iot_app/app/core`)
- `MQTTClient`: Manages pub/sub to `Home/#` + callbacks + reconnects
- `DBClient`: Inserts, tests, and fetches records from MySQL

### 🎛 Main Controllers (`iot_app/app`)
- `main.py`: Launches GUI and services
- `emulators_manager.py`: Central registry for all emulators
- `mqtt_listener.py`: Routes MQTT messages to `RoomViewTab`

### 🖥️ UI Tabs (`iot_app/app/ui`)
| Tab         | Purpose                              |
|-------------|--------------------------------------|
| Dashboard   | System health (MQTT, DB, Emulators)  |
| Emulators   | Control buttons per emulator         |
| Room View   | Grid with live device indicators     |
| Logs        | Real-time log console (Loguru)       |
| Settings    | Reconnect, test DB, and exit         |

### 📚 Logging (`iot_app/app/utils/logger.py`)
- Color-coded console + rolling files (weekly zip)
- `add_gui_sink()` routes logs into GUI view

---

## 🐳 Docker Setup

To start backend services:

```bash
docker-compose up -d
```

- Mosquitto: `localhost:1883` (MQTT), `localhost:9001` (WebSocket)
- MySQL: `localhost:3307`
- Adminer: `localhost:8080`

---

## 🖥 GUI Startup

```bash
call setup_env.bat
```
This script will:
- Create virtualenv if missing
- Install dependencies

```bash
call run_app.bat
```

This script:
- Launches the GUI (`main.py`)

To clean/reset environment:

```bash
call clean_env.bat
```

---

## 👥 Contributors

- **Itay Vazana** – [GitHub](https://github.com/ItayVazana1)
- **Omer Trabulski** – [GitHub](https://github.com/OmerTrb)

---

## 🎓 Academic Note

Developed as part of the **"Software Development for IoT Systems in a Smart City Environment"**  
in the **Computer Science B.Sc.** program.

---

## ✅ Status

- ✅ Modular architecture (7 layers)
- ✅ Fully simulated devices
- ✅ MQTT + MySQL integration
- ✅ Dockerized & reproducible setup
- ✅ Live GUI control with data logging

---

## 📬 Questions?

Open an issue or contact the team for assistance.