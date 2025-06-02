# 🤖 Part 2 – Emulators Architecture

## 🧱 Shared Base: `BaseEmulator`

All emulators in the project inherit from the `BaseEmulator` class, which provides:

- 🎯 State management (`turn_on` / `turn_off`)
- ⏲️ Internal timer using `QTimer` for periodic polling
- 📡 MQTT publishing via `publish()`
- 🗄️ Database logging via `save_to_db()`
- 🧱 Topic definition: `Home/<device_type>`

---

## ⚙️ Core Operation Logic (base_emulator.py)
```python
# Every X milliseconds (based on interval_ms), the emulator runs:
self.generate_value()
self.publish()
self.save_to_db()
```

### 🧠 Key Methods:
- `turn_on()` → Starts the timer and triggers the first data point
- `turn_off()` → Stops timer, resets value, and publishes to MQTT
- `publish()` → Sends the current value to the MQTT broker
- `save_to_db()` → Logs the value with timestamp to the database

---

## 🧪 Actual Emulators and Their Behavior

### 🌡️ DHTEmulator
- Generates random temperature & humidity every 5 seconds
- Output format (JSON):
```json
{"temperature": "24.1 °C", "humidity": "51.0 %"}
```

### 💡 LightEmulator
- Sends light intensity values (0–1000 lx) every 2 seconds
- Example payload: `"723 lx"`

### 🧍 MotionEmulator
- Every 3 seconds: 80% chance `"motion detected"`, 20% `"no motion"`
- Simulates basic random motion behavior

### 🔌 RelayEmulator
- No polling (interval = 0)
- Controlled manually via `turn_on()` / `turn_off()`
- Publishes `"1"` for ON and `"0"` for OFF

### 🔔 ButtonEmulator
- Also doesn't poll periodically
- On `press()` (e.g., from GUI button):
  - Publishes `"pressed"`
  - Resets automatically after 7 seconds
  - Triggers pulse animation in Room View

---

## 🔄 Motion Sensor Example Flow

1. `motion_emulator.generate_value()` picks `"motion detected"`
2. Publishes to MQTT topic `Home/motion`
3. `MQTTListener` receives the message and routes it to `RoomViewTab`
4. `RoomViewTab` updates the "motion" box to green with the reading
5. Value is logged into the `device_data` table in the MySQL database

---

## 🎯 Purpose of This Layer

- Provides a **realistic hardware substitute** for development and testing
- Builds a **controlled test environment** for GUI, MQTT, and DB
- Enables both **manual and automatic control** over emulator behavior

---

## ✅ Summary Table

| Emulator | Polling Frequency | Sample Output         | MQTT | DB  |
|----------|-------------------|------------------------|------|-----|
| DHT      | Every 5 seconds   | JSON (temp + humidity) | ✔️   | ✔️  |
| Light    | Every 2 seconds   | `"723 lx"`             | ✔️   | ✔️  |
| Motion   | Every 3 seconds   | `"motion detected"`    | ✔️   | ✔️  |
| Relay    | Manual only       | `"1"` / `"0"`          | ✔️   | ✔️  |
| Button   | On press          | `"pressed"` → `"idle"` | ✔️   | ✔️  |