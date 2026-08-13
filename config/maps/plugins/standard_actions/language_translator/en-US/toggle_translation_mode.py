# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/standard_actions/language_translator/de-DE/toggle_translation_mode.py

# translation

import os
import shutil
import sys
from pathlib import Path
import subprocess
import re

from scripts.py.func.config.dynamic_settings import settings

if settings.TRINO_ENABLED:
    from scripts.py.func.db.trino_client import set_feature_state, set_target_lang

"""
    Vorteile:

        Sehr transparent: Ein Blick in die FUZZY_MAP_pre.py zeigt sofort den aktuellen Zustand.
        Keine Kern-Änderung: Die Logik der Regel-Engine selbst bleibt unberührt.
        Intuitiv: Aktivieren/Deaktivieren entspricht dem Auskommentieren, was Programmierer gewohnt sind.

    Nachteile:
        Dateizugriffe: Das System muss Schreibrechte auf seine eigenen Konfigurationsdateien haben, was manchmal ein Sicherheitsrisiko sein kann.

(S, 26.10.'25 12:22 Sun)
"""

# --- CONFIGURATION ---

# The path to the rules file we want to edit.

# Adjust this path to be correct from this script.

# Assume that the rules file is in the same directory as the plugins.

RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
# The unique anchor comment we are looking for.

RULE_ANCHOR = '# TRANSLATION_RULE'

def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e33:
        print(f"33: STDOUT (TTS-Fallback): {e33}")
        speak(f"33: STDOUT (TTS-Fallback): Fehler {e33}")

def execute(match_data):

    # temp = "('pt-BR', r'^(portuguese|translation|translator) (activate|activated|active|on|turn on|abs|deactivate|turn off"

    # temp1 = "('en', r'^(Switch|Activate|activate|activated|active|switch on|deactivate|deactivate|switch off|look out|toggle) (English|ennglish"


    # original_text = match_data['original_text'].lower()

    # config/maps/plugins/standard_actions/language_translator/de-DE/toggle_translation_mode.py:41

    text_after_replacement = match_data['text_after_replacement'].lower()

    target_lang = text_after_replacement
    if text_after_replacement == 'pt-BR':
        target_lang = 'pt-BR'
    elif text_after_replacement == 'en':
        target_lang = 'en'

    # print("yyyyyyyyyyyyyyyyyyyyyyyyyyy")

    # print(f"original_text={original_text}")

    print(f"🌈 text_after_replacement={text_after_replacement}")
    # ufeffOlá, como vai (original: 'hello, how are you', Tradução de Voz SL5.de/Aura).

    # print(f"target_lang={target_lang}")

    # sys.exit(0)



    #
    # match_obj = match_data['regex_match_obj']


    # num1 = int(match_obj.group(1))

    # target_lang_matched_in_regex = match_obj.group(2).lower()

    # num2 = int(match_obj.group(3))



    """
    Liest die Regel-Datei, findet die Übersetzungsregel und kommentiert sie
    ein oder aus, um sie zu aktivieren oder zu deaktivieren.
    """
    if not RULES_FILE_PATH.exists():
        error_msg = f"Fehler: Regel-Datei nicht gefunden unter {RULES_FILE_PATH}"
        print(error_msg, file=sys.stderr)
        speak("Fehler: Die Konfigurationsdatei wurde nicht gefunden.")
        return

    try:
        lines = RULES_FILE_PATH.read_text(encoding='utf-8').splitlines()
        found_anchor = False
        rule_line_index = -1
        current_state = 'off' # Standardannahme

        # Find the anchor and state of the rule line

        for i, line in enumerate(lines):
            if RULE_ANCHOR in line:
                found_anchor = True
                # The rule is the next line

                rule_line_index = i + 1
                if rule_line_index < len(lines):
                    # Check whether the line is active (not commented out).

                    if not lines[rule_line_index].strip().startswith('#'):
                        current_state = 'on'
                break

        print("current_state:", current_state)

        if not found_anchor:
            error_msg = f"Fehler: Anker '{RULE_ANCHOR}' in der Regel-Datei nicht gefunden."
            print(error_msg, file=sys.stderr)
            speak("Fehler: Die Übersetzungsregel konnte nicht konfiguriert werden.")
            return

        if current_state == 'on':
            new_state = 'off'
            feedback_message = "translation mode is switched off (übersetzung modus wird ausgeschaltet')"
            # comment out rule in this rule file

            # lines[rule_line_index] = '#' + lines[rule_line_index]

            lines[rule_line_index] = re.sub(r'^(\s*)(.*)', r'\1#\2', lines[rule_line_index])
        else: # current_state is 'off'

            # create backup path (same name + .bak)

            backup_path = RULES_FILE_PATH.with_name(RULES_FILE_PATH.name + ".off.backup.py")

            # copy (overwrites existing backup)

            shutil.copy2(RULES_FILE_PATH, backup_path)

            new_state = 'on'


            print("new_state:", new_state)
            feedback_message = "translation mode is switched on (übersetzung modus wird eingeschaltet')"
            # Comment the line (remove leading '#' and spaces)

            # lines[rule_line_index] = lines[rule_line_index].lstrip('# ')

            # lines[rule_line_index] = lines[rule_line_index].lstrip('#')

            lines[rule_line_index] = lines[rule_line_index].replace('#', '', 1)


        INTERFACE = os.getenv("INTERFACE", "speech")

        trino_is_used = False

        if settings.TRINO_ENABLED:
            try:
                set_target_lang(INTERFACE, target_lang=target_lang)
                set_feature_state(INTERFACE, feature='translation', state=new_state)
                trino_is_used = True
                print("Trino-Updated.")
            except Exception as trino_err:
                print(f"note: optional Trino-Service ignored. ({trino_err})")
                trino_is_used = False

        # write back to the file

        RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')

        print(f"state now: {new_state.upper()}. rule-file updated.")
        speak(feedback_message)

        if not trino_is_used:
            (Path(__file__).parent / 'RELOAD_RULES.trigger').touch()
            print("Reload-Trigger was set.")

            with open(Path(__file__).parent / 'translation_state.py', "w") as file:
                target_lang_as_variable_key = target_lang.strip().replace('-', '_')
                file.write(f"{target_lang_as_variable_key}='{new_state}'")

        return ' ' # text that is result. if you let it empty text you have spoken was written. if you want a empty result write ' '  because its intern not empty and will than accepted.


    except Exception as e:
        error_msg = f"Error: {e}"
        print(error_msg, file=sys.stderr)
        speak(f"Es gab einen Fehler beim Ändern der Konfiguration. {e}")
