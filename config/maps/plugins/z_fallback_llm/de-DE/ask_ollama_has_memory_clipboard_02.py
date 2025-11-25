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

# Optional: File logging as backup (same as in your example)
LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- LOGGING HELPER (From wikipedia_local.py) ---
def log_debug(message: str):
    """
    Prints debug info to stderr so it appears in the main Aura log stream.
    Includes filename and line number of the caller.
    """
    caller_info = "UNKNOWN:0"
    stack = inspect.stack()
    if len(stack) > 1:
        try:
            filename = os.path.basename(stack[1].filename)
            line_number = stack[1].lineno
            caller_info = f"{filename}:{line_number}"
        except Exception:
            pass
    # Using sys.stderr ensures it bypasses buffering and shows up in systemd/console
    print(f"[DEBUG_LLM] {caller_info}: {message}", file=sys.stderr)
    # Also write to file for persistence
    logging.info(f"{caller_info}: {message}")

# --- ENVIRONMENT FIX ---
# Ensure DISPLAY is set for background process clipboard access
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"

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
    """Reads clipboard using pyperclip with logging."""
    if not PYPERCLIP_AVAILABLE:
        return None

    try:
        log_debug(f"Attempting clipboard read. Env DISPLAY={os.environ.get('DISPLAY')}")
        content = pyperclip.paste()

        if content and content.strip():
            log_debug(f"Clipboard read success. Length: {len(content)}")
            return content.strip()
        else:
            log_debug("Clipboard is empty or None returned.")
            return None
    except Exception as e:
        log_debug(f"Clipboard Error: {e}")
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
    except Exception as e:
        log_debug(f"History Save Error: {e}")

def execute(match_data):
    try:
        match_obj = match_data['regex_match_obj']
        # Determine user input from regex groups
        if len(match_obj.groups()) >= 2:
            user_input_raw = match_obj.group(2).strip()
        else:
            user_input_raw = match_obj.group(1).strip()

        log_debug(f"Input received: '{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        if "vergiss alles" in user_input_raw.lower():
            if MEMORY_FILE.exists(): MEMORY_FILE.unlink()
            log_debug("Memory cleared by user request.")
            return "Gedächtnis gelöscht."

        # --- CLIPBOARD LOGIC ---
        trigger_words = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "das hier", "zusammenfassung"]

        final_prompt_context = ""
        user_prompt_suffix = user_input_raw

        if any(word in user_input_raw.lower() for word in trigger_words):
            log_debug("Clipboard trigger detected.")
            clipboard_content = get_clipboard_content()

            if clipboard_content:
                # Inject clipboard content as context
                final_prompt_context = f"\n\n--- KONTEXT (Zwischenablage) ---\n{clipboard_content[:8000]}\n--------------------------------\n"

                # If the user just asked "What is in clipboard?", guide the LLM to summarize/state it
                if len(user_input_raw.split()) < 5:
                    user_prompt_suffix = "Fasse den Inhalt der Zwischenablage zusammen oder gib ihn wieder."
                    log_debug("Prompt rewritten for summarization.")
            else:
                log_debug("Clipboard was empty/inaccessible.")
                return "Ich konnte die Zwischenablage nicht lesen."

        # --- CONSTRUCT FULL PROMPT ---
        history = load_history()
        base_instruction = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze), außer bei Zusammenfassungen. Keine Emojis."

        full_prompt = f"{base_instruction}{final_prompt_context}\n\n"

        if history:
            full_prompt += "Verlauf:\n"
            for entry in history:
                role = "User" if entry['role'] == "user" else "Aura"
                full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += f"\nUser: {user_prompt_suffix}\nAura:"

        # --- CALL OLLAMA ---
        log_debug("Calling Ollama subprocess...")
        cmd = ["ollama", "run", "llama3.2", full_prompt]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=30)

        if result.returncode != 0:
            log_debug(f"Ollama Error: {result.stderr.strip()}")
            return f"Fehler: {result.stderr.strip()}"

        response_text = result.stdout.strip()
        log_debug(f"Ollama Response: '{response_text[:100]}...'") # Log first 100 chars

        clean_response = clean_text_for_typing(response_text)
        save_to_history(user_input_raw, clean_response)

        return clean_response

    except Exception as e:
        log_debug(f"FATAL EXCEPTION: {e}")
        return f"Systemfehler: {str(e)}"

