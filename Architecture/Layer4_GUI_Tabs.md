# 🖥️ Part 4 – GUI Layer (PyQt5 Tabs)

## 📌 Main Tabs Overview

| Tab        | File              | Description                                               |
|------------|-------------------|-----------------------------------------------------------|
| Dashboard  | `dashboard_tab.py`| Displays general status of MQTT, DB, and Emulators       |
| Emulators  | `emulators_tab.py`| Control panel for starting/stopping/pressing emulators   |
| Room View  | `room_view_tab.py`| Graphical layout with visual device indicators            |
| Logs       | `logs_tab.py`     | Live logs with color-coded levels, clear/save actions     |
| Settings   | `settings_tab.py` | MQTT/DB reconnection, test buttons, exit, and credits     |

---

## 🧩 Integration with Logic

Each tab receives references to:
- `db_client`
- `mqtt_client`
- `emulators_manager` (if relevant)

Calls such as `turn_on()` or `insert_sensor_data()` are routed via these references, all initialized in `MainWindow`.

---

## 📊 DashboardTab

Displays three status cards:
- MQTT
- DB
- Emulators

Runs `update_status()` every 30 seconds:
- Calls `test_connection()` on MQTT and DB clients
- Shows status using colored labels

---

## 🧪 EmulatorsTab

Each emulator is displayed with:
- Icon + Label
- Start/Stop or Press button (for Button)

Each button triggers:
```python
self.manager.get(...).turn_on()
self.manager.get(...).press()
```

### 📐 Responsive Design
- Automatically adjusts the number of columns (2 or 3) based on window width

---

## 🗺️ RoomViewTab

Split into two panels:
- **Left**: Textual status and latest values
- **Right**: Grid-based layout of device boxes

Updates come from:
```python
MQTTListener.route_message(...)
```

### Visual Mapping:
- `"motion detected"` → green
- `"OFF"` → dark gray

Includes 7-second doorbell animation via:
```python
pulse_doorbell()
```

---

## 📜 LogsTab

- Based on `QTextEdit`
- Connected to Loguru via `add_gui_sink()`
- Recognizes `[INFO]`, `[WARNING]`, `[ERROR]` and colors accordingly

Buttons:
- 🧹 `Clear Logs`
- 💾 `Save to File`

---

## ⚙️ SettingsTab

- Displays current MQTT and DB info
- Reconnect button:
```python
self.mqtt.reconnect()
```
- Test DB button:
```python
self.db.test_connection()
```
- Exit button with confirmation dialog

---

## 🎨 Theme (theme.py)

Centralized design constants:
- `COLORS` – background, text, highlight, etc.
- `FONT_SIZES`, `SIZES` – padding, margins, button sizes
- `get_font(...)` – returns a consistent styled QFont object

---

## 🔄 Reminder: Data Flow

```text
Emulator → MQTT → GUI
```

1. Emulator sends value to MQTT
2. `MQTTClient` triggers callback
3. `MainWindow` forwards it to `MQTTListener`
4. `MQTTListener.route_message()` parses and updates
5. `RoomViewTab.update_device_state(...)` visually displays the result

---

## ✅ Summary

- Core logic (MQTT, DB) is integrated into the interface
- GUI built with modular, themed tabs
- Realtime visual updates and developer utilities in place