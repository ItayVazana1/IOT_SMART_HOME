# 🧠 Main Controller & MQTT Listener – *IoT Smart Home*

### 📂 Includes:
- `main.py`
- `mqtt_listener.py`
- `emulators_manager.py`

---

## 🚀 Overview

This group forms the **central control logic** of the *IoT Smart Home* system. It governs the initialization of GUI components, manages emulators, and routes real-time MQTT messages to update visual interfaces.

---

## 📁 Components

### 1. `main.py` – 🖥️ **Main Application Launcher**
This is the **entry point** for the PyQt5-based GUI. It:
- Initializes and displays all GUI tabs (`Dashboard`, `Emulators`, `Logs`, `Room View`, `Settings`)
- Manages the **MQTT and MySQL connections**
- Shows a visual **status bar** with ping timers and live connection state
- Periodically performs **health checks**
- Handles MQTT message routing through the `MQTTListener`

🔁 Automatic ping and countdown timers ensure a constantly updated interface.

### 2. `mqtt_listener.py` – 📡 **Real-Time MQTT Router**
This class listens for all incoming MQTT messages (on `Home/#` topics) and:
- Validates and parses the topic and payload
- Dynamically updates the `RoomViewTab` with the correct visual and textual indicators
- Supports sensors like:
  - 🌡️ DHT (temperature + humidity)
  - 💡 Light intensity
  - 🧍 Motion detection
  - 🔔 Button (triggers blinking pulse)
  - 🔌 Relay (on/off)

It smartly separates **data routing** from business logic, helping maintain clarity and scalability.

### 3. `emulators_manager.py` – 🧪 **Emulator Factory & Accessor**
This file:
- Creates and stores all emulator instances (`DHT`, `Light`, `Motion`, `Relay`, `Button`)
- Provides a `get()` method to access emulators by their key (like `'light'`, `'relay'`, etc.)
- Ensures all emulators share the same DB and MQTT clients

💡 Think of this as the **emulator hub**, handling unified access and control.

---

## 📌 Integration Flow

```
        +------------------+           MQTT Payloads          +---------------------+
        |     Sensors      |  ─────────────────────────────▶  |    MQTTListener     |
        | (Emulators Tab)  |                                | (Real-time Parser)   |
        +--------┬---------+                                 +----------┬----------+
                 │                                                       │
                 │                                                       ▼
        +--------▼---------+                                   +--------------------+
        |  MQTTClient.py   |                                   |   RoomViewTab.py   |
        | (paho-mqtt)      |                                   | (UI Visualization) |
        +------------------+                                   +--------------------+
```

---

## ✅ Features Summary

| Feature                         | Description                                 |
|----------------------------------|---------------------------------------------|
| 🌐 Full MQTT integration         | Listens on `Home/#`, supports publish/recv  |
| 🏠 Tab-based GUI structure       | All tabs loaded dynamically after init      |
| 🧠 Separation of concerns        | `main.py`, `emulators_manager`, `listener`  |
| 📡 Listener logic                | JSON parsing, topic routing, UI control     |
| 🔄 Periodic ping + status bar    | Keeps user informed of system health        |