# scripts/py/chat/streamlit-chat.py
import streamlit as st
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit.components.v1 as components
import socket

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".secrets")

if "speak_enabled" not in st.session_state:
    st.session_state.speak_enabled = True
if "scroll_trigger" not in st.session_state:
    st.session_state.scroll_trigger = 0
if "speech_speed" not in st.session_state:
    st.session_state.speech_speed = 1.0
if "messages" not in st.session_state:
    st.session_state.messages = []

# def trigger_scroll_to_bottom():
#     st.session_state.scroll_trigger += 1

def st_speak_diagnostic(text, speed=1.0):
    safe_text = text.replace('"', '\\"').replace('\n', ' ')
    diag_html = f"""
    <div id="diag-box" style="padding:10px; border:1px solid #ccc; border-radius:5px; background:#f9f9f9; font-family:sans-serif; font-size:12px;">
        <b>Browser-Status:</b> <span id="status">Warte auf Klick...</span><br>
        <b>Stimmen gefunden:</b> <span id="voices-count">0</span><br>
        <b>Fehlermeldung:</b> <span id="error-msg" style="color:red;">keine</span>
    </div>
    <button id="play-btn" style="margin-top:10px; width:100%; padding:10px; background:#4f8bf9; color:white; border:none; border-radius:5px;">
        🔊 JETZT TESTEN (Klick mich!)
    </button>
    <script>
        const status = document.getElementById('status');
        const voicesCount = document.getElementById('voices-count');
        const errorMsg = document.getElementById('error-msg');
        const btn = document.getElementById('play-btn');
        const runSpeech = () => {{
            try {{
                if (!window.speechSynthesis) {{ status.innerText = "API NICHT UNTERSTÜTZT!"; return; }}
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance("{safe_text}");
                msg.lang = "de-DE"; msg.rate = {speed};
                msg.onstart = () => {{ status.innerText = "Spreche gerade..."; }};
                msg.onend = () => {{ status.innerText = "Fertig gesprochen."; }};
                msg.onerror = (e) => {{ status.innerText = "FEHLER!"; errorMsg.innerText = e.error; }};
                window.speechSynthesis.speak(msg);
                status.innerText = "Befehl an Browser gesendet...";
            }} catch (err) {{ errorMsg.innerText = err.message; }}
        }};
        const updateVoices = () => {{
            const v = window.speechSynthesis.getVoices();
            voicesCount.innerText = v.length + " (z.B. " + (v[0]?.name || 'keine') + ")";
        }};
        window.speechSynthesis.onvoiceschanged = updateVoices;
        updateVoices();
        btn.onclick = runSpeech;
    </script>
    """
    components.html(diag_html, height=180)

def st_speak(text, speed=1.0):
    safe_text = text.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
    speak_js = f"""
    <script>
        (function() {{
            if (window.speechSynthesis) {{
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance("{safe_text}");
                msg.lang = "de-DE";
                msg.rate = {speed};
                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(speak_js, height=0)

print("Loading .secrets from:", PROJECT_ROOT / ".secrets")

API_PORT = 8830
API_ENDPOINT = "process_cli"
API_HOSTNAME = "my-api-service"

def get_external_ip(ip_check_url="https://api.ipify.org"):
    try:
        response = requests.get(ip_check_url, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        st.error(f"Fehler beim Abrufen der externen IP-Adresse: {e}")
        return None

def get_api_base_url():
    public_ip = get_external_ip()
    local_json_url = f"http://localhost:{API_PORT}"
    public_http = f"http://{public_ip}:{API_PORT+1}"
    try:
        sock = socket.create_connection(('localhost', API_PORT), timeout=1)
        sock.close()
        st.info(f"JSON auf: ...{str(local_json_url)[-15:]}. HTTP online: ...{str(public_http)[-15:]}.")
        return local_json_url
    except (socket.error, ConnectionRefusedError):
        pass
    public_ip = get_external_ip()
    if public_ip:
        external_url = f"http://{public_ip}:{API_PORT}"
        st.info(f"Service nicht lokal gefunden. Verwende externe IP(JSON): {external_url}.")
        return external_url
    onlineIP = '89.244.126.232'
    fallback_url = f"http://{onlineIP}:{API_PORT}"
    st.warning(f"Verwende Fallback-IP: {fallback_url}")
    return fallback_url

BASE_API_URL = get_api_base_url()
FINAL_API_URL = f"{BASE_API_URL}/{API_ENDPOINT}"
API_URL = FINAL_API_URL

API_KEY_SECRET = os.environ.get("SERVICE_API_KEY", "DEVELOPMENT_KEY_PLACEHOLDER").strip()
API_KEY = API_KEY_SECRET
if not API_KEY:
    st.error("FEHLER: API_KEY konnte nicht geladen werden.")
LANG_CODE = "de-DE"

def copy_to_clipboard_component_v2(text_to_copy, button_label="Click to Copy (Then Ctrl+V)"):
    unique_id = hash(text_to_copy)
    html_code = f"""
    <input type="text" id="copy-target-{unique_id}" value="{text_to_copy}"
           style="position: absolute; left: -9999px;" readonly>
    <button style="background-color:#f0f2f6;color:#4f8bf9;border:1px solid #4f8bf9;padding:5px 10px;border-radius:5px;cursor:pointer;"
            onclick="var c=document.getElementById('copy-target-{unique_id}');c.select();document.execCommand('copy');
                     this.innerText='Copied!';
                     setTimeout(()=>this.innerText='{button_label}',2500);">{button_label}</button>
    """
    components.html(html_code, height=45)

def process_command(param):
    pass

# ================================================================
# FIX: Den richtigen CSS-Selektor für Streamlit 1.46+ verwenden.
# In neueren Versionen heißt die Klasse stChatFloatingInputContainer
# – nicht mehr stBottom. Außerdem: padding-bottom auf den
# Hauptinhalt damit die letzte Nachricht nicht verdeckt wird.
# ================================================================
st.markdown("""
<style>
/* Streamlit 1.46+ : Chat-Input Container */
.stChatFloatingInputContainer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 999999 !important;
    background: white !important;
    padding-bottom: env(safe-area-inset-bottom, 0px) !important;
}

