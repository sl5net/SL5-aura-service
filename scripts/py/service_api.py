# file: scripts/py/service_api.py
import subprocess
import time
import os
import logging
from pathlib import Path

import socket

# Imports
from fastapi import FastAPI, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv

# Import der Kernfunktion
from scripts.py.func.process_text_in_background import process_text_in_background


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# --- 1. Setup & Konfiguration ---

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


SECRETS_PATH = PROJECT_ROOT / ".secrets"
print(f"DEBUG: Suche .secrets unter: {SECRETS_PATH}")

if not SECRETS_PATH.exists():
    print("FEHLER: .secrets Datei existiert NICHT am erwarteten Ort.")
load_dotenv(SECRETS_PATH)

API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER").strip()
# Debug Print (Should be removed in production)
print(f"DEBUG: Loaded API Key (length {len(API_KEY_SECRET)}): '{API_KEY_SECRET[:5]}...'")

# Temporärer Pfad
TMP_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "sl5_aura_service"
TMP_DIR.mkdir(parents=True, exist_ok=True)

app_logger = logging.getLogger("fastapi_service")
app_logger.setLevel(logging.INFO)

# Beispiel-URL für LanguageTool
LT_URL = "http://localhost:8082/v2/check"



# --- 2. FastAPI Setup ---

app = FastAPI()

def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    # Debug Prints
    # print(f"API_KEY_SECRET: {repr(API_KEY_SECRET)[:4]}...")

    if x_api_key is None or x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Ungültiger oder fehlender X-API-Key Header. Zugriff verweigert."
        )
    return True


