# config/maps/plugins/standard_actions/language_translator/de-DE/toggle_translation_mode.py
# translation
import sys
from pathlib import Path
import subprocess

"""
    Vorteile:

        Sehr transparent: Ein Blick in die FUZZY_MAP_pre.py zeigt sofort den aktuellen Zustand.
        Keine Kern-Änderung: Die Logik der Regel-Engine selbst bleibt unberührt.
        Intuitiv: Aktivieren/Deaktivieren entspricht dem Auskommentieren, was Programmierer gewohnt sind.

    Nachteile:
        Dateizugriffe: Das System muss Schreibrechte auf seine eigenen Konfigurationsdateien haben, was manchmal ein Sicherheitsrisiko sein kann.

(S, 26.10.'25 12:22 Sun)
"""

# --- KONFIGURATION ---
# Der Pfad zur Regel-Datei, die wir bearbeiten wollen.
# Passe diesen Pfad an, damit er von diesem Skript aus korrekt ist.
# Angenommen, die Regeldatei liegt im selben Verzeichnis wie die Plugins.
RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
# Der eindeutige Anker-Kommentar, den wir suchen.
RULE_ANCHOR = '# TRANSLATION_RULE'

def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")

def execute(match_data):

    # temp = "('pt-BR', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|ein|einschalten|abs|deaktivieren|ausschalten"
    # temp1 = "('en', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (Englisch|ennglish"

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
    # ﻿Olá, como vai (original:'hallo wie geht's', Tradução de Voz SL5.de/Aura ).
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

        # Finde den Anker und den Zustand der Regelzeile
        for i, line in enumerate(lines):
            if RULE_ANCHOR in line:
                found_anchor = True
                # Die Regel ist die nächste Zeile
                rule_line_index = i + 1
                if rule_line_index < len(lines):
                    # Prüfen, ob die Zeile aktiv (nicht auskommentiert) ist
                    if not lines[rule_line_index].strip().startswith('#'):
                        current_state = 'on'
                break

        print("current_state:", current_state)

        if not found_anchor:
            error_msg = f"Fehler: Anker '{RULE_ANCHOR}' in der Regel-Datei nicht gefunden."
            print(error_msg, file=sys.stderr)
            speak("Fehler: Die Übersetzungsregel konnte nicht konfiguriert werden.")
            return

        # Zustand umschalten und Feedback geben
        if current_state == 'on':
            new_state = 'off'
            feedback_message = "translation mode is switched off (übersetzung modus wird ausgeschaltet')"
            # Die Zeile auskommentieren
            lines[rule_line_index] = '#' + lines[rule_line_index]
        else: # current_state is 'off'
            new_state = 'on'
            print("new_state:", new_state)
            feedback_message = "translation mode is switched on (übersetzung modus wird eingeschaltet')"
            # Die Zeile einkommentieren (entferne führende '#' und Leerzeichen)
            #lines[rule_line_index] = lines[rule_line_index].lstrip('# ')
            lines[rule_line_index] = lines[rule_line_index].lstrip('#')


        # write back to the file
        RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')

        print(f"Status geändert zu: {new_state.upper()}. Regel-Datei wurde aktualisiert.")
        speak(feedback_message)

        # --- WICHTIG: SCHRITT 3 ---
        # Signalisiere der Hauptanwendung, dass sie die Regeln neu laden soll.
        # Eine einfache Methode ist, eine "Trigger-Datei" zu erstellen.
        #(Path(__file__).parent / 'RELOAD_RULES.trigger').touch()
        # print("Reload-Trigger was set.")

        with open(Path(__file__).parent / 'translation_state.py', "w") as file:
            target_lang_as_variable_key = target_lang.strip().replace('-', '_')
            file.write(f"{target_lang_as_variable_key}='{new_state}'")

        return ' ' # text that is result. if you let it empty text you have spoken was written. if you want a empty result write ' '  because its intern not empty and will than accepted.

    except Exception as e:
        error_msg = f"Ein Fehler ist aufgetreten: {e}"
        print(error_msg, file=sys.stderr)
        speak("Es gab einen Fehler beim Ändern der Konfiguration.")