/* Dark mode */
[data-theme="dark"] .stChatFloatingInputContainer,
.dark .stChatFloatingInputContainer {
    background: #0e1117 !important;
}

/* Ältere Versionen (stBottom) als Fallback */
div[data-testid="stBottom"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 999999 !important;
    background: white !important;
}

/* Platz am Ende des Inhalts damit letzte Nachricht
   nicht hinter dem Eingabefeld verschwindet */
.main .block-container {
    padding-bottom: 100px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("SL5 Aura (external interface to the core logic)")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Einstellungen 5")
    st.session_state.speak_enabled = st.checkbox("Ergebnisse laut vorlesen", value=st.session_state.speak_enabled)

    if "speech_speed_saved" not in st.session_state:
        try:
            st.session_state.speech_speed_saved = float(st.query_params.get("spd", 1.0))
        except (ValueError, TypeError):
            st.session_state.speech_speed_saved = 1.0

    speech_speed = st.slider("Geschwindigkeit", 0.5, 2.0, st.session_state.speech_speed_saved, 0.1)
    st.session_state.speech_speed_saved = speech_speed

    components.html(f"""<script>
        localStorage.setItem('sl5_speech_speed', '{speech_speed}');
        const url = new URL(window.parent.location.href);
        url.searchParams.set('spd', '{speech_speed}');
        window.parent.history.replaceState(null, '', url.toString());
    </script>""", height=0)

    if st.button("🔊 Sprach-Test"):
        st_speak("Die Sprachausgabe ist jetzt aktiviert.", speech_speed)
        st.success("Sound aktiviert!")

    st.markdown("---")
    st.subheader("Audio Diagnose")
    st_speak_diagnostic("Diagnose-Modus aktiv.")
    st.info("Hinweis: Chrome wird für die Sprachausgabe empfohlen.")

st.info('https://github.com/sl5net/SL5-aura-service/blob/master/docs/README/README-delang.md')
st.info('https://pad.ccc-mannheim.de/p/kihelfer')

st.markdown(r"""[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/demo_fast.gif)""")

example_text = "Aura Was ist das Besondere an SL5 Aura"
st.markdown(r"""### Beispiel-Eingaben:""")
st.code(example_text, language='plaintext')



if st.button("▶️ Beispiel direkt senden", key="ex_main"):
    st.session_state.prefill_input = example_text

copy_to_clipboard_component_v2(example_text,
                           "📋 Beispiel kopieren (⬇️ unten Einfügen, Ändern ▶️ Senden)")

if st.session_state.get('ready_to_submit', False):
    process_command(st.session_state['user_input'])
    st.session_state['ready_to_submit'] = False
    st.session_state['user_input'] = ""
    st.rerun()

st.markdown(r"""

*   SL5 Aura: Die Private KI-Steuerung.
    *   **Datenschutz:** 100% Offline und GDPR-konform.
    *   **Verlässlichkeit:** Hierarchische RegEx-Engine für präzise, wartbare Sprachbefehle.
    *   **Aura (RegEx-Kern):** Übernimmt die Steuerung (z.B. "Schalte Englisch an").
    *   **LLama3.2 (Fallback):** Übernimmt "Fuzzy Matching", Zusammenfassungen und kreative Interaktion ("Café-Gespräche").
    *   *Implikation:* Entlastung des Nutzers von exakter Syntax.

---

```
Wiki Wo ist Wannweil?
```
```
was ist 5+4
```
```
wiki was ist ein Berg Begriffserklärung
```
```
Wiki Wer ist Sebastian Lauffer
```
```
Wiki Wer ist Herr Schröer
```
```
Wiki Wer ist Harald
```
```
Ruth Kapitel 1 Vers 1
```
```
mit nachnamen laufer
```
```
mit ergoltherabpeut Herr Schrör
```
```
Englisch einschalten
```
```
Wie ist das Wetter?
```
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Reload-Button: immer sichtbar, scrollt nicht weg.
# window.parent.location.reload() macht echten Browser-Reload –
# st.session_state.messages bleibt erhalten weil Streamlit
# den Session State beim Reload beibehält.
col_reload, col_clear = st.columns([1, 1])
with col_reload:
    reload_html = (
        '<button onclick="window.parent.location.reload()" '
        'style="width:100%;padding:6px 10px;background:#f0f2f6;'
        'border:1px solid #ccc;border-radius:6px;cursor:pointer;font-size:13px;">'
        '🔄 Eingabefeld wieder sichtbar machen</button>'
    )
    components.html(reload_html, height=40)
with col_clear:
    if st.button("🗑️ Chat leeren", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BEISPIEL-BUTTONS ---
EXAMPLES = [
    "Aura Was ist das Besondere an SL5 Aura",
    "Wiki Wo ist Wannweil?",
    "was ist 5+4",

    "wiki was ist ein Berg Begriffserklärung",
    "Wiki Wer ist Sebastian Lauffer",
    "Wiki Wer ist Herr Schröer",

    "Wiki Wer ist Harald",
    "Ruth Kapitel 1 Vers 1",
    "mit nachnamen laufer",

    "mit ergoltherabpeut Herr Schrör",
    "Englisch einschalten",
    "Wie ist das Wetter?",

    "deutschlandradio", "gemini", "KI Kurse workshops",
    "deutschlandradio", "gemini", "Chaos",
    "openstreetmap", "gemini", "Chaos",
]
st.markdown("**Beispiele direkt ausprobieren:**")
cols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    if cols[i % 3].button(ex, key=f"exbtn_{i}"):
        st.session_state.prefill_input = ex
        st.rerun()

# --- EINGABE (original, unverändert) ---
if "prefill_input" not in st.session_state:
    st.session_state.prefill_input = ""

prefill = st.session_state.pop("prefill_input", "") if "prefill_input" in st.session_state else ""

if prefill:
    prompt = prefill
elif prompt := st.chat_input("Ihre Frage an den Service"):
    pass
else:
    prompt = None

if prompt:
    cleaned_prompt = prompt.strip().lower()
    trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]

    if any(trigger in cleaned_prompt for trigger in trigger_clipboard):
        st.error("Ihre Anfrage konnte aufgrund der Sicherheitsrichtlinien nicht verarbeitet werden.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        data = {"raw_text": prompt, "lang_code": LANG_CODE}
        headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

        service_answer = ""
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            api_response_data = response.json()
            service_answer = api_response_data.get("result") or \
                             api_response_data.get("result_text") or \
                             "API-Antwort erhalten (Unbekanntes Format)."
        except requests.exceptions.RequestException as e:
            service_answer = f"**Verbindungs- oder API-Fehler:**\n\n```\n{e}\n```"
        except json.JSONDecodeError:
            service_answer = f"**Fehler beim Parsen der API-Antwort:**\n\n```\n{response.text}\n```"

        st.session_state.messages.append({"role": "assistant", "content": service_answer})

        # Sprache und Scroll im Session State merken –
        # st.rerun() bricht sofort ab, danach kommt nichts mehr.
        # Beides wird beim nächsten Render-Durchlauf ausgeführt.
        if st.session_state.speak_enabled and service_answer:
            st.session_state["pending_speak"] = service_answer
        st.session_state["do_scroll"] = True

        st.rerun()

# --- NACH RERUN: Chat anzeigen, dann Sprache + Scroll ---
# Die letzte Antwort liegt jetzt in messages und wird oben im
# Chat-Verlauf gerendert. Danach Sprache und Scroll ausführen.

if st.session_state.get("pending_speak"):
    text_to_speak = st.session_state.pop("pending_speak")
    st_speak(text_to_speak, speech_speed)

if st.session_state.get("do_scroll"):
    st.session_state["do_scroll"] = False
    components.html(
        "<script>setTimeout(function(){"
        "var el=window.parent.document.querySelector('section.main');"
        "if(el)el.scrollTo({top:el.scrollHeight,behavior:'smooth'});"
        "},300);</script>",
        height=0
    )