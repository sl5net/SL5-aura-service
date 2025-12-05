# scripts/py/chat/streamlit-chat.py
import streamlit as st
import requests
import json

# --- KONFIGURATION ---
# Stellen Sie sicher, dass diese URL und der Port zu Ihrem laufenden Service passen
# HINWEIS: Wenn Sie es lokal testen, ist es oft http://127.0.0.1:8000

# curl -H "X-API-Key: lub2025-1204-22082025-1204-2208" -X POST -H "Content-Type: application/json" -d '{"raw_text": "Computer Wer bist du?", "lang_code": "de-DE"}' http://89.244.126.234:8830/process_cli


API_URL = "http://89.244.126.234:8830/process_cli" # Oder http://127.0.0.1:8000
API_KEY = "lub2025-1204-22082025-1204-2208"
LANG_CODE = "de-DE"

# Titel der Anwendung
st.title("SL5 Aura (external interface to the core logic)")
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
        service_answer = f"**Fehler beim Parsen der API-Antwort (kein gültiges JSON):**\n\n```\n{response.text}\n```"


    # 3. Service-Antwort zum Verlauf hinzufügen und anzeigen
    with st.chat_message("assistant"):
        st.markdown(service_answer)

    st.session_state.messages.append({"role": "assistant", "content": service_answer})
