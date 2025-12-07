# file: scripts/py/service_api.py

import time
from pathlib import Path

from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel
import os # noqa: F811
import logging

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SECRETS_PATH = PROJECT_ROOT / ".secrets"
print(f"DEBUG: Suche .secrets unter: {SECRETS_PATH}")
if not SECRETS_PATH.exists():
    print("FEHLER: .secrets Datei existiert NICHT am erwarteten Ort.")
load_dotenv(SECRETS_PATH)


API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER").strip()

print(f"DEBUG: Loaded API Key (length {len(API_KEY_SECRET)}): '{API_KEY_SECRET[:5]}...'")


TMP_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "sl5_aura_service"
TMP_DIR.mkdir(parents=True, exist_ok=True)

app_logger = logging.getLogger("fastapi_service")
app_logger.setLevel(logging.INFO)

# Dies muss der tatsächliche temporäre Pfad sein, den Ihre Anwendung verwendet!
TMP_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "sl5_aura_service"
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Beispiel-URL für LanguageTool (muss in settings oder hier definiert sein)
LT_URL = "http://localhost:8082/v2/check" # Muss der tatsächlichen URL entsprechen

# Import der Kernfunktion
from scripts.py.func.process_text_in_background import process_text_in_background


# --- 2. FastAPI Setup ---


# file: scripts/py/service_api.py
app = FastAPI()
from fastapi import Header

def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    print(f"API_KEY_SECRET: {repr(API_KEY_SECRET)[:4]}...")
    print(f"Incoming X-API-Key: x_api_key: {repr(x_api_key)[:4]}...")
    if x_api_key is None or x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Ungültiger oder fehlender X-API-Key Header. Zugriff verweigert."
        )
    return True

# Pydantic Modell für die eingehenden Daten
class ProcessRequest(BaseModel):
    raw_text: str
    lang_code: str
    # 'output_dir_override' könnte optional hier hinzugefügt werden:
    # output_dir_override: str = None


# --- 3. Endpunkt-Definition ---

@app.post("/process")
async def process_text_command(request: ProcessRequest):
    """
    Empfängt Text und Sprachcode über die API und startet die
    Hintergrundverarbeitung.
    """

    # 1. Parameter aus dem Request entpacken
    raw_text = request.raw_text
    lang_code = request.lang_code

    # 2. Andere notwendige Parameter vorbereiten
    recording_time = time.time()
    active_lt_url = LT_URL # Verwende die oben definierte Konstante

    # 3. Funktion im Hintergrund aufrufen
    # FastAPI wird diese synchrone Funktion in einem Threadpool ausführen,
    # was ein nicht-blockierendes Verhalten für den API-Server gewährleistet.
    try:
        process_text_in_background(
            logger=app_logger,         # Verwenden Sie Ihren eingerichteten Logger
            LT_LANGUAGE=lang_code,
            raw_text=raw_text,
            TMP_DIR=TMP_DIR,           # Verwenden Sie das vordefinierte TMP_DIR
            recording_time=recording_time,
            active_lt_url=active_lt_url,
            # Wir verwenden KEIN output_dir_override, da dies für den normalen Service-Betrieb unnötig ist.
        )

        app_logger.info(f"API-Request: Processing started for lang={lang_code}, text='{raw_text[:30]}...'")

        return {
            "status": "success",
            "message": "Processing started.",
            "input_text": raw_text
        }

    except Exception as e:
        app_logger.error(f"Error during background process execution: {e}")
        return {
            "status": "error",
            "message": f"Could not start process: {str(e)}",
            "input_text": raw_text
        }










#@app.post("/process_cli")
#def process_text_cli(request: ProcessRequest):

@app.post("/process_cli")
def process_text_cli(request: ProcessRequest, valid: bool = Depends(verify_api_key)):

    """
    Empfängt Text, startet die Verarbeitung, wartet auf die Ausgabedatei,
    liest das Ergebnis und gibt es zurück.
    """

    # 1. Parameter vorbereiten
    raw_text = request.raw_text
    lang_code = request.lang_code
    recording_time = time.time()
    active_lt_url = LT_URL

    # 2. Eindeutigen Output-Ordner erstellen (wie im self_tester)
    # Verwenden eines eindeutigen Namens, um Race Conditions zu vermeiden
    unique_dir_name = f"cli_request_{int(time.time() * 1000)}"
    request_output_dir = TMP_DIR / unique_dir_name
    request_output_dir.mkdir(parents=True, exist_ok=True)

    # 3. Prozess starten (schreibt in den eindeutigen Ordner)
    process_text_in_background(
        logger=app_logger,
        LT_LANGUAGE=lang_code,
        raw_text=raw_text,
        TMP_DIR=TMP_DIR,           # Beibehalten der ursprünglichen TMP_DIR-Logik
        recording_time=recording_time,
        active_lt_url=active_lt_url,
        output_dir_override=request_output_dir # Wichtig: Leitet die Ausgabe um
    )

    # 4. Warten und Ergebnis aus der Datei lesen (Logik vom self_tester übernommen)
    actual_result_text = "[NO OUTPUT FILE CREATED]"
    start_wait_time = time.time()
    MAX_WAIT_TIME = 5.0  # Maximal 5 Sekunden warten

    while time.time() - start_wait_time < MAX_WAIT_TIME:
        try:
            # Suchen nach der Ausgabedatei im spezifischen Ordner
            output_files = list(request_output_dir.glob("tts_output_*.txt"))

            if output_files:
                # Datei gefunden! Logik zum Lesen und Aufräumen
                latest_file = max(output_files, key=os.path.getctime)
                with open(latest_file, 'r', encoding='utf-8-sig') as f:
                    actual_result_text = f.read().lstrip()

                # Aufräumen: Datei und temporären Ordner löschen
                os.remove(latest_file)
                request_output_dir.rmdir()
                break # Schleife beenden, Ergebnis gefunden

        except Exception as e:
            # Fehler beim Lesen/Aufräumen
            app_logger.error(f"Fehler beim Auslesen des CLI-Ergebnisses: {e}")
            actual_result_text = f"[ERROR READING FILE: {e}]"
            break # Schleife bei Fehler beenden

        time.sleep(0.05) # Kurze Pause

    # Bereinigung des Ergebnistextes (wie im self-tester)
    # HINWEIS: Sie müssen settings.signatur importieren, um dies zu tun!
    # if actual_result_text != "[NO OUTPUT FILE CREATED]":
    #    actual_result_text = actual_result_text.replace(settings.signatur1, '')
    #    actual_result_text = actual_result_text.replace(settings.signatur, '')
    actual_result_text = actual_result_text.strip()

    app_logger.info(f"API-CLI-Call: Finished. Input='{raw_text[:20]}', Result='{actual_result_text[:20]}'")

    return {
        "status": "completed" if actual_result_text != "[NO OUTPUT FILE CREATED]" else "timeout",
        "result_text": actual_result_text, # <-- DAS ERGEBNIS!
        "input_text": raw_text
    }
    pass
