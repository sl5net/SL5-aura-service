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

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

def get_readme_content():
    """Sucht README.md in übergeordneten Ordnern."""
    try:
        current_path = Path(__file__).resolve()
        for _ in range(6):
            current_path = current_path.parent
            readme_path = current_path / "README.md"
            if readme_path.exists():
                log_debug(f"README gefunden: {readme_path}")
                content = readme_path.read_text(encoding='utf-8').strip()

                # OPTIMIERUNG: Nur die ersten 6000 Zeichen nehmen.
                # Das deckt meist Intro, Features und Install ab.
                # 16000 war zu viel für schnelles Inferenz.
                return content[:6000]
        log_debug("WARNUNG: Keine README.md gefunden.")
        return None
    except Exception as e:
        log_debug(f"Error reading README: {e}")
        return None

def get_clipboard_content():
    if not BRIDGE_FILE.exists():
        log_debug(f"FAIL: Bridge-Datei {BRIDGE_FILE} fehlt.")
        return None
    try:
        content = BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content:
            preview = content.replace('\n', ' ')[:50]
            log_debug(f"SUCCESS: Clipboard: '{preview}...' ({len(content)} Zeichen)")
            return content
        return None
    except Exception:
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
        if len(match_obj.groups()) >= 2:
            user_input_raw = match_obj.group(2).strip()
        else:
            user_input_raw = match_obj.group(1).strip()

        log_debug(f"Input: '{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        if "vergiss alles" in user_input_raw.lower():
            if MEMORY_FILE.exists():
                try: MEMORY_FILE.unlink()
                except: pass
            return "Gedächtnis gelöscht."

        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "zusammenfassung"]
        trigger_readme = [
            "hilfe", "dokumentation", "readme", "read me", "redmi", "lies mich",
            "wie installiere", "wie funktioniert", "projekt", "features", "was kannst du",
            "anleitung", "handbuch"
        ]

        context_data = ""
        system_role = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze)."
        use_history = True
        input_lower = user_input_raw.lower()

        # Fall 1: Clipboard
        if any(w in input_lower for w in trigger_clipboard):
            log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten in der Zwischenablage."
                use_history = False
            else:
                return "Die Zwischenablage ist leer."

        # Fall 2: Projekt-Fragen (README)
        elif any(w in input_lower for w in trigger_readme):
            log_debug("Mode: README / SUPPORT")
            readme_content = get_readme_content()
            if readme_content:
                # Gekürzte Readme übergeben
                context_data = f"\nPROJEKT DOKUMENTATION (README.md - Auszug):\n'''{readme_content}'''\n"
                system_role = (
                    "Du bist der Support-Bot für das Projekt 'SL5 Aura'. "
                    "Nutze die folgende Dokumentation. Fasse dich kurz."
                )
                use_history = False
            else:
                return "Ich konnte die Readme-Datei nicht finden."

        # --- PROMPT BAUEN ---
        full_prompt = f"{system_role}\n"

        if use_history:
            history = load_history()
            if history:
                full_prompt += "\nVerlauf:\n"
                for entry in history:
                    role = "User" if entry['role'] == "user" else "Aura"
                    full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += f"{context_data}\nUser: {user_input_raw}\nAura:"

        log_debug(f"Prompt Länge: {len(full_prompt)} Zeichen.")

        # --- OLLAMA AUFRUF ---
        cmd = ["ollama", "run", "llama3.2"]

        log_debug("Sende Prompt via STDIN an Ollama...")

        # FIX: Timeout auf 90s erhöht
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=90
        )

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response = clean_text_for_typing(result.stdout.strip())

        if use_history:
            save_to_history(user_input_raw, response)

        return response

    except Exception as e:
        log_debug(f"FATAL: {e}")
        return f"Fehler: {str(e)}"