def is_port_open(port: int) -> bool:
    """Check if a specific port is already accepting TCP connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@app.get("/admin")
def open_admin_panel():
    """
    On-Demand Gateway to the Aura Admin Dashboard.
    Detects if Streamlit is installed, auto-installs it if missing,
    spawns the background server, and redirects the browser.
    """
    port = 8084

    # 1. If the Admin Dashboard is already running, redirect immediately
    if is_port_open(port):
        return RedirectResponse(url=f"http://localhost:{port}")

    # 2. If not running, resolve paths to verify installation
    project_root = Path(__file__).resolve().parents[2]

    if os.name == 'nt':  # Windows
        streamlit_bin = project_root / ".venv" / "Scripts" / "streamlit.exe"
    else:  # Linux / Mac
        streamlit_bin = project_root / ".venv" / "bin" / "streamlit"

    # 3. Auto-install Streamlit on-demand if it is missing
    if not streamlit_bin.exists():
        from scripts.py.func.try_auto_install_package import try_auto_install_package
        # We pass the existing app_logger from service_api.py
        success = try_auto_install_package('streamlit', logger=app_logger)
        if not success:
            return HTMLResponse(
                content="<h3>Error: Failed to auto-install Streamlit. Please verify requirements-web.txt.</h3>",
                status_code=500
            )

    script_path = project_root / "scripts" / "py" / "chat" / "streamlit-admin.py"

    # 4. Start the Streamlit server in the background
    subprocess.Popen(
        [str(streamlit_bin), "run", str(script_path), "--server.port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    # 5. Return a styled loading page that auto-refreshes to /admin after 3 seconds
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aura Admin Initializing</title>
        <meta http-equiv="refresh" content="3; url=/admin">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #0e1117;
                color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.1);
                width: 50px;
                height: 50px;
                border-radius: 50%;
                border-left-color: #ff4b4b;
                animation: spin 1s linear infinite;
                margin-bottom: 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            h2 {
                font-weight: 400;
                margin: 0 0 10px 0;
            }
            p {
                color: #a3a8b4;
                margin: 0;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="spinner"></div>
        <h2>Initializing Aura Admin Dashboard...</h2>
        <p>Installing dependencies and starting the dashboard server. Please wait a moment.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# --- SICHERHEITS-MIDDLEWARE (Nur Unterstrich-Regel) ---
@app.middleware("http")
async def block_sensitive_folders(request: Request, call_next):
    """
    Blocks access if the path contains ANY folder starting with "_"
    (e.g. /_privat/data.txt, /config/_hidden/file.json).
    """
    path = request.url.path

    # Split path into segments: "/files/_abc/image.png" -> ["files", "_abc", "image.png"]
    path_segments = path.strip("/").split("/")

    for segment in path_segments:
        if segment.startswith("_"):
            app_logger.warning(f"Blocked access (Underscore Rule): {path}")
            return JSONResponse(
                status_code=403,
                content={"error": "Access to hidden folders (starting with '_') is forbidden."}
            )

    response = await call_next(request)
    return response


# Pydantic Modell
class ProcessRequest(BaseModel):
    raw_text: str
    lang_code: str
    unmasked: bool = False
    interface: str = 'terminal'


# --- 3. Endpunkt-Definition ---

# IMPORTANT: “Depends(verify_api_key)” was missing here!
@app.post("/process")
async def process_text_command(request: ProcessRequest, valid: bool = Depends(verify_api_key)):
    """
    Empfängt Text und Sprachcode über die API und startet die
    Hintergrundverarbeitung.
    """
    raw_text = request.raw_text
    lang_code = request.lang_code
    unmasked = request.unmasked

    recording_time = time.time()
    active_lt_url = LT_URL

    try:
        process_text_in_background(
            logger=app_logger,
            LT_LANGUAGE=lang_code,
            raw_text=raw_text,
            output_dir=TMP_DIR,
            recording_time=recording_time,
            active_lt_url=active_lt_url,
            unmasked=unmasked,
            interface='web',
        )

        app_logger.info(f"API-Request: Processing started for lang={lang_code}, unmasked={unmasked}, text='{raw_text[:30]}...'")

        return {
            "status": "success",
            "message": "Processing started.",
            "input_text": raw_text
        }

    except Exception as e:  # noqa: W0718
        app_logger.error(f"Error during background process execution: {e}")
        return {
            "status": "error",
            "message": f"Could not start process: {str(e)}",
            "input_text": raw_text
        }


@app.post("/process_cli")
def process_text_cli(request: ProcessRequest, valid: bool = Depends(verify_api_key)):
    """
    Empfängt Text, startet die Verarbeitung, wartet auf die Ausgabedatei,
    liest das Ergebnis und gibt es zurück.
    """
    raw_text = request.raw_text
    lang_code = request.lang_code
    recording_time = time.time()
    active_lt_url = LT_URL

    unmasked = request.unmasked

    # Eindeutigen Output-Ordner erstellen

    unique_dir_name = f"cli_request_{timestamp()}"
    request_output_dir = TMP_DIR / "sl5_aura" / "tts_output" / unique_dir_name
    request_output_dir.mkdir(parents=True, exist_ok=True)

    # Process start
    process_text_in_background(
        logger=app_logger,
        LT_LANGUAGE=lang_code,
        raw_text=raw_text,
        output_dir=TMP_DIR,
        recording_time=recording_time,
        active_lt_url=active_lt_url,
        output_dir_override=request_output_dir,
        unmasked=unmasked,
        interface=request.interface,
    )


    # Warten und Ergebnis lesen
    actual_result_text = "[NO OUTPUT FILE CREATED]"
    start_wait_time = time.time()
    MAX_WAIT_TIME = 5.0

    while time.time() - start_wait_time < MAX_WAIT_TIME:
        try:
            output_files = list(request_output_dir.glob("tts_output_*.txt"))

            if output_files:
                latest_file = max(output_files, key=os.path.getctime)
                with open(latest_file, 'r', encoding='utf-8-sig') as f:
                    actual_result_text = f.read().lstrip()

                os.remove(latest_file)
                request_output_dir.rmdir()
                break

        except OSError as e:
            app_logger.error(f"Fehler beim Auslesen des CLI-Ergebnisses: {e}")
            actual_result_text = f"[ERROR READING FILE: {e}]"
            break

        time.sleep(0.05)

    actual_result_text = actual_result_text.strip()
    app_logger.info(f"API-CLI-Call: Finished. Input='{raw_text[:20]}', Result='{actual_result_text[:20]}'")

    return {
        "status": "completed" if actual_result_text != "[NO OUTPUT FILE CREATED]" else "timeout",
        "result_text": actual_result_text,
        "input_text": raw_text
    }
