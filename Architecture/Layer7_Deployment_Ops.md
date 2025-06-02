# ⚙️ Part 7 – Operational Layer: Deployment & Execution

---

## 🧱 Key Operation Components

| File              | Purpose |
|-------------------|---------|
| `docker-compose.yml` | Launches MySQL and Mosquitto services via Docker |
| `run_app.bat`        | Starts the GUI (includes virtual environment activation) |
| `setup_env.bat`      | Loads virtual environment, installs dependencies |
| `clean_env.bat`      | Cleans logs, cache, Docker volumes if needed |

---

## 🐳 Docker Compose Overview

### Services Launched:
- **MySQL**
  - Port: `3307`
  - Credentials: `iotuser` / `iotpass`
  - Uses `init.sql` and `my.cnf` (forces `mysql_native_password`)
  - Root password protected: `rootpass`
  - Volume: `db_data` for persistent storage

- **Mosquitto (MQTT Broker)**
  - Ports: `1883` (MQTT), `9001` (WebSocket)
  - Config: Anonymous access and full logging
  - Volume: `/mosquitto/data`

---

## 🖥️ Running the Application

### ▶️ Step 1: Start Docker Services
```bash
docker-compose up -d
```
- Launches Mosquitto and MySQL in background

---

### ▶️ Step 2: Launch the GUI
```bash
run_app.bat
```
- Calls `setup_env.bat`
- Loads virtual environment (venv)
- Starts `main.py` with all dependencies

---

### 🔄 Step 3 (Optional): Clean Environment
```bash
clean_env.bat
```
- Deletes logs, temp files, and DB volumes
- Used to reset the development state

---

## 📁 Supporting Scripts

### `setup_env.bat`
- Loads or creates a Python `venv`
- Installs `requirements.txt`
- Automatically launches the application at the end

### `run_app.bat`
```bat
call setup_env.bat
```

---

## ✅ Summary – System Operations

| Step              | Command / File     | Outcome                            |
|-------------------|--------------------|------------------------------------|
| Launch Services   | `docker-compose up -d` | Mosquitto + MySQL running locally  |
| Run App           | `run_app.bat`      | Starts the PyQt5 GUI               |
| Clean Environment | `clean_env.bat`    | Resets development environment     |
| First-time Setup  | `setup_env.bat`    | Installs dependencies + venv setup |