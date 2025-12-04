# file: scripts/py/cli_client.py
from pathlib import Path

import requests
import json
import argparse
import os

# check my ip:
# # Alternative zu wieistmeineip.de:
# curl -s checkip.dyndns.org | grep -Eo '[0-9\.]+'

# Stellen Sie sicher, dass dies die korrekte Adresse des laufenden FastAPI-Service ist
# SERVICE_URL = "http://127.0.0.1:8000/process"
# SERVICE_URL = "http://127.0.0.1:8000/process_cli"

import os
from dotenv import load_dotenv
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".secrets")
API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER")

# sudo ufw status verbose | grep 8000
"""
sudo ufw allow 8000/tcp                 0|1 ✘  8s   STT 
Rule added
Rule added (v6)

"""

CLIENT_API_KEY = API_KEY_SECRET

#def verify_api_key(x_api_key: str = Header(None)):
#    if x_api_key is None or x_api_key != API_KEY_SECRET:


def send_request(text: str, lang: str):
    """Sendet die Anfrage an den FastAPI-Service."""

    payload = {
        "raw_text": text,
        "lang_code": lang
    }

    headers = {
        "X-API-Key": CLIENT_API_KEY
    }

    try:
        # Führen Sie den POST-Request aus
        response = requests.post(
            SERVICE_URL,
            json=payload,
            headers=headers,
            timeout=5
        )

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

