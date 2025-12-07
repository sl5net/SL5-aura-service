# file: scripts/py/cli_client.py
from pathlib import Path

import requests
import json
import argparse
import os # noqa: F811

from dotenv import load_dotenv

# check my ip:
# # Alternative zu wieistmeineip.de:
# curl -s checkip.dyndns.org | grep -Eo '[0-9\.]+'

# file: scripts/py/cli_client.py
SERVICE_URL = "http://127.0.0.1:8830/process_cli"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".secrets")
print("Loading .secrets from:", PROJECT_ROOT / ".secrets")
API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER").strip()
CLIENT_API_KEY = API_KEY_SECRET

print("CLIENT_API_KEY:", repr(CLIENT_API_KEY))

def send_request(text: str, lang: str):
    """Sendet die Anfrage an den FastAPI-Service."""

    payload = {
        "raw_text": text,
        "lang_code": lang
    }

    # file: scripts/py/cli_client.py:39
    headers = {
        "X-API-Key": CLIENT_API_KEY
    }

    try:
        # Führen Sie den POST-Request aus

        response = requests.post(SERVICE_URL,json=payload,headers=headers,timeout=120)

        response.raise_for_status()

        # Ausgabe der Server-Antwort
        #print("Service-Antwort:")
        #print(json.dumps(response.json(), indent=4))


        # Ausgabe der Server-Antwort
        response_data = response.json()

        if response_data.get("status") == "completed":
            # Direkte Ausgabe des Ergebnistextes
            print(response_data.get("result_text", "FEHLER: Kein Ergebnis im Feld 'result_text'."))
        else:
            # Bei Fehlern oder Timeouts die vollständige Antwort ausgeben
            print("Service-Antwort (Fehler/Timeout):")
            print(json.dumps(response_data, indent=4))


    except requests.exceptions.HTTPError as errh:
        print(f"HTTP-Fehler: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Verbindungsfehler (Service nicht erreichbar?): {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout-Fehler: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Unbekannter Fehler: {err}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CLI-Client für den Prozess-Service.")
    parser.add_argument("text", type=str, help="Der Text, der verarbeitet werden soll.")
    parser.add_argument("--lang", type=str, default="de-DE",
                        help="Der Sprachcode für die Verarbeitung (Standard: de-DE).")

    args = parser.parse_args()

    send_request(args.text, args.lang)

