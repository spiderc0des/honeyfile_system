#!/usr/bin/env python3
import http.server
import socketserver
import datetime
import subprocess

PORT = 7000

class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        super().log_message(format, *args)
        ip = self.client_address[0]
        mac = self.get_mac_address(ip)
        user_agent = self.headers.get('User-Agent', 'Unknown')
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"{timestamp} - IP: {ip} - MAC: {mac} - User-Agent: {user_agent} accessed {self.path}\n"
        with open("access.log", "a") as f:
            f.write(log_entry)

    def get_mac_address(self, ip):
        try:
            result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            for line in lines:
                if ip in line:
                    parts = line.split()
                    for part in parts:
                        if ':' in part:
                            return part
        except Exception as e:
            print(f"Error retrieving MAC address for IP {ip}: {str(e)}")
        return "Unknown MAC"


Handler = LoggingHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    print(f"http://localhost:{PORT}")
    httpd.serve_forever()
