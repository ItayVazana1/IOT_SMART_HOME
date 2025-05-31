# 🧠 UI & Tabs Module – IoT Smart Home

This module contains all the **PyQt5 user interface tabs** that power the GUI of the IoT Smart Home system. It provides dynamic interaction panels for users to control and monitor emulators, view logs, test services, and personalize behavior.

---

## 🧩 Module Overview

| File               | Purpose                                                              |
|--------------------|----------------------------------------------------------------------|
| `dashboard_tab.py` | 📊 Displays system-wide status (MQTT, DB, Emulators) in visual cards |
| `emulators_tab.py` | 🧪 Allows toggling of each emulator and controlling its behavior      |
| `logs_tab.py`      | 📜 Real-time color-coded log viewer with save and clear options      |
| `room_view_tab.py` | 🗺️ Visual map of the room showing active devices and live readings   |
| `settings_tab.py`  | ⚙️ App controls for DB, MQTT reconnection, exit and credits          |
| `theme.py`         | 🎨 Centralized colors, font sizes, spacing, and font utilities       |

---

## 🖥 Tabs Breakdown

### 📊 `DashboardTab`
Displays **real-time system status** using styled info cards:
- MQTT: Connected / Disconnected
- DB: Synced / Failed
- Emulators: Count of active ones

Each card uses a different color banner to reflect status.

---

### 🧪 `EmulatorsTab`
Grid-based control panel:
- Each emulator (DHT, Light, Motion, Relay, Button) has its own card.
- Start/Stop buttons (Relay, DHT, etc.).
- Press behavior (Button emulator).
- Cards adapt layout responsively based on window size.

---

### 📜 `LogsTab`
Live log console with:
- Color-coded severity (INFO = green, ERROR = red, etc.).
- Timestamped entries.
- `Clear` and `Save to File` buttons, disabled until logs exist.
- Connected to the centralized `Loguru` logger via a custom sink.

---

### 🗺️ `RoomViewTab`
Dual-panel layout:
- Left: Device status labels with bold readings.
- Right: Grid layout of visual “device boxes” (green = active, dark = inactive).
- Devices: Doorbell, Light, Motion, DHT, Relay.
- Special animations for doorbell press duration.
- Auto-refresh every 500ms.

---

### ⚙️ `SettingsTab`
- Reconnect to MQTT with popup feedback
- Test DB connection (with success/failure dialogs)
- App exit with confirmation
- Developer credits shown at the bottom

---

## 🎨 `theme.py`
Global design variables:
- `COLORS`: For background, border, highlights, etc.
- `FONT_SIZES`: Keywords mapped to integer point sizes
- `SIZES`: UI spacing, button width, and corner radius
- `get_font(...)`: Utility function for styled fonts (e.g., `get_font("title", bold=True)`)

---

## 📦 Dependencies
This UI layer depends on:
- PyQt5
- Loguru
- The main manager/controller logic to pass emulator states and data

---

## 💡 Tips
- You can dynamically inject new emulators into the GUI if the manager structure stays consistent.
- Extend theme variables for new colors or styles in one place.

---