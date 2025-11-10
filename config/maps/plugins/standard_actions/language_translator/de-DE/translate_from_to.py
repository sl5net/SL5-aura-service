# In Ihrer CONFIG_DIR / 'translate_from_to.py'

import sys
from pathlib import Path
import subprocess

from config.settings import signatur_ar,signatur_en,signatur_pt_br,signatur_ja

#

STATE_FILE = Path(__file__).parent / 'translation_state.py'

project_dir = Path(__file__).parent.parent.parent.parent.parent.parent.parent

TRANSLATE_SCRIPT = project_dir / 'tools' / 'simple_translate.py'
PYTHON_EXECUTABLE = project_dir / '.venv' / 'bin' / 'python3'

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
        # Sprachübersetzung - Tradução de VozTesttest (original:'test', Voice Translation SL5.de/Aura Powered by SL5.de/Aura ).

        #

        if lang_target=='pt-BR' or lang_target=='pt-br' :
            return f"{translated_text} (original:'{original_text}', {signatur_pt_br}). "
        elif lang_target == 'en':
            return f"{translated_text} (original:'{original_text}', {signatur_en})."
        elif lang_target == 'ar':
            return f"{translated_text} (original:'{original_text}, {signatur_ar}). "
        elif lang_target == 'ja':
            return f"{translated_text} (original:'{original_text}, {signatur_ja}). "
        else:
            return f"{translated_text} (original:'{original_text}', {signatur_en}). "
        # ﻿Sprach Übersetzung﻿ar okay funktionieren ﻿sprach BesetzungBei der Übersetzung ist ein unerwarteter Fehler aufgetreten.

    except subprocess.CalledProcessError as e:
        # Das simple_translate.py Skript hat einen Fehler gemeldet.
        # Die Fehlermeldung steht in e.stderr.
        print(f"ERROR: [Translator Plugin] Fehler vom Übersetzungsskript: {e.stderr.strip()}", file=sys.stderr)
        return "Bei der Übersetzung ist ein Fehler aufgetreten."
    except Exception as e:
        print(f"ERROR: [Translator Plugin] Unerwarteter Fehler: {e}", file=sys.stderr)
        return "Bei der Übersetzung ist ein unerwarteter Fehler aufgetreten."
