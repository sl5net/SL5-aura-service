# In Ihrer CONFIG_DIR / 'translate_german_to_portuguese.py'

import sys
from pathlib import Path
import subprocess

# Pfad zur Statusdatei
STATE_FILE = Path(__file__).parent / 'translation_state.py'

# --- KONFIGURATION für das externe Übersetzungstool ---
# Python-Interpreter für das neue Skript
PYTHON_EXECUTABLE = Path.home() / 'projects' / 'py' / 'STT' / '.venv' / 'bin' / 'python3'
# WICHTIG: Pfad zum NEUEN, sauberen Skript
TRANSLATE_SCRIPT = Path.home() / 'projects' / 'py' / 'STT' / 'tools' / 'simple_translate.py' # ANPASSEN, falls der Pfad anders ist

def execute(match_data):
    """
    Prüft den Übersetzungsmodus. Wenn aktiv, wird der Text mit dem sauberen
    simple_translate.py Skript übersetzt und das Ergebnis zurückgegeben.
    """
    # 1. Prüfen, ob der Übersetzungsmodus aktiv ist
    original_text = match_data.get('original_text')

    # match_obj = match_data['regex_match_obj']

    # ('', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (Englisch|ennglish\w*)\b', 95, {

    # = int(match_obj.group(1))
    # operator = match_obj.group(2).lower()
    # lang_target = int(match_obj.group(3))



    #

    if not STATE_FILE.exists():
        return original_text  # Modus aus, nichts tun

    content = STATE_FILE.read_text().strip().lower()
    if "='on'" not in content:
        return original_text  # Modus aus, nichts tun

    key, value = content.split('=', 1)

    # Prefix speichern (entfernt Leerzeichen)
    lang_target = key.strip()
    lang_target = lang_target.strip().replace('_', '-')

    # 'pt-BR' # Ziel: Brasilianisches Portugiesisch
    # 'ar' # Ziel: arabisch

    try:
        if not original_text:
            return None # Kein Text zum Übersetzen

        print(f"INFO: [Translator Plugin] trnslate: '{original_text}'")

        # 2. Das NEUE, saubere Übersetzungsskript aufrufen
        command = [
            str(PYTHON_EXECUTABLE),
            str(TRANSLATE_SCRIPT),
            original_text,
            str(lang_target)

        ]

        print(f"67: yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        print(f"INFO: [Translator Plugin] Translation command: '{' '.join(command)}'")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # Löst einen Fehler aus, wenn simple_translate.py mit sys.exit(1) endet
            encoding='utf-8'
        )


        translated_text = result.stdout.strip()

        # 3. Das reine Ergebnis zurückgeben, damit der Service es sprechen kann
        # Sprachübersetzung - Tradução de Voz

        if lang_target=='pt-BR' or lang_target=='pt-br' :
            return f"{translated_text} (original:'{original_text}', Tradução de Voz SL5.de/Aura ). "
        elif lang_target == 'en':
            return f"{translated_text} (original:'{original_text}', Voice Translation SL5.de/Aura ). "
        elif lang_target == 'ar':
            return f"{translated_text} (original:'{original_text}, SL5.de/Aura  تحدثت الترجمة). "
        else:
            return f"{translated_text} (original:'{original_text}', Voice Translation SL5.de/Aura ). "
        # ﻿Sprach Übersetzung﻿ar okay funktionieren ﻿sprach Besetzung

    except subprocess.CalledProcessError as e:
        # Das simple_translate.py Skript hat einen Fehler gemeldet.
        # Die Fehlermeldung steht in e.stderr.
        print(f"ERROR: [Translator Plugin] Fehler vom Übersetzungsskript: {e.stderr.strip()}", file=sys.stderr)
        return "Bei der Übersetzung ist ein Fehler aufgetreten."
    except Exception as e:
        print(f"ERROR: [Translator Plugin] Unerwarteter Fehler: {e}", file=sys.stderr)
        return "Bei der Übersetzung ist ein unerwarteter Fehler aufgetreten."
