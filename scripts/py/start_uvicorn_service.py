# start_service.py

import os
import sys
import subprocess
import psutil
import time
from pathlib import Path

# --- KONFIGURATION ---
HOST = "0.0.0.0"
PORT = 8000
MODULE_PATH = "scripts.py.service_api:app"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_FILE = PROJECT_ROOT / 'log' / "service_start.log"
# ----------------------

def find_and_kill_process_on_port(port):
    """Sucht nach Prozessen, die auf dem gegebenen TCP-Port lauschen und beendet diese."""

    # psutil.net_connections() liefert alle Verbindungen, wir filtern nach LISTEN auf dem Port
    for conn in psutil.net_connections(kind='inet'):
        # Prüfen auf LISTEN-Status und passenden lokalen Port
        if conn.status == 'LISTEN' and conn.laddr.port == port:
            pid = conn.pid

            # WICHTIG: Prüfen, ob der Prozess wirklich existiert und nicht nur ein Trace ist
            if psutil.pid_exists(pid):
                try:
                    p = psutil.Process(pid)
                    print(f"WARNUNG: Port {port} belegt durch PID {pid} (Name: {p.name()}).")

                    # Versuche, den Prozess zu beenden (SIGTERM)
                    p.terminate()
                    p.wait(timeout=5) # Warte maximal 5 Sekunden auf die Beendigung

                    if p.is_running():
                        print(f"WARNUNG: PID {pid} reagiert nicht, erzwinge Beendigung (SIGKILL).")
                        p.kill() # Erzwinge die Beendigung
                        p.wait(timeout=5)

                    print(f"INFO: Prozess PID {pid} wurde erfolgreich beendet.")
                    return True # Prozess gefunden und beendet

                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    print(f"FEHLER: Konnte PID {pid} nicht beenden (Fehler: {e}).")
                    return False # Fehler beim Beenden

    return False # Kein Prozess gefunden

def start_uvicorn_service(host, port, module_path):
    """Startet den Uvicorn-Service neu."""

    print(f"INFO: Starte Uvicorn auf {host}:{port} mit Modul {module_path}...")

    command = [
        sys.executable,  # Das aktuell laufende Python (aus der VENV)
        "-m", "uvicorn",
        module_path,
        "--host", host,
        "--port", str(port),
        "--reload"
    ]

    try:
        with LOG_FILE.open('a', encoding='utf-8') as log_f:

            # Subprocess.Popen startet den Befehl im Hintergrund
            process = subprocess.Popen(
                command,
                cwd=PROJECT_ROOT, # <<< KORREKTUR: Setze das CWD auf den Projekt-Root
                stdout=log_f,
                stderr=log_f,
                preexec_fn=os.setsid
            )
            print(f"INFO: Uvicorn-Prozess (PID: {process.pid}) gestartet. Logs in {LOG_FILE}")
            # ...
            return process

    except Exception as e:
        print(f"FEHLER: Uvicorn konnte nicht gestartet werden: {e}")


if __name__ == "__main__":

    print(f"--- Service Start Skript ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")

    # 1. Beende den alten Prozess, falls vorhanden
    find_and_kill_process_on_port(PORT)

    # 2. Kurze Pause, um sicherzustellen, dass der Port freigegeben ist
    time.sleep(1)

    # 3. Starte Uvicorn neu
    start_uvicorn_service(HOST, PORT, MODULE_PATH)

    print("---------------------------------------------------------")

