import subprocess
import re

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py

def clean_text_for_typing(text):
    """
    Entfernt Emojis und problematische Sonderzeichen, die xdotool crashen lassen.
    Behält deutsche Umlaute und normale Satzzeichen.
    """
    # 1. Emojis und exotische Unicode-Zeichen entfernen
    # Dieser Regex erlaubt nur Wortzeichen, Whitespace und gängige Satzzeichen.
    # Alles andere (wie 😂, 🚀) wird gelöscht.
    text = re.sub(r'[^\w\s\.,!\?\-\(\)äöüÄÖÜß:;\'"]', '', text)

    # 2. Doppelte Leerzeichen bereinigen
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def execute(match_data):
    """
    Sends the captured text to the local Ollama instance (llama3.2).

    """
    try:
        match_obj = match_data['regex_match_obj']

        # Gruppe 2 nutzen, da Gruppe 1 jetzt das Trigger-Wort ist (z.B. "Aura")
        # Sicherstellen, dass wir den richtigen Index greifen, falls sich die Regex ändert.
        # Bei deiner Regex: ^(Aura|...) (.*)$ ist (.*) Gruppe 2.
        if len(match_obj.groups()) >= 2:
            user_input = match_obj.group(2).strip()
        else:
            # Fallback, falls Regex anders aufgebaut ist
            user_input = match_obj.group(1).strip()

        if not user_input:
            return "Ich habe nichts gehört."

        # System prompt: Kurz, Deutsch, keine Emojis (zur Sicherheit auch hier sagen)
        system_instruction = "Antworte auf Deutsch. Maximal 2 Sätze. Benutze KEINE Emojis."
        full_prompt = f"{system_instruction}\nUser: {user_input}"

        cmd = ["ollama", "run", "llama3.2", full_prompt]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response_text = result.stdout.strip()

        if not response_text:
            return "Keine Antwort erhalten."

        # WICHTIG: Text säubern, damit der Type-Watcher nicht abstürzt
        clean_response = clean_text_for_typing(response_text)

        return clean_response

    except subprocess.TimeoutExpired:
        return "Die KI antwortet nicht schnell genug."
    except Exception as e:
        return f"Fehler: {str(e)}"
