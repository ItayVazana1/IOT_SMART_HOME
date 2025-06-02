# 🧠 Part 1 – Main Controller Architecture

## 🎛 Involved Components

| File                  | Description |
|------------------------|-------------|
| `main.py`              | Main entry point, initializes the GUI, sets up MQTT and MySQL connections |
| `mqtt_listener.py`     | Parses incoming MQTT messages and updates the Room View accordingly |
| `emulators_manager.py` | Manages all emulators — creates, stores, and provides unified access to them |

---

## 🚀 Execution Flow

### 🟢 Step 1: Launching the GUI
```python
if __name__ == "__main__":
    run_gui()
```
Runs the `MainWindow()` instance using PyQt5.  
This initializes the entire GUI interface.

---

### 🟡 Step 2: Countdown and Pre-connection
```python
self._start_connection_countdown()
```
After a 3-second countdown:
- Creates `MQTTClient`, `DBClient`, and `EmulatorsManager`
- Waits 1.5 seconds and then calls `self._finalize_tabs()`

---

### 🔵 Step 3: Connection and Tab Finalization
```python
self._finalize_tabs()
```
- Calls `db.connect()` and `mqtt.start()`
- Verifies DB and MQTT connectivity
- Replaces placeholder tabs with functional ones:
  - `DashboardTab`, `EmulatorsTab`, `RoomViewTab`, `LogsTab`, `SettingsTab`
- Creates the `MQTTListener` which routes messages to `RoomViewTab`

---

## 📡 MQTT Message Routing – from `mqtt_listener.py`
```python
def route_message(self, topic, payload):
```
- Listens for topics of the form `Home/<type>`
- Based on `<type>`, decides how to update:

| Type | Behavior |
|------|----------|
| `dht` | Parses JSON with temperature and humidity, forwards to Room View |
| `light` / `motion` | Displays value and active status |
| `button` | Triggers pulse animation in Room View |
| `relay` | Displays ON/OFF state |

- On error: logs a warning

---

## 🤖 Emulators Management – from `emulators_manager.py`
```python
self.emulators = {
    "button": ButtonEmulator(...),
    "dht": DHTEmulator(...),
    ...
}
```
- All emulators are initialized with MQTT and DB clients
- Accessible via `get("light")`, `get("relay")`, etc.
- Central access point across the codebase and GUI

---

## 📊 Sample Interaction Flow

1. `DHTEmulator` publishes to MQTT (`Home/dht`)
2. `MQTTListener` receives and parses the message
3. `RoomViewTab` updates the visual box with new data
4. Simultaneously, `DHTEmulator` logs the value to the database via `DBClient`

---

## 📌 Summary

- `main.py` = Central orchestrator for GUI, MQTT, and DB
- `mqtt_listener.py` = Bridges incoming MQTT data to the GUI
- `emulators_manager.py` = Central registry for emulator instances used across the app