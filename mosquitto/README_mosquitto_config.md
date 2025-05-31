# 🐝 Mosquitto Configuration – Explained

This file configures the Eclipse Mosquitto MQTT broker for use in development or local Docker environments.  
It defines how messages are stored, how logs are handled, and which ports are open for both TCP and WebSocket communication.

---

## 📦 Persistence Configuration

- `persistence true`  
  Enables persistent message storage. This ensures retained messages and session data survive broker restarts.

- `persistence_location /mosquitto/data/`  
  Sets the directory where the broker saves its persistent data (used inside the container).

---

## 📝 Logging Configuration

- `log_dest stdout`  
  Sends all broker logs to the standard output stream — ideal for observing logs in real time inside Docker.

- `log_type all`  
  Enables logging for all types of messages, including `error`, `notice`, `info`, and `debug`.

---

## 🔌 MQTT Listener (TCP)

- `listener 1883`  
  Opens port **1883** for incoming standard MQTT connections over TCP.

- `protocol mqtt`  
  Specifies that this listener handles MQTT over traditional TCP.

---

## 🌐 WebSocket Listener

- `listener 9001`  
  Opens port **9001** for MQTT clients that connect using WebSockets (e.g., web browsers or dashboard UIs).

- `protocol websockets`  
  Tells Mosquitto to expect WebSocket-based MQTT messages on this port.

---

## 🔓 Security Settings

- `allow_anonymous true`  
  Allows connections **without authentication**.  
  ⚠️ This is **not secure for production** — it's okay for testing but highly recommended to set to `false` and configure a password file (`password_file`) in real deployments.

---

## ✅ Summary

| Feature        | Enabled | Notes                          |
|----------------|---------|--------------------------------|
| Persistence    | ✅       | Messages survive restarts      |
| Logging        | ✅       | Full verbosity to stdout       |
| TCP MQTT Port  | 1883    | Standard clients               |
| WebSocket Port | 9001    | For web-based MQTT connections |
| Anonymous Auth | ✅       | ⚠️ Not safe for production use |

---

> 📌 Tip: To harden your setup, consider:
> - `allow_anonymous false`
> - `password_file /mosquitto/config/passwords.txt`
> - Enabling TLS (`cafile`, `certfile`, `keyfile`)