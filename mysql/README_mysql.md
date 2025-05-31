# 🗄️ MySQL in the IoT Smart Home Project

This module configures and integrates a **MySQL 8.0** database for storing sensor data in the IoT Smart Home system. It is designed to work seamlessly inside a Docker container, alongside the Mosquitto broker and GUI app.

---

## 🧩 Role in the System

MySQL serves as the **persistent backend** for logging all sensor/emulator activity. It allows:

- ✅ Storing time-series sensor readings from emulators
- 📊 Querying recent activity for visual or analytics purposes
- 🔄 Integration with GUI (via `DBClient`) to allow live inserts, tests, and fetches

---

## 📁 Data Model

The database is automatically initialized using the `init.sql` script. It creates:

### 🔸 Database: `iot_data`

### 🔸 Table: `device_data`
| Column       | Type         | Description                     |
|--------------|--------------|---------------------------------|
| `id`         | `INT`        | Auto-incrementing primary key   |
| `device_type`| `VARCHAR(50)`| Device name (e.g. `dht`, `light`) |
| `value`      | `TEXT`       | Sensor reading or payload       |
| `timestamp`  | `DATETIME`   | Defaults to `CURRENT_TIMESTAMP` |

---

## 👤 Authentication Fix (mysql_native_password)

By default, MySQL 8 uses `caching_sha2_password`, which is **incompatible with `mysql-connector-python`** used by this project.

To fix this, the project:

- Creates the user `iotuser` with the **legacy plugin** `mysql_native_password`
- Ensures full privileges on `iot_data`
- Applies the fix automatically via `init.sql`

If needed manually, follow this:
```sql
ALTER USER 'iotuser'@'%' IDENTIFIED WITH mysql_native_password BY 'iotpass';
FLUSH PRIVILEGES;
```

> 💡 You can verify the plugin with:
> ```sql
> SELECT user, host, plugin FROM mysql.user;
> ```

---

## ⚙️ Docker Integration

The database container is configured in `docker-compose.yml` and includes:

- 📦 `mysql:8.0` base image
- 📄 Mounted `init.sql` for auto-setup
- 🔐 Root password: `rootpass`
- 👤 User: `iotuser` / `iotpass`
- 🛠 `my.cnf` override file to enforce plugin defaults:
  ```ini
  [mysqld]
  default_authentication_plugin = mysql_native_password
  ```

---

## 📂 Volumes & Persistence

The DB state is persisted using Docker volumes:

```yaml
volumes:
  db_data:  # ↳ persists MySQL data across runs
```

To wipe/reset the database, remove the volume:

```bash
docker volume rm yourprojectname_db_data
```

---

## 🧪 Testing the Connection

You can validate the DB connection via:

- GUI Settings Tab → "Test Connection" ✅
- Logs show insert success/failure 🔍
- Use Adminer UI at [http://localhost:8080](http://localhost:8080) for browsing data

---

## ✅ Summary

| Feature                    | Status |
|---------------------------|--------|
| Auto DB setup via `init.sql` | ✅     |
| Password plugin fix         | ✅     |
| Dockerized & persistent     | ✅     |
| GUI + programmatic access   | ✅     |

---