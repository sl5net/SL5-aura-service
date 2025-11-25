import subprocess
import re
import json
import os
import sys
import logging
import inspect
from pathlib import Path

# --- CONFIGURATION ---
MEMORY_FILE = Path(__file__).parent / "conversation_history.json"
MAX_HISTORY_ENTRIES = 6

# Optional: File logging
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

# --- ENVIRONMENT FIX (THE KEY) ---
# Wir holen uns das Home-Verzeichnis des Users dynamisch
user_home = os.path.expanduser("~")

# 1. DISPLAY setzen
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"

# 2. XAUTHORITY setzen (WICHTIG!)
# Ohne das darf ein Hintergrundprozess nicht auf X11 zugreifen
if "XAUTHORITY" not in os.environ:
    xauth_path = os.path.join(user_home, ".Xauthority")
    if os.path.exists(xauth_path):
        os.environ["XAUTHORITY"] = xauth_path
        log_debug(f"Environment: XAUTHORITY set to {xauth_path}")
    else:
        log_debug(f"WARNING: .Xauthority not found at {xauth_path}")

# Import Pyperclip
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    log_debug("WARNING: pyperclip not installed in .venv")

def clean_text_for_typing(text):
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_clipboard_content():
    """Reads clipboard using multiple fallback methods."""

    # Methode 1: Pyperclip (Standard)
    if PYPERCLIP_AVAILABLE:
        try:
            log_debug(f"Attempting pyperclip read. Disp={os.environ.get('DISPLAY')} XAuth={os.environ.get('XAUTHORITY')}")
            content = pyperclip.paste()
            if content and content.strip():
                log_debug(f"Clipboard (pyperclip) success. Len: {len(content)}")
                return content.strip()
        except Exception as e:
            log_debug(f"Pyperclip Error: {e}")

    # Methode 2: xclip direkt via Subprocess (mit Environment!)
    # Das hilft oft, wenn pyperclip die Pfade nicht findet
    try:
        log_debug("Fallback: Try 'xclip -o'...")
        res = subprocess.run(
            ['xclip', '-selection', 'clipboard', '-o'],
            capture_output=True,
            text=True,
            timeout=1,
            env=os.environ # WICHTIG: Das manipulierte Environment übergeben
        )
        if res.returncode == 0 and res.stdout.strip():
            log_debug(f"Clipboard (xclip) success. Len: {len(res.stdout)}")
            return res.stdout.strip()
    except Exception as e:
        log_debug(f"xclip Error: {e}")

    # Methode 3: wl-paste (Wayland Fallback)
    try:
        log_debug("Fallback: Try 'wl-paste'...")
        res = subprocess.run(
            ['wl-paste', '--no-newline'],
            capture_output=True,
            text=True,
            timeout=1,
            env=os.environ
        )
        if res.returncode == 0 and res.stdout.strip():
            log_debug(f"Clipboard (wl-paste) success. Len: {len(res.stdout)}")
            return res.stdout.strip()
    except Exception:
        pass

    log_debug("ALL clipboard methods failed.")
    return None

def load_history():
    if not MEMORY_FILE.exists(): return []
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception:
        return []

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
                final_context = f"\n\n--- KONTEXT (Zwischenablage) ---\n{clipboard_content[:8000]}\n--------------------------------\n"

                # Prompt umschreiben, wenn User nur "Lies Clipboard" sagt
                if len(user_input_raw.split()) < 5:
                    user_suffix = "Fasse den Kontext zusammen oder erkläre ihn."
                    log_debug("Prompt rewritten.")
            else:
                log_debug("Clipboard empty.")
                return "Ich konnte die Zwischenablage nicht lesen."

        # --- PROMPT ---
        history = load_history()
        base_instruction = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze), außer bei Analysen. Keine Emojis."

        full_prompt = f"{base_instruction}{final_context}\n\n"

        if history:
            full_prompt += "Verlauf:\n"
            for entry in history:
                role = "User" if entry['role'] == "user" else "Aura"
                full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += f"\nUser: {user_suffix}\nAura:"

        # --- OLLAMA ---
        cmd = ["ollama", "run", "llama3.2", full_prompt]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=30)

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response_text = result.stdout.strip()
        clean_response = clean_text_for_typing(response_text)
        save_to_history(user_input_raw, clean_response)

        return clean_response

    except Exception as e:
        log_debug(f"FATAL: {e}")
        return f"Fehler: {str(e)}"
