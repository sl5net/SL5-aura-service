import subprocess
import re
import json
from pathlib import Path

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama_with_memory.py

# Speicherort für das Gedächtnis (im gleichen Ordner)
MEMORY_FILE = Path(__file__).parent / "conversation_history.json"
MAX_HISTORY_ENTRIES = 6  # Merkt sich die letzten 6 Wechsel (User + AI)

def clean_text_for_typing(text):
    """ Entfernt Emojis für xdotool Stabilität. """
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_history():
    """ Lädt den Verlauf und formatiert ihn als Text-Block für das LLM. """
    if not MEMORY_FILE.exists():
        return []

    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_to_history(user_text, ai_text):
    """ Speichert den neuen Austausch und hält die Liste kurz. """
    history = load_history()

    # Neuen Eintrag hinzufügen
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})

    # Nur die letzten N Einträge behalten (Sliding Window)
    # Wir nehmen MAX_HISTORY_ENTRIES * 2, da ein "Wechsel" aus 2 Einträgen besteht
    if len(history) > MAX_HISTORY_ENTRIES * 2:
        history = history[-(MAX_HISTORY_ENTRIES * 2):]

    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Fehler beim Speichern des Gedächtnisses: {e}")

def format_prompt_with_history(system_instruction, user_input, history):
    """ Baut den finalen Prompt zusammen. """
    full_prompt = f"{system_instruction}\n\n"

    if history:
        full_prompt += "Bisheriger Gesprächsverlauf:\n"
        for entry in history:
            role = "User" if entry['role'] == "user" else "Aura"
            full_prompt += f"{role}: {entry['content']}\n"

    full_prompt += f"\nUser: {user_input}\nAura:"
    return full_prompt

def execute(match_data):
    try:
        match_obj = match_data['regex_match_obj']

        # Regex Gruppen Logik (wie gehabt)
        if len(match_obj.groups()) >= 2:
            user_input = match_obj.group(2).strip()
        else:
            user_input = match_obj.group(1).strip()

        if not user_input:
            return "Ich habe nichts gehört."

        # Sonderbefehl: Gedächtnis löschen
        if "vergiss alles" in user_input.lower() or "neues gespräch" in user_input.lower():
            if MEMORY_FILE.exists():
                MEMORY_FILE.unlink()
            return "Okay, mein Kurzzeitgedächtnis ist gelöscht. Wir fangen von vorne an."

        # 1. Geschichte laden
        history = load_history()

        # 2. Prompt bauen
        system_instruction = (
            "Du bist Aura, ein hilfsbereiter Sprachassistent. "
            "Antworte auf Deutsch. Kurz und prägnant (max 2 Sätze). Keine Emojis."
        )
        full_prompt = format_prompt_with_history(system_instruction, user_input, history)

        # 3. Ollama aufrufen
        cmd = ["ollama", "run", "llama3.2", full_prompt]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=15 # Timeout leicht erhöht, da mehr Text verarbeitet wird
        )

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response_text = result.stdout.strip()

        if not response_text:
            return "Keine Antwort erhalten."

        # 4. Bereinigen
        clean_response = clean_text_for_typing(response_text)

        # 5. Speichern (Gedächtnis aktualisieren)
        save_to_history(user_input, clean_response)

        return clean_response

    except subprocess.TimeoutExpired:
        return "Das dauert zu lange."
    except Exception as e:
        return f"Fehler: {str(e)}"
