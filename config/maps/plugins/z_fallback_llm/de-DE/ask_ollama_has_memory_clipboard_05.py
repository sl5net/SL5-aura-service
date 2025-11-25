import subprocess
import re
import json
import os
import sys
import logging
import inspect
from pathlib import Path

# --- KONFIGURATION ---
MEMORY_FILE = Path(__file__).parent / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
MAX_HISTORY_ENTRIES = 6

# Optional: File Logging
LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- LOGGING HELPER ---
def log_debug(message: str):
    caller_info = "UNKNOWN:0"
    stack = inspect.stack()
    if len(stack) > 1:
        try:
            filename = os.path.basename(stack[1].filename)
            line_number = stack[1].lineno
            caller_info = f"{filename}:{line_number}"
        except Exception:
            pass
    print(f"[DEBUG_LLM] {caller_info}: {message}", file=sys.stderr)
    logging.info(f"{caller_info}: {message}")

def clean_text_for_typing(text):
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_clipboard_content():
    """
    Liest den Inhalt aus der Bridge-Datei.
    Voraussetzung: ~/clipboard_bridge.sh läuft im Hintergrund!
    """
    if not BRIDGE_FILE.exists():
        log_debug(f"FAIL: Bridge-Datei {BRIDGE_FILE} nicht gefunden.")
        return None

    try:
        content = BRIDGE_FILE.read_text(encoding='utf-8').strip()

        if content:
            # --- WICHTIGE ÄNDERUNG: WIR LOGGEN JETZT DEN INHALT ---
            preview = content.replace('\n', ' ')[:100]
            log_debug(f"SUCCESS: Gelesen: '{preview}' ({len(content)} Zeichen)")
            return content
        else:
            log_debug("INFO: Bridge-Datei ist leer (0 Zeichen).")
            return None
    except Exception as e:
        log_debug(f"ERROR beim Lesen der Bridge-Datei: {e}")
        return None

def load_history():
    if not MEMORY_FILE.exists(): return []
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > MAX_HISTORY_ENTRIES * 2:
        history = history[-(MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log_debug(f"History Save Error: {e}")

def execute(match_data):
    try:
        match_obj = match_data['regex_match_obj']
        if len(match_obj.groups()) >= 2:
            user_input_raw = match_obj.group(2).strip()
        else:
            user_input_raw = match_obj.group(1).strip()

        log_debug(f"Input: '{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        if "vergiss alles" in user_input_raw.lower():
            if MEMORY_FILE.exists(): MEMORY_FILE.unlink()
            return "Gedächtnis gelöscht."

        # --- CLIPBOARD LOGIC ---
        trigger_words = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "das hier", "zusammenfassung"]

        final_context = ""
        user_suffix = user_input_raw

        if any(word in user_input_raw.lower() for word in trigger_words):
            log_debug("Trigger detected.")
            clipboard_content = get_clipboard_content()

            if clipboard_content:
                final_context = f"\n\n--- KONTEXT ---\n{clipboard_content[:8000]}\n--------------------------------\n"

                # Prompt umschreiben
                if len(user_input_raw.split()) < 5:
                    user_suffix = "Fasse den Kontext zusammen oder erkläre ihn."
                    log_debug("Prompt rewritten.")
            else:
                log_debug("Clipboard content was empty.")
                return "Die Zwischenablage ist leer."

        # --- PROMPT ---
        history = load_history()
        base = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze), außer bei Analysen. Keine Emojis."
        full_prompt = f"{base}{final_context}\n\n"

        if history:
            full_prompt += "Verlauf:\n"
            for entry in history:
                role = "User" if entry['role'] == "user" else "Aura"
                full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += f"\nUser: {user_suffix}\nAura:"

        # --- OLLAMA ---
        log_debug("Calling Ollama...")
        cmd = ["ollama", "run", "llama3.2", full_prompt]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=30)

        if result.returncode != 0:
            log_debug(f"Ollama Error: {result.stderr.strip()}")
            return f"Fehler: {result.stderr.strip()}"

        response = clean_text_for_typing(result.stdout.strip())
        log_debug(f"Ollama Response: {response}")

        save_to_history(user_input_raw, response)

        return response

    except Exception as e:
        log_debug(f"FATAL EXCEPTION: {e}")
        return f"Systemfehler: {str(e)}"
