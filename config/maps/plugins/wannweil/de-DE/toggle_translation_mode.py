# config/maps/plugins/wannweil/de-DE/toggle_translation_mode.py
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
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} {e}")

def execute(match_data):
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

        if not found_anchor:
            error_msg = f"Fehler: Anker '{RULE_ANCHOR}' in der Regel-Datei nicht gefunden."
            print(error_msg, file=sys.stderr)
            speak("Fehler: Die Übersetzungsregel konnte nicht konfiguriert werden.")
            return

        # Zustand umschalten und Feedback geben
        if current_state == 'on':
            new_state = 'off'
            feedback_message = "Übersetzungsmodus wird ausgeschaltet."
            # Die Zeile auskommentieren
            lines[rule_line_index] = '#' + lines[rule_line_index]
        else: # current_state is 'off'
            new_state = 'on'
            feedback_message = "Übersetzungsmodus wird aktiviert."
            # Die Zeile einkommentieren (entferne führende '#' und Leerzeichen)
            lines[rule_line_index] = lines[rule_line_index].lstrip('#')


        # Schreibe die geänderten Zeilen zurück in die Datei
        RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')

        print(f"Status geändert zu: {new_state.upper()}. Regel-Datei wurde aktualisiert.")
        speak(feedback_message)

        # --- WICHTIG: SCHRITT 3 ---
        # Signalisiere der Hauptanwendung, dass sie die Regeln neu laden soll.
        # Eine einfache Methode ist, eine "Trigger-Datei" zu erstellen.
        (Path(__file__).parent / 'RELOAD_RULES.trigger').touch()
        print("Reload-Trigger wurde gesetzt.")


    except Exception as e:
        error_msg = f"Ein Fehler ist aufgetreten: {e}"
        print(error_msg, file=sys.stderr)
        speak("Es gab einen Fehler beim Ändern der Konfiguration.")
