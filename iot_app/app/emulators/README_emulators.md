
# 🤖 Emulators Module – IoT Smart Home

Welcome to the **Emulators Module** of the IoT Smart Home system! This module simulates smart home devices (sensors and actuators) and handles:

- ✅ MQTT communication  
- ✅ Database logging  
- ✅ Periodic polling (for sensors)  
- ✅ ON/OFF control (for actuators)

It provides a realistic and testable environment for the frontend and backend systems without requiring physical devices.

---

## 📁 File Structure

| File                  | Description                                  |
|-----------------------|----------------------------------------------|
| `base_emulator.py`    | Abstract base class for all emulators        |
| `button_emulator.py`  | Doorbell button emulator                     |
| `dht_emulator.py`     | DHT sensor (temperature & humidity)          |
| `light_emulator.py`   | Ambient light sensor                         |
| `motion_emulator.py`  | Motion detector simulator                    |
| `relay_emulator.py`   | Binary actuator switch (relay)               |

---

## 🧠 Architecture

All emulators inherit from `BaseEmulator`, which defines:

- `turn_on()` / `turn_off()` for activation
- `generate_value()` for simulating sensor readings
- `build_payload()` for sending MQTT messages
- `publish()` and `save_to_db()` built-in

Each emulator runs independently and updates periodically based on a configurable timer.

---

## 🧪 Included Emulators

### 🔔 Button Emulator (`button_emulator.py`)
- Simulates a doorbell press.
- Publishes "pressed" once and resets after 7 seconds.
- Controlled manually (no polling).

### 🌡️ DHT Emulator (`dht_emulator.py`)
- Simulates temperature (18–32°C) and humidity (30–90%).
- Publishes JSON-formatted payload.
- Runs every 5 seconds.

### 💡 Light Emulator (`light_emulator.py`)
- Simulates ambient brightness (0–1000 lx).
- Runs every 2 seconds.
- Outputs raw value as string (`e.g., "720 lx"`).

### 🧍 Motion Emulator (`motion_emulator.py`)
- Randomly detects motion:
  - 80% chance: "motion detected"
  - 20% chance: "no motion"
- Runs every 3 seconds.

### 🔌 Relay Emulator (`relay_emulator.py`)
- Binary switch (ON/OFF).
- Controlled manually using `turn_on()` / `turn_off()`.
- Publishes `"1"` or `"0"` as payload.

---

## 🔗 MQTT Topics

Each emulator publishes to the topic format:

```
Home/<device_type>
```

For example:
- `Home/dht`
- `Home/motion`
- `Home/relay`

---

## 💾 Database Integration

Each emulator logs its state changes and sensor values to a MySQL database using `insert_sensor_data()` from the `DBClient`.

Fields stored:
- `device_type`
- `value`
- `timestamp`

---

## 🛠️ Example Usage

```python
dht = DHTEmulator(mqtt_client, db_client)
dht.turn_on()  # Starts generating and publishing data every 5 seconds

relay = RelayEmulator(mqtt_client, db_client)
relay.turn_on()  # Publishes "1" and logs it
relay.turn_off()  # Publishes "0" and logs it
```

---

## 📦 Extending

To add a new emulator:
1. Create a subclass of `BaseEmulator`.
2. Implement `generate_value()` and `build_payload()`.
3. Set `interval_ms` appropriately.
4. Register it in your emulator manager.
