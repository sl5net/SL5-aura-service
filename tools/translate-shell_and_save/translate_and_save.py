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
TRANSLATION NOTE: The translation function
sudo pacman -S translate-shell
uses external online services (translate-shell). When this function is used, the text to be translated leaves your device and is subject to the privacy policies of the respective third-party provider (e.g., Google Translate). Do not use this function for confidential or internal data.

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
    try:
        # Befehl 1: Kopiere die Primary Selection (Auswahl)
        # in die Clipboard Selection (Strg+C)
        subprocess.run(
            shlex.split("xclip -selection primary -o"), # Hol Primary Selection
            capture_output=True,
            check=True,
            text=True
        )

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
    use 'translate-shell' (trans),
    """
    target_lang = target_lang.lower()
    if target_lang == 'pt':
        target_lang = 'pt-br'

    if target_lang not in ['de', 'en', 'pt', 'pt-br']:
         return f"[ERROR: target_lang: '{target_lang}' not suported]"

    if not text.strip():
        return ""

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

    slug_base = translated_text[:100]
    filename_slug = slugify(slug_base, max_length=MAX_SLUG_LENGTH)

    target_filepath = os.path.join(STORAGE_DIR, f"{filename_slug}.txt")

    file_content = (
        f"--- org ---\n"
        f"{original_text}\n\n"
        f"--- trans ({base_lang_code.upper()}) ---\n"
        f"{translated_text}\n"
    )

    try:
        with open(target_filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)

        return f"OK: saved '{filename_slug}.txt'", True
    except Exception as e:
        return f"ERROR saving: {e}", False

#
if __name__ == "__main__":


    HOME_DIR = os.environ.get("HOME", "/tmp") # $HOME Variable

    SPEAK_SCRIPT_PATH = os.path.join(HOME_DIR, "projects/py/TTS/speak_file.py")

    LOG_FILE_PATH = "/tmp/speak_error.log"

    # script.py [clipboard|TEXT] [TARGET_LANG] [OPTIONAL: SAVE]
    if len(sys.argv) < 3:
        print("Usage: python3 translate_and_save.py [clipboard|TEXT] [TARGET_LANG] [SAVE|NOSAVE]", file=sys.stderr)
        sys.exit(1)



    input_source = sys.argv[1]
    target_lang = sys.argv[2]
    should_save = len(sys.argv) > 3 and sys.argv[3].upper() == 'SAVE'

    text_to_translate = ""
    if input_source.lower() in ['clipboard', '-clipboard']:

        if not copy_selection_to_clipboard():
            sys.exit(1)


        try:
            text_to_translate = pyperclip.paste()
        except pyperclip.PyperclipException as e:
            print(f"[ERROR read pyperclip: {e}]", file=sys.stderr)
            sys.exit(1)
    else:
        text_to_translate = input_source

    translated_result = translate_text(text_to_translate, target_lang)

    if translated_result.startswith("[Fehler"):
        print(translated_result, file=sys.stderr)
        sys.exit(1)

    if should_save:

        save_msg, save_success = save_translation_as_file(text_to_translate, translated_result, target_lang)


    temp_file_path = None
    try:
        # a) temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(translated_result)
            temp_file_path = tmp.name # $f ist nun temp_file_path

        # b) python3 "$speak_file_path" "$temp_file_path" > log

        # -c "python3 /home/seeh/projects/py/TTS/speak_file.py %f > /tmp/speak_error.log 2>&1"

        python_bin = sys.executable
        # python_bin = '/home/seeh/projects/py/TTS/python3'
        python_bin   = "/home/seeh/projects/py/TTS/venv/bin/python3"

        cmd = [python_bin, SPEAK_SCRIPT_PATH, temp_file_path]

        with open(LOG_FILE_PATH, "a") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)

    except Exception as e:
        print(f"[Warnung: TTS: {e}]", file=sys.stderr)

    finally:

        print(f"python_bin={python_bin} SPEAK_SCRIPT_PATH={SPEAK_SCRIPT_PATH} temp_file_path={temp_file_path}")

        time.sleep(4)
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


    pyperclip.copy(translated_result)
    print(translated_result)

