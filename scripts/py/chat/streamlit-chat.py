# scripts/py/chat/streamlit-chat.py
import streamlit as st
import requests
import json, os
from pathlib import Path

from dotenv import load_dotenv # <<< MUSS HIER SEIN

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".secrets")

print("Loading .secrets from:", PROJECT_ROOT / ".secrets")


# --- KONFIGURATION ---

# curl -H "X-API-Key: ...." -X POST -H "Content-Type: application/json" -d '{"raw_text": "Computer Wer bist du?", "lang_code": "de-DE"}' http://...:8830/process_cli


#import streamlit as st
#import requests
#import os
import socket
#from urllib.parse import urlparse

# --- Konfiguration ---
API_PORT = 8830
API_ENDPOINT = "process_cli"
# Versuchen Sie zuerst, einen Hostnamen zu verwenden, falls dieser konfiguriert ist (z.B. in /etc/hosts)
API_HOSTNAME = "my-api-service"  # Ersetzen Sie dies durch einen echten Hostnamen oder lassen Sie es 'None'


# --- Funktion zur IP-Ermittlung ---

# scripts/py/chat/streamlit-chat.py
def get_external_ip(ip_check_url="https://api.ipify.org"):
    """Ruft die aktuelle öffentliche IP-Adresse ab."""
    try:
        # Verwenden Sie ein kurzes Timeout, um die App nicht zu verzögern
        response = requests.get(ip_check_url, timeout=5)
        response.raise_for_status()  # Löst Fehler bei 4xx/5xx Status-Codes aus
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        st.error(f"Fehler beim Abrufen der externen IP-Adresse: {e}")
        # Rückgabe eines Platzhalters oder Abbruch
        return None


# --- Funktion zur Bestimmung der finalen API_URL ---

def get_api_base_url():
    """Bestimmt die Basis-URL für den API-Dienst."""
    # 1. Lokale/interne Prüfung (localhost, Hostname)
    public_ip = get_external_ip()
    # Prüfen Sie zuerst localhost
    local_json_url = f"http://localhost:{API_PORT}"
    public_http = f"http://{public_ip}:{API_PORT+1}"
    try:
        # Versuchen Sie eine Verbindung nur zum Host (ohne API-Aufruf)
        sock = socket.create_connection(('localhost', API_PORT), timeout=1)
        sock.close()
        st.info(f"JSON auf: {local_json_url}. HTTP Alterntive: {public_http}.")
        return local_json_url
    except (socket.error, ConnectionRefusedError):
        # Wenn localhost nicht funktioniert, gehen wir zum nächsten Schritt über.
        pass

    # 2. Externe IP-Prüfung (für dynamische externe IPs)

    # Nur wenn der Dienst nicht lokal läuft, ermitteln wir die externe IP
    public_ip = get_external_ip()
    if public_ip:
        external_url = f"http://{public_ip}:{API_PORT}"
        external_url_streamlit = f"http://{public_ip}:{int(API_PORT)}"
        # Fügen Sie hier optional eine weitere Erreichbarkeitsprüfung hinzu (z.B. ping/telnet)
        st.info(f"Service nicht lokal gefunden. "
                f"Verwende externe IP(JSON): {external_url}. "
                f"external streamlit: {external_url_streamlit}")
        return external_url

    # 3. Fallback (Wenn nichts funktioniert, verwenden Sie die alte statische IP als Fallback)

    # Verwenden Sie die alte, aber fehlgeschlagene, statische IP als Notfall-Fallback.
    # Dies ist hilfreich, falls der externe IP-Dienst ausgefallen ist.
    onlineIP = '88.130.216.36'
    fallback_url = f"http://{onlineIP}:{API_PORT}"  # Verwenden Sie die alte IP
    st.warning(f"Konnte lokale oder aktuelle externe IP nicht ermitteln. Verwende Fallback-IP: {fallback_url}")
    return fallback_url


BASE_API_URL = get_api_base_url()
FINAL_API_URL = f"{BASE_API_URL}/{API_ENDPOINT}"

API_URL = FINAL_API_URL

API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER").strip()
API_KEY = API_KEY_SECRET
# API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("FEHLER: API_KEY konnte nicht geladen werden.")
LANG_CODE = "de-DE"

# Titel der Anwendung
st.title("SL5 Aura (external interface to the core logic)")
st.markdown("""
### Beispiel-Eingaben:
```
Aura Was ist das besondere an SL5 Aura
```

```py
# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pr.py
    ('', r'^(?!Computer|Aura).*(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der| Herr)? (?P<search>.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),
```

```
Wo ist Wannweil?
```

```py
    ('', r'(?:rechne|was ist|was is|was)\s*(\d+)\s*([\+\-\*\/]|plus|minus|mal|geteilt durch)\s*(\d+)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'calculator.py']
    }),
```

```
was ist 5+4
```

```
Wer ist Sebastian Lauffer
```

```
Wer ist Herr Schröer
```

```
Wer ist Harald
```

```py
# config/maps/plugins/bible_search/FUZZY_MAP_pr.py
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
```

```
Ruth Kapitel 1 Vers 1
```
Rechtschreibung:
```
mit nachnamen laufer
```
```
mit ergoltherabpeut Herr Schrör
```





```py
# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pr.py
    ('', r'\b(wie (wird|ist)\b.*\bwetter|wetterbericht|wettervorhersage)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'weather.py'] # Passe den Pfad ggf. an
    }),
```

```
Wie ist das Wetter?
```
Die aktuellen Wetterinformationen sind Ausnahme von der Offline-Regel. 
Sie werden bei einer Anfrage über das Internet neu abgerufen, sofern der letzte Abruf mehr als 15 Minuten zurückliegt.
Der sonstige Funktionsumfang hängen von den Beispielen (Plugins) ab, die Sie verwenden oder erstellt haben.

""")
st.caption(f"Verbindet mit: {API_URL}")

# Initialisiere den Chat-Verlauf in Streamlit's Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zeige vorherige Nachrichten an (falls vorhanden)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HAUPT-EINGABE-BEREICH ---
if prompt := st.chat_input("Ihre Frage an den Service"):

    # 1. Benutzer-Eingabe zum Verlauf hinzufügen und anzeigen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. API-Anfrage vorbereiten und senden
    data = {
        "raw_text": prompt,
        "lang_code": LANG_CODE
    }
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        # Prüfen auf HTTP-Fehler
        response.raise_for_status()

        # Antwort auswerten (Annahme: Die Antwort ist ein JSON-Objekt mit einem 'result'-Feld)
        # PASSEN SIE DIESEN TEIL AN DAS EXAKTE ANTWORT-FORMAT IHRES SERVICES AN!
        api_response_data = response.json()

        # ANNAHME: Die relevante Antwort steht in einem Feld namens 'result' oder 'text'
        # PASSEN SIE DEN KEY (z.B. 'result') AN IHR EXAKTES FORMAT AN!
        service_answer = api_response_data.get("result") or api_response_data.get("result_text") or "API-Antwort erhalten (Unbekanntes Format)."

    except requests.exceptions.RequestException as e:
        service_answer = f"**Verbindungs- oder API-Fehler:**\n\n```\n{e}\n```"
    except json.JSONDecodeError:
        service_answer = (f"**Fehler beim Parsen der "
                          f"API-Antwort (kein gültiges JSON):**\n\n```\n{response.text}\n```")


    # 3. Service-Antwort zum Verlauf hinzufügen und anzeigen
    with st.chat_message("assistant"):
        st.markdown(service_answer)

    st.session_state.messages.append({"role": "assistant", "content": service_answer})
