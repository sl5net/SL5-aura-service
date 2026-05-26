# config/maps/plugins/wannweil/de-DE/toggle_translation_mode.py
import os
import sys
from pathlib import Path
import subprocess

# Project root for imports
PROJECT_ROOT = Path(__file__).parents[5]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.py.func.db.trino_client import get_translation_state, set_translation_state

# --- KONFIGURATION ---
RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
RULE_ANCHOR = '# TRANSLATION_RULE'
INTERFACE = os.getenv("AURA_INTERFACE", "terminal")

def speak(text):
    """Gibt Text ueber ein TTS-System aus."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} {e}")

def execute(match_data):
    """
    Liest den Translation-State aus Trino (interface-aware),
    toggled ihn und schreibt ihn zurueck.
    FUZZY_MAP_pre.py wird nur noch fuer Terminal geaendert.
    """
    target_lang = 'en'  # default, erweiterbar

    # State aus Trino lesen
    current_state = get_translation_state(interface=INTERFACE, target_lang=target_lang)
    print(f"[Trino] interface={INTERFACE} lang={target_lang} current_state={current_state}")

    # Toggle
    new_state = 'off' if current_state == 'on' else 'on'

    # State in Trino speichern
    set_translation_state(interface=INTERFACE, target_lang=target_lang, state=new_state)
    print(f"[Trino] new_state={new_state} gespeichert.")

    # FUZZY_MAP_pre.py nur fuer Terminal anpassen
    if INTERFACE == 'terminal':
        if not RULES_FILE_PATH.exists():
            print(f"Fehler: Regel-Datei nicht gefunden unter {RULES_FILE_PATH}", file=sys.stderr)
            speak("Fehler: Die Konfigurationsdatei wurde nicht gefunden.")
            return

        try:
            lines = RULES_FILE_PATH.read_text(encoding='utf-8').splitlines()
            found_anchor = False
            rule_line_index = -1

            for i, line in enumerate(lines):
                if RULE_ANCHOR in line:
                    found_anchor = True
                    rule_line_index = i + 1
                    break

            if not found_anchor:
                print(f"Fehler: Anker '{RULE_ANCHOR}' nicht gefunden.", file=sys.stderr)
                speak("Fehler: Die Uebersetzungsregel konnte nicht konfiguriert werden.")
                return

            if new_state == 'off':
                lines[rule_line_index] = '#' + lines[rule_line_index]
            else:
                lines[rule_line_index] = lines[rule_line_index].lstrip('#')

            RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print(f"FUZZY_MAP_pre.py aktualisiert: {new_state.upper()}")

            (Path(__file__).parent / 'RELOAD_RULES.trigger').touch()
            print("Reload-Trigger gesetzt.")

        except Exception as e:
            print(f"Fehler: {e}", file=sys.stderr)
            speak(f"Es gab einen Fehler beim Aendern der Konfiguration.")
            return

    # Feedback
    if new_state == 'on':
        speak("Uebersetzungsmodus wird aktiviert.")
    else:
        speak("Uebersetzungsmodus wird ausgeschaltet.")

    return ' '
