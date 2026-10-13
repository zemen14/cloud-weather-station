#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote_plus
import datetime

PORT     = 1234
LOCATION = "Santa Cruz, CA"

class WeatherHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == "/location":
            body = LOCATION.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] Sent location: {LOCATION}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/data":
            length  = int(self.headers.get("Content-Length", 0))
            body    = self.rfile.read(length).decode()
            params  = parse_qs(body)
            location     = unquote_plus(params.get("location",     ["N/A"])[0])
            outdoor_temp = unquote_plus(params.get("outdoor_temp", ["N/A"])[0])
            sensor_temp  = unquote_plus(params.get("sensor_temp",  ["N/A"])[0])
            sensor_hum   = unquote_plus(params.get("sensor_hum",   ["N/A"])[0])
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{ts}] ── Weather Station Report ──")
            print(f"  Location     : {location}")
            print(f"  Outdoor temp : {outdoor_temp} C")
            print(f"  Sensor temp  : {sensor_temp} C")
            print(f"  Humidity     : {sensor_hum} %")
            print(f"────────────────────────────────\n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), WeatherHandler)
    print(f"Cloud weather station server on port {PORT}")
    print(f"Location: {LOCATION}\n")
    server.serve_forever()
