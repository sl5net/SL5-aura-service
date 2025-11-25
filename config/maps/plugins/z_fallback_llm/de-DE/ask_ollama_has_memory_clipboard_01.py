import subprocess
import re
import json
import os

import datetime
from pathlib import Path

# --- KONFIGURATION ---
DEBUG_FILE = Path("/tmp/aura_llm_debug.log")
MEMORY_FILE = Path(__file__).parent / "conversation_history.json"
MAX_HISTORY_ENTRIES = 6

def debug_log(msg):
    """Schreibt Debug-Infos in eine Datei, da wir Stdout im Hintergrund oft nicht sehen."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(DEBUG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

# --- ENVIRONMENT FIXES (NUCLEAR OPTION) ---
# Damit Hintergrundprozesse auf Clipboard zugreifen dürfen
user_home = str(Path.home())
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"
if "XAUTHORITY" not in os.environ:
    # Der Schlüssel zum X-Server liegt meist hier
    os.environ["XAUTHORITY"] = f"{user_home}/.Xauthority"

debug_log(f"INIT: Display={os.environ.get('DISPLAY')} XAuth={os.environ.get('XAUTHORITY')}")

# Versuch, pyperclip zu importieren
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    debug_log("ERROR: pyperclip nicht importierbar!")

def clean_text_for_typing(text):
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_clipboard_content():
    if not PYPERCLIP_AVAILABLE:
        return None

    try:
        # Versuch 1: Pyperclip (High Level)
        content = pyperclip.paste()

        # Wenn leer, Versuch 2: xclip direkt mit Environment (Low Level)
        if not content or not content.strip():
            debug_log("Pyperclip leer. Versuche xclip Fallback...")
            res = subprocess.run(
                ['xclip', '-selection', 'clipboard', '-o'],
                capture_output=True, text=True, timeout=1,
                env=os.environ # WICHTIG: Environment übergeben
            )
            if res.returncode == 0:
                content = res.stdout

        if content and content.strip():
            debug_log(f"SUCCESS: Clipboard gelesen ({len(content)} Zeichen)")
            return content.strip()
        else:
            debug_log("FAIL: Clipboard ist leer oder Zugriff verweigert.")
            return None

    except Exception as e:
        debug_log(f"EXCEPTION beim Clipboard Zugriff: {e}")
        return None

def load_history():
    if not MEMORY_FILE.exists(): return []
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception: return []

def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > MAX_HISTORY_ENTRIES * 2:
        history = history[-(MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception: pass

def execute(match_data):
    try:
        match_obj = match_data['regex_match_obj']
        # Gruppe finden (Name vs Text)
        if len(match_obj.groups()) >= 2:
            user_input = match_obj.group(2).strip()
        else:
            user_input = match_obj.group(1).strip()

        debug_log(f"USER INPUT: {user_input}")

        if not user_input: return "Ich habe nichts gehört."

        if "vergiss alles" in user_input.lower():
            if MEMORY_FILE.exists(): MEMORY_FILE.unlink()
            return "Gedächtnis gelöscht."

        # --- CLIPBOARD LOGIK ---
        trigger_words = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "das hier", "zusammenfassung"]
        clipboard_msg = ""

        if any(word in user_input.lower() for word in trigger_words):
            debug_log("Trigger erkannt. Lese Clipboard...")
            clipboard_content = get_clipboard_content()

            if clipboard_content:
                snippet = clipboard_content[:6000]
                clipboard_msg = f"\n\n--- ZWISCHENABLAGE INHALT ---\n{snippet}\n-----------------------------\n"
                if len(user_input.split()) < 3:
                    user_input += " (Beziehe dich auf die Zwischenablage)"
            else:
                # Klare Anweisung an das LLM, nicht zu halluzinieren
                debug_log("Setze Fallback-Nachricht für LLM.")
                clipboard_msg = (
                    "\n\n[SYSTEM HINWEIS: Der Zugriff auf die Zwischenablage ist fehlgeschlagen oder sie ist leer. "
                    "Erkläre NICHT was eine Zwischenablage ist. "
                    "Sag dem Nutzer einfach: 'Ich konnte die Zwischenablage nicht lesen.']\n"
                )

        # Prompt bauen
        history = load_history()
        system_instruction = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze), außer bei Zusammenfassungen. Keine Emojis."

        full_prompt = f"{system_instruction}\n\n"
        if history:
            full_prompt += "Verlauf:\n"
            for entry in history:
                role = "User" if entry['role'] == "user" else "Aura"
                full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += clipboard_msg
        full_prompt += f"\nUser: {user_input}\nAura:"

        # Ollama
        cmd = ["ollama", "run", "llama3.2", full_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=20)

        if result.returncode != 0: return f"Fehler: {result.stderr.strip()}"
        response_text = result.stdout.strip()

        clean_response = clean_text_for_typing(response_text)
        save_to_history(user_input, clean_response)

        debug_log(f"RESPONSE: {clean_response}")
        return clean_response

    except Exception as e:
        debug_log(f"FATAL ERROR: {e}")
        return f"Fehler: {str(e)}"
