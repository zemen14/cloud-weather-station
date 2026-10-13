# ☁️ Cloud Weather Station — ESP32-C3 + Python Server

**An ESP32-C3 that doesn't just sense — it phones home.** Every 15
seconds the board asks a Python server where it is, fetches the live
outdoor temperature for that location from wttr.in, bundles it with
its own sensor reading, and posts a full weather report back to the
server.

```
[ESP32] Location: Santa Cruz, CA
[ESP32] Outdoor temp: +18 C
[ESP32] Sensor temp:  26.40 C
```

```
[2026-10-13 15:42:07] ── Weather Station Report ──
  Location     : Santa Cruz, CA
  Outdoor temp : +18 C
  Sensor temp  : 26.40 C
────────────────────────────────
```

## How it works

1. **ESP32-C3** joins WiFi (event-driven, auto-reconnect) and asks
   the server `GET /location`
2. It queries **wttr.in** for that location's current temperature
3. It `POST /data` back to the server with location, outdoor temp,
   and its own sensor reading, form-encoded
4. The **Python server** (stdlib only — no dependencies) prints a
   formatted report

## Setup

Firmware (`firmware/main/main.c`) — set before building:

- `WIFI_SSID` / `WIFI_PASSWORD` — your network credentials
  (placeholders in this repo; never commit real ones)
- `SERVER_IP` — the LAN address of the machine running the server

Server:

```bash
python3 server/server.py   # listens on port 1234
```

Firmware (ESP-IDF 6.1):

```bash
cd firmware
idf.py set-target esp32c3
idf.py build flash monitor
```

## Sensor

`sensor_temp` and `sensor_hum` come from a real **SHTC3**
temperature/humidity sensor on I2C (address `0x70`, SDA GPIO 7,
SCL GPIO 8), read with CRC-8 validation on every sample. If the
read fails or the CRC doesn't match, the cycle is skipped — the
station never posts a reading it didn't actually measure.
