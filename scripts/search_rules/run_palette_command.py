#!/usr/bin/env python3
# scripts/search_rules/run_palette_command.py:1
import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json
import urllib.request
import os
import socket
import subprocess
import time
from pathlib import Path
import logging
logger = logging.getLogger()


def is_api_running():
    try:
        with socket.create_connection(("127.0.0.1", 8830), timeout=0.1):
            return True
    except Exception: return False

def main():
    if len(sys.argv) < 2: sys.exit(0)
    query = sys.argv[1]
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
    secrets_path = PROJECT_ROOT / ".secrets"

    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("SERVICE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except Exception as e20260702_1708:
            print(f'e20260702_1708: {e20260702_1708}')


    # DEBUG_LOG = PROJECT_ROOT / "log" / "palette_launch_debug.log"
    # with open(DEBUG_LOG, "a", encoding="utf-8") as lf:
    #     subprocess.Popen(
    #         [sys.executable, str(PROJECT_ROOT / "scripts" / "py" / "start_uvicorn_service.py")],
    #         stdout=lf, stderr=lf, **kwargs
    #     )

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"  # erzwingt UTF-8 Mode für den Kindprozess
    env["PYTHONIOENCODING"] = "utf-8:replace"  # Fallback, falls PYTHONUTF8 nicht greift

    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("SERVICE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except Exception as e20260702_1707:
            print(f'e20260702_1707: {e20260702_1707}')


    if not is_api_running():
        print("🚀 Starting FastAPI Uvicorn Service in background...", flush=True)
        # CREATE_NO_WINDOW = 0x08000000
        DETACHED_PROCESS = '0x00000008' # noqa: F841

        # CREATE_NEW_PROCESS_GROUP = '0x00000200'
        # flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        flags = subprocess.DETACHED_PROCESS
        kwargs = {"start_new_session": True} if os.name != "nt" else {"creationflags": flags}

        DEBUG_LOG = PROJECT_ROOT / "log" / "palette_launch_debug.log"
        with open(DEBUG_LOG, "a", encoding="utf-8") as lf:
            subprocess.Popen(
                [sys.executable, str(PROJECT_ROOT / "scripts" / "py" / "start_uvicorn_service.py")],
                stdout=lf, stderr=lf, **kwargs
            )

        # subprocess.Popen(
        #     [sys.executable, str(PROJECT_ROOT / "scripts" / "py" / "start_uvicorn_service.py")],
        #     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  env=env, **kwargs
        # )
        for _ in range(40):
            if is_api_running(): break
            time.sleep(0.1)

    # payload = {"raw_text": query, "lang_code": "de-DE", "unmasked": False}
    payload = {"raw_text": query, "lang_code": "de-DE", "unmasked": False, "interface": "speech"}
    data = json.dumps(payload).encode("utf-8")
    url = "http://127.0.0.1:8830/process_cli"
    req = urllib.request.Request(
        url, data=data,
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("status") == "completed":
                result_text = res_data.get("result_text", "")
                print(result_text)

                # Schreibe die Ausgabedatei für Hintergrund-Watcher (Master-Kompatibilität)
                tmp_dir = Path("C:/tmp") if os.name == 'nt' else Path("/tmp")
                output_dir = tmp_dir / "sl5_aura" / "tts_output"
                output_dir.mkdir(parents=True, exist_ok=True)
                out_file = output_dir / f"tts_output_{int(time.time() * 1000)}.txt"
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(result_text)
            else:
                print(f"Service-Antwort (Fehler): {res_data}")
    except Exception as e:
        print(f"Verbindungsfehler (Port 8830): {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
