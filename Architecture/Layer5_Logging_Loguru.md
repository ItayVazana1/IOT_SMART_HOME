# 🪵 Part 5 – Logging System with Loguru

## 📄 File: `logger.py`

Provides a unified logging infrastructure across the entire system:
✔️ Colorful console output  
✔️ Systematic log file creation  
✔️ Integration with GUI (`LogsTab`)

---

## 📦 Configuration

### Log Directory:
```python
LOG_DIR = "sys_logs"
```

### File Naming:
```
2025-06-02_12-47-00.log
```
Generated using timestamp format.

---

### Console Handler:
- Displays colored logs with:
  - Timestamp
  - Log level (INFO, WARNING, ERROR)
  - Caller info
  - Message body

### File Handler:
- Rotation: `1 week`
- Retention: `2 weeks`
- Compression: `.zip`

---

### GUI Sink:
```python
def add_gui_sink(gui_callback)
```
- Sends logs directly into the `LogsTab` via `QTextEdit`
- Hooked into the GUI using:
```python
add_gui_sink(self._loguru_sink)
```

---

## 🔄 Full Log Flow

```
[ Any module ]
     ↓  logger.info(...) / warning() / error()
         ↓
     → Console (colored output)
     → Rolling log file (compressed weekly)
     → LogsTab (if GUI is active)
```

---

## 🖥️ Integration in LogsTab

- Each incoming message is passed to:
```python
_loguru_sink(message)
```
- Parsed to identify level:
  - INFO
  - WARNING
  - ERROR
- Displayed in `QTextEdit` with timestamp and styled color

---

## ✅ Logging Capabilities Summary

| Feature                  | Supported |
|--------------------------|-----------|
| Console color output     | ✔️        |
| Log to file              | ✔️        |
| Rotation + compression   | ✔️        |
| Live GUI log view        | ✔️        |
| Multiple log levels      | ✔️        |