# 🪵 Logger Module – IoT Smart Home

### 📁 File: `logger.py`  
### 🗓️ Last Updated: May 31, 2025  
### 🧠 Purpose: Provide consistent, color-coded logging across the entire application using Loguru.

---

## 🧰 Overview

This module sets up a **centralized logger** for the entire Smart Home system. It ensures all important messages—whether from MQTT, database, GUI, or emulators—are logged in both the terminal **(with colors 🎨)** and a **rotating log file 📂**. Optionally, it also supports pushing logs live into the PyQt5 GUI (🖥️).

---

## 📌 Features

✅ **Colorful console output** with timestamps, levels, file & function info  
✅ **Daily log files** saved to `sys_logs/`, with auto-rotation and compression  
✅ **Custom log sink** for pushing messages into GUI widgets like `QTextEdit`  
✅ **Safe initialization** (removes duplicate handlers to avoid spam)

---

## 🛠️ How It Works

### 🔁 File Setup

```python
LOG_DIR = "sys_logs"
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = os.path.join(LOG_DIR, f"{timestamp}.log")
```

- Logs are saved under the `sys_logs/` directory.
- Each run generates a new file like `2025-05-31_21-47-12.log`.

---

### 🎨 Console Logging

```python
logger.add(sys.stdout, ...)
```

- Colored format: shows `time`, `level`, `file:function:line`, and `message`.
- Helps in debugging while running the GUI or backend.

---

### 📁 File Logging

```python
logger.add(log_file, rotation="1 week", retention="2 weeks", compression="zip", ...)
```

- Rotates every week 🗓️
- Keeps logs for 2 weeks ♻️
- Archives old logs in `.zip` format for storage efficiency 📦

---

### 🪟 GUI Logging

```python
def add_gui_sink(gui_callback):
    logger.add(gui_callback, format="{level.icon} [{level}] {message}", level="INFO")
```

- Allows real-time log updates in the Logs tab of the GUI
- The `gui_callback` typically points to something like `QTextEdit.append`

---

## 🚀 Example Usage

```python
from iot_app.app.utils.logger import logger

logger.info("System started successfully!")
logger.warning("Low light level detected")
logger.error("Database connection failed")
```

---

## 📎 Dependencies

- [Loguru](https://github.com/Delgan/loguru) — simple, powerful logging library  
📦 `pip install loguru`