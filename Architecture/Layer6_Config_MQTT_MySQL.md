# 🛠️ Part 6 – System Configuration Layer (MQTT + MySQL)

---

## 🐝 MQTT Configuration (Mosquitto Broker)

### 📄 File: `README_mosquitto_config.md`

Mosquitto runs as a Docker container and is configured for local development use.

### 🧰 Key Settings

| Setting              | Value        | Description |
|----------------------|--------------|-------------|
| `persistence`        | `true`       | Retains messages after broker restart |
| `persistence_location` | `/mosquitto/data/` | Message storage inside the container |
| `log_dest`           | `stdout`     | Logs to `docker logs` |
| `log_type`           | `all`        | Full logging (error, notice, info, debug) |
| `listener (TCP)`     | `1883`       | For Python MQTT clients |
| `listener (WS)`      | `9001`       | For WebSocket-based clients |
| `protocol`           | `mqtt` / `websockets` | Depends on port |
| `allow_anonymous`    | `true`       | No authentication required (development only) ⚠️ |

---

### 📶 Integration with Project

- `MQTTClient` in Python connects to `localhost:1883`
- Docker exposes ports:
```yaml
ports:
  - "1883:1883"
  - "9001:9001"
```
- Authentication is disabled for development:
```python
mqtt.Client(...)
```

---

### 🛠️ Recommended Production Changes

| Recommendation              | Reason |
|-----------------------------|--------|
| `allow_anonymous false`     | Prevents unauthorized access |
| `password_file`             | Enables user-based access control |
| `cafile`, `certfile`, `keyfile` | Secures communication with TLS |
| `log_type error`            | Reduces log noise |

---

### ✅ MQTT Configuration Summary

| Component    | Value / Notes                     |
|--------------|-----------------------------------|
| Broker       | Mosquitto                         |
| Protocols    | MQTT (TCP), WebSocket             |
| Ports        | 1883 (MQTT), 9001 (WS)            |
| Deployment   | Docker container                  |
| Security     | Anonymous access only ⚠️          |
| Logs         | Full debug to STDOUT              |
| Persistence  | Enabled (`persistence = true`)    |

---

## 🗄️ MySQL Configuration

### 📄 Files:
- `README_mysql.md`
- `init.sql`
- `my.cnf`
- `mysql_native_password_fix_guide.txt`

---

### 🧩 Role

MySQL acts as the persistent backend storing:
- Sensor readings (from emulators)
- Historical data for display and analysis in the GUI

---

### 🧰 Schema Definition (`init.sql`)

Automatically creates:
- Database: `iot_data`
- Table: `device_data`
```sql
id (INT, PK)          -- Auto-increment ID
device_type (VARCHAR) -- e.g., dht, light
value (TEXT)          -- The reading
timestamp (DATETIME)  -- Auto-set timestamp
```

Also defines user:
```sql
USER: iotuser
PASS: iotpass
PLUGIN: mysql_native_password
```

---

### 🔐 Authentication Fix

MySQL 8 defaults to `caching_sha2_password`, which may not work with `mysql-connector-python`.  
We use `mysql_native_password` instead to ensure compatibility:
```sql
ALTER USER 'iotuser'@'%' IDENTIFIED WITH mysql_native_password BY 'iotpass';
```

---

### ⚙️ Docker Integration

Uses the `mysql:8.0` image.  
- `init.sql` is mounted and executed on first run
- `my.cnf` enforces the correct auth plugin:
```ini
[mysqld]
default_authentication_plugin = mysql_native_password
```
- Docker Compose volume:
```yaml
volumes:
  db_data:
```

---

### 🧪 Connectivity Testing

- From GUI: `Settings → Test Connection`
- Log entries for `insert` and `ping`
- Via Adminer (browser): `localhost:8080`

---

### 🧰 Manual Fix Guide

File: `mysql_native_password_fix_guide.txt`  
```bash
docker exec -it mysql_db mysql -u root -p
```
```sql
ALTER USER 'iotuser'@'%' IDENTIFIED WITH mysql_native_password BY 'iotpass';
FLUSH PRIVILEGES;
SELECT user, host, plugin FROM mysql.user;
```

---

### ✅ MySQL Configuration Summary

| Feature                         | Status |
|----------------------------------|--------|
| Auto-created schema (`init.sql`) | ✅     |
| `mysql_native_password` plugin   | ✅     |
| GUI + Code Access                | ✅     |
| Docker Deployment                | ✅     |
| Persistent Volume                | ✅     |