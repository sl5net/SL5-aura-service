# translate_and_save.py
import subprocess
import sys
import pyperclip
import os
import time
import tempfile  # NEU: Wird benötigt für temporäre Datei
from slugify import slugify
# pip install python-slugify

"""
HINWEIS ZUR ÜBERSETZUNG: Die Übersetzungsfunktion
sudo pacman -S translate-shell
 nutzt externe Online-Dienste (translate-shell). Wenn diese Funktion verwendet wird, verlässt der zu übersetzende Text Ihr Gerät und unterliegt den Datenschutzrichtlinien des jeweiligen Drittanbieters (z.B. Google Translate). Verwenden Sie diese Funktion nicht für vertrauliche oder interne Daten.

Tested and works in copyQ:
bash -c "$HOME/projects/py/.venv/bin/python3 $HOME/projects/py/translate_and_save.py clipboard de SAVE"



/path/to/python3 ~/projects/py/translate_and_save.py clipboard de NOSAVE
/path/to/python3 ~/projects/py/translate_and_save.py clipboard de SAVE

/path/to/venv/bin/python3 $HOME/projects/py/translate_and_save.py clipboard de SAVE

# Innerhalb eines Python Skripts:
import os
expanded_path = os.path.expanduser("~/projects/py/translate_and_save.py")

"""

# --- Konfiguration ---
TRANSLATION_COMMAND = "trans"

# Konfiguration für das Speichern
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translations')
MAX_SLUG_LENGTH = 50
DEFAULT_SAVE_LANG = 'de' # Speichern basiert auf der DE Übersetzung

# === TEIL 1: ÜBERSETZUNGSFUNKTION (STABIL) ===


import subprocess
import sys
import pyperclip
import os
from slugify import slugify
import shlex


def copy_selection_to_clipboard() -> bool:
    """
    Kopiert den aktuell markierten Text (Primary Selection) in die
    Zwischenablage (Clipboard Selection), um ihn danach mit pyperclip.paste()
    lesen zu können. (Linux-spezifisch, nutzt xclip).
    """
    try:
        # Befehl 1: Kopiere die Primary Selection (Auswahl)
        # in die Clipboard Selection (Strg+C)
        subprocess.run(
            shlex.split("xclip -selection primary -o"), # Hol Primary Selection
            capture_output=True,
            check=True,
            text=True
        )
        # Die Ausgabe des ersten Kommandos muss nun in das Clipboard gepipet werden.
        # Da dies kompliziert ist, vereinfachen wir: xclip -i liest von stdin.
        # Aber das ist in Python fehleranfällig.

        # Der einfachste Weg: Simulate Strg+C via xdotool, ABER: xdotool ist extern.

        # WIR NUTZEN STATT DESSEN DIE ROBUSTE XCLIP KETTE DIREKT:
        # xclip -o | xclip -i -selection c

        # Wir müssen es in Bash ausführen, um die Pipe zu nutzen
        subprocess.run(
            "xclip -o | xclip -i -selection c",
            shell=True,
            check=True
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"[Fehler beim Kopieren der Auswahl: xclip-Aufruf fehlgeschlagen: {e.stderr.decode()}]", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("[Fehler: xclip nicht gefunden. Installation nötig.]", file=sys.stderr)
        return False








def translate_text(text: str, target_lang: str) -> str:
    """
    Übersetzt Text mithilfe von 'translate-shell' (trans),
    indem die Argumente direkt übergeben werden.
    """
    target_lang = target_lang.lower()
    if target_lang == 'pt':
        target_lang = 'pt-br'

    if target_lang not in ['de', 'en', 'pt', 'pt-br']:
         return f"[Fehler: Zielssprache '{target_lang}' wird nicht unterstützt.]"

    if not text.strip():
        return ""

    # Verwendung der stabilen Argumentenübergabe für trans
    cmd_args = [TRANSLATION_COMMAND, "-b", "--no-ansi", "-t", target_lang, text]

    try:
        result = subprocess.run(
            cmd_args,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return f"[Fehler: {e.stderr.strip()}]"
    except FileNotFoundError:
        return f"[Fehler: '{TRANSLATION_COMMAND}' nicht gefunden.]"


# === TEIL 2: SPEICHERFUNKTION (SLUGIFY) ===

def save_translation_as_file(original_text, translated_text, base_lang_code):
    """Speichert PT Original und Übersetzung (basierend auf der Basissprache)."""

    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    original_text = original_text.strip()
    translated_text = translated_text.strip()

    if not translated_text:
        return f"Fehler: Übersetzungstext ({base_lang_code}) ist leer.", False

    # Dateinamen-Basis (Slug) basiert auf der aktuellen Übersetzung
    slug_base = translated_text[:100]
    filename_slug = slugify(slug_base, max_length=MAX_SLUG_LENGTH)

    target_filepath = os.path.join(STORAGE_DIR, f"{filename_slug}.txt")

    # Annahme: Der Originaltext (PT) wird immer als PT markiert
    file_content = (
        f"--- Original ---\n"
        f"{original_text}\n\n"
        f"--- Übersetzung ({base_lang_code.upper()}) ---\n"
        f"{translated_text}\n"
    )

    try:
        with open(target_filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)

        return f"Erfolg: Gespeichert als '{filename_slug}.txt'", True
    except Exception as e:
        return f"Fehler beim Speichern: {e}", False


# === HAUPTPROGRAMM ===

if __name__ == "__main__":


    HOME_DIR = os.environ.get("HOME", "/tmp") # $HOME Variable

    SPEAK_SCRIPT_PATH = os.path.join(HOME_DIR, "projects/py/TTS/speak_file.py")

    LOG_FILE_PATH = "/tmp/speak_error.log"

    # Nutzung: script.py [clipboard|TEXT] [TARGET_LANG] [OPTIONAL: SAVE]
    if len(sys.argv) < 3:
        print("Usage: python3 translate_and_save.py [clipboard|TEXT] [TARGET_LANG] [SAVE|NOSAVE]", file=sys.stderr)
        sys.exit(1)



    input_source = sys.argv[1]
    target_lang = sys.argv[2]
    should_save = len(sys.argv) > 3 and sys.argv[3].upper() == 'SAVE'

    # 1. Text besorgen (PT Original oder was auch immer in der Zwischenablage ist)
    text_to_translate = ""
    if input_source.lower() in ['clipboard', '-clipboard']:

        # NEU: Kopiere zuerst die Auswahl in das Clipboard, falls noch nicht geschehen
        if not copy_selection_to_clipboard():
            sys.exit(1)


        try:
            text_to_translate = pyperclip.paste()
        except pyperclip.PyperclipException as e:
            print(f"[Fehler beim Lesen der Zwischenablage: {e}]", file=sys.stderr)
            sys.exit(1)
    else:
        text_to_translate = input_source

    # 2. Übersetzen
    translated_result = translate_text(text_to_translate, target_lang)

    # Prüfen auf Übersetzungsfehler
    if translated_result.startswith("[Fehler"):
        print(translated_result, file=sys.stderr)
        sys.exit(1)

    # 3. Speichern, falls angefordert
    if should_save:
        # HINWEIS: Wir nehmen an, dass der Text_to_translate der PT-Originaltext ist,
        # der in der Datenbank gespeichert werden soll.
        save_msg, save_success = save_translation_as_file(text_to_translate, translated_result, target_lang)

        # Optional: Gib die Speichernachricht zusätzlich aus (oder logge sie)
        # print(save_msg)

   # 4. SPRACHAUSGABE (Der kritische neue Teil)
    temp_file_path = None
    try:
        # a) Erstelle temporäre Datei und schreibe deutschen Text hinein
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(translated_result)
            temp_file_path = tmp.name # $f ist nun temp_file_path

        # b) Befehl ausführen: python3 "$speak_file_path" "$temp_file_path" > log

        # -c "python3 /home/seeh/projects/py/TTS/speak_file.py %f > /tmp/speak_error.log 2>&1"

        python_bin = sys.executable
        # python_bin = '/home/seeh/projects/py/TTS/python3'
        python_bin   = "/home/seeh/projects/py/TTS/venv/bin/python3"

        cmd = [python_bin, SPEAK_SCRIPT_PATH, temp_file_path]

        with open(LOG_FILE_PATH, "a") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)

    except Exception as e:
        # Fehler beim Speak-Prozess wird nur geloggt, aber Hauptprozess läuft weiter
        print(f"[Warnung: Fehler bei TTS-Ausgabe: {e}]", file=sys.stderr)

    finally:
        # c) Temporäre Datei aufräumen

        print(f"python_bin={python_bin} SPEAK_SCRIPT_PATH={SPEAK_SCRIPT_PATH} temp_file_path={temp_file_path}")

        time.sleep(4)
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


    # 5. Ergebnis ausgeben (immer, wenn erfolgreich übersetzt)
    pyperclip.copy(translated_result)
    print(translated_result)

