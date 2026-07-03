#!/usr/bin/env python3
# scripts/search_rules/run_palette_command.py:
import sys

if getattr(sys, "stdout", None) is not None:
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding and encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if getattr(sys, "stderr", None) is not None:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")

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

try:
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())
except Exception:
    import traceback
    with open(r"C:\tmp\sl5_aura\run_palette_import_error.log", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    raise

# tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
# PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8:replace"

log_file = PROJECT_ROOT / "log" / f"{Path(__file__).stem}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

do_log = False

def log(msg):
    if do_log:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

def is_api_running():
    try:
        with socket.create_connection(("127.0.0.1", 8830), timeout=0.1):
            return True
    except Exception as e:
        print(e)
        return False

def main():
    if len(sys.argv) < 2:
        query = "Läuf"
    else:
        query = sys.argv[1]

    secrets_path = PROJECT_ROOT / ".secrets"

    # Initialize debug logging for pythonw.exe execution
    log(f"\n--- Script execution started ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
    log(f"Query argument received: '{query}'\n")

    api_key = None

    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("SERVICE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        log(f"API key loaded successfully (length: {len(api_key)} characters).\n")
                        break
        except Exception as e20260702_1708:
            print(f'e20260702_1708: {e20260702_1708}')
            log(f'e20260702_1708: {e20260702_1708}')
    else:
        log("FATAL: SERVICE_API_KEY missing (no .secrets found on Windows)\n")
        raise RuntimeError("Missing SERVICE_API_KEY")

    if not api_key:
        log_file = PROJECT_ROOT / "log" / "run_palette_command.log"
        with open(log_file, "a", encoding="utf-8") as lf:
            log("ERROR: API key not loaded\n")
        raise RuntimeError("API key missing")

    log(f"secrets_path exists: {secrets_path.exists()}\n")

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
        time.sleep(3)
    if not is_api_running():
        print("🚀 Starting FastAPI Uvicorn Service in background...", flush=True)
        # CREATE_NO_WINDOW = 0x08000000
        DETACHED_PROCESS = '0x00000008' # noqa: F841

        # CREATE_NEW_PROCESS_GROUP = '0x00000200'
        # flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        flags = subprocess.DETACHED_PROCESS
        kwargs = {"start_new_session": True} if os.name != "nt" else {"creationflags": flags}

        DEBUG_LOG = PROJECT_ROOT / "log" / f"{Path(__file__).stem}.log"
        with open(DEBUG_LOG, "a", encoding="utf-8") as lf:
            subprocess.Popen(
                [sys.executable, str(PROJECT_ROOT / "scripts" / "py" / "start_uvicorn_service.py")],
                stdout=lf, stderr=lf, **kwargs
            )

        # subprocess.Popen(
        #     [sys.executable, str(PROJECT_ROOT / "scripts" / "py" / "start_uvicorn_service.py")],
        #     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  env=env, **kwargs
        # )
        # for _ in range(40):
        #     if is_api_running(): break
        #     time.sleep(0.1)

        # Wait for the API to become responsive
        api_ready = False
        for attempt in range(1, 140):
            if is_api_running():
                api_ready = True
                log(f"Uvicorn service became responsive after {attempt * 100}ms (attempt {attempt}).\n")
                break
            time.sleep(0.1)

        if not api_ready:
            log("WARNING: Uvicorn service failed to respond within 4.0 seconds timeout.\n")






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

                tmp_dir = Path("C:/tmp") if os.name == 'nt' else Path("/tmp")
                output_dir = tmp_dir / "sl5_aura" / "tts_output"

                log_file = PROJECT_ROOT / "log" / f"{Path(__file__).stem}.log"
                log_file.parent.mkdir(parents=True, exist_ok=True)

                with open(log_file, "a", encoding="utf-8") as lf:
                    log(f"--- try ({time.strftime('%H:%M:%S')}) ---\n")
                    log(f"output_dir: {output_dir}\n")
                    try:
                        output_dir.mkdir(parents=True, exist_ok=True)
                        out_file = output_dir / f"tts_output_{int(time.time() * 1000)}.txt"
                        with open(out_file, "w", encoding="utf-8") as f:
                            f.write(result_text)
                        log(f"success: file wrote -> {out_file}\n")
                    except PermissionError as pe:
                        log(f"ERROR (rights): {pe}\n")
                    except Exception as ex:
                        log(f"ERROR : {ex}\n")
            else:
                print(f"ERROR Service-answer : {res_data}")
    except Exception as e:
        # Write connection/runtime errors to log file since pythonw.exe suppresses stderr
        log(f"ERROR (API connection or runtime failure): {type(e).__name__} - {e}\n")
        print(f"connection error (Port 8830): {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
