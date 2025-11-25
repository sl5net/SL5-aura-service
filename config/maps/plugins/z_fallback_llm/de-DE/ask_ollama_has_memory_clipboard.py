import subprocess
import re
import json


from pathlib import Path

# Versuch, pyperclip zu importieren. Wenn es fehlt, fangen wir das ab.
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py

MEMORY_FILE = Path(__file__).parent / "conversation_history.json"
MAX_HISTORY_ENTRIES = 6

def clean_text_for_typing(text):
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_clipboard_content():
    """
    Nutzt die Bibliothek 'pyperclip' für robusten Zugriff.
    """
    if not PYPERCLIP_AVAILABLE:
        print("DEBUG: 'pyperclip' ist nicht installiert in der .venv!")
        return None

    try:
        # Pyperclip versucht automatisch xclip, xsel, wl-clipboard etc.
        content = pyperclip.paste()

        # Leere Ergebnisse abfangen
        if not content or not content.strip():
            print("DEBUG: Pyperclip lieferte leeren String.")
            return None

        return content.strip()

    except Exception as e:
        print(f"DEBUG: Pyperclip Fehler: {e}")
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
            user_input = match_obj.group(2).strip()
        else:
            user_input = match_obj.group(1).strip()

        if not user_input: return "Ich habe nichts gehört."

        if "vergiss alles" in user_input.lower():
            if MEMORY_FILE.exists(): MEMORY_FILE.unlink()
            return "Gedächtnis gelöscht."

        # --- CLIPBOARD LOGIK ---
        trigger_words = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "das hier", "zusammenfassung"]
        clipboard_msg = ""

        if any(word in user_input.lower() for word in trigger_words):
            clipboard_content = get_clipboard_content()

            if clipboard_content:
                snippet = clipboard_content[:6000]
                clipboard_msg = f"\n\n--- ZWISCHENABLAGE ---\n{snippet}\n----------------------\n"
                if len(user_input.split()) < 3:
                    user_input += " (Beziehe dich auf die Zwischenablage)"
            else:
                # Fehlermeldung für das LLM
                clipboard_msg = "\n\n[SYSTEM: Clipboard leer oder Zugriff verweigert. Prüfe 'pip install pyperclip' in der venv.]\n"

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

        cmd = ["ollama", "run", "llama3.2", full_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=20)

        if result.returncode != 0: return f"Fehler: {result.stderr.strip()}"
        response_text = result.stdout.strip()
        if not response_text: return "Keine Antwort."

        clean_response = clean_text_for_typing(response_text)
        save_to_history(user_input, clean_response)
        return clean_response

    except subprocess.TimeoutExpired:
        return "Zeitüberschreitung."
    except Exception as e:
        return f"Fehler: {str(e)}"

