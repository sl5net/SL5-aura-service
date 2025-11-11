# simple_log_server.py

readme = """
Standardmäßig dient der SimpleHTTPRequestHandler (der erste Code-Vorschlag) nur die Dateien in dem Verzeichnis, in dem er gestartet wird, und allen Unterverzeichnissen. Es ist ein reiner Download-Server (GET-Anfragen) und verhindert normalerweise den Zugriff auf darüber liegende Verzeichnisse. ABER: Er stellt alle Dateien in diesem Startverzeichnis bereit.
"""

import http.server
import socketserver
import logging

logging.basicConfig(level=logging.INFO)
PORT = 8000

# To be executed in the directory containing the log file
handler = http.server.SimpleHTTPRequestHandler

# Set up to be accessible from the network
with socketserver.TCPServer(("", PORT), handler) as httpd:
    logging.info(f"Serving at port {PORT}. Access this PC's IP address from your main machine.")
    httpd.serve_forever()
