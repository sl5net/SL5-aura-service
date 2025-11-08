# renumber_clipboard_text.py

import pyperclip
import re
import logging
import sys, os

from pathlib import Path
import subprocess
import time

script_file = Path(__file__).parent / 'renumber_clipboard_text.py'
project_dir = Path(__file__).parent.parent.parent.parent.parent.parent



CURRENT_DIR = Path(__file__).parent
# script_file_abs = CURRENT_DIR /

PYTHON_EXECUTABLE = project_dir / '.venv' / 'bin' / 'python3'

# --- Setup Logging ---
# Ensure logging is configured to follow the user's request for documentation via logger.info
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

if 'DISPLAY' not in os.environ:
    print(f"ERROR: DISPLAY environment variable is NOT set. Current environment: {os.environ}", file=sys.stderr)

description = """
Vorschlag für Sprachbefehl-Phrasen ( CMD_RENUMBER_CLIP ):

    Der kurze, prägnante Befehl:

        Trigger Phrase (EN): "Number Lines"

        Alternative: "Renumber Text"

    Der zielgerichtete Befehl (Fokus auf die Zwischenablage):

        Trigger Phrase (EN): "Number the Clipboard"

        Alternative: "Process Clip"

    Der vollständige, erklärende Befehl:

        Trigger Phrase (EN): "Add Sequential Line Numbers"

        Alternative: "Update Text Line Numbers"

deutsche Sprachbefehl-Phrasen, die leicht zu diktieren und spezifisch für die Funktion sind:

Vorschlag für Sprachbefehl-Phrasen (DE):

Der kurze, prägnante Befehl:

Trigger Phrase (DE): "Zeilen nummerieren"

Alternative: "Text neu nummerieren"

Der zielgerichtete Befehl (Fokus auf die Zwischenablage):

Trigger Phrase (DE): "Zwischenablage nummerieren"

Alternative: "Clip verarbeiten"

Der vollständige, erklärende Befehl:

Trigger Phrase (DE): "Laufende Zeilennummern einfügen"

Alternative: "Zeilennummern aktualisieren"


"""

def execute(match_data):

    # ENVIRONMENT VORBEREITEN
    env_vars = os.environ.copy()

    # Stellen Sie sicher, dass DISPLAY gesetzt ist, typischerweise ':0'
    # Dies ist nur notwendig, wenn der Parent (die Plugin-Engine) DISPLAY nicht korrekt übergibt
    if 'DISPLAY' not in env_vars:
        print("WARNING: DISPLAY not found in parent environment. Setting to ':0'.")
        env_vars['DISPLAY'] = ':0'

    command = [
        str(PYTHON_EXECUTABLE),
        str(script_file)
    ]

    full_command = ' '.join(command)
    print(f"INFO: [renumberClipboard] command: '{full_command}'")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env_vars  # <-- Verwenden Sie die manipulierte Umgebung
    )

    if result.returncode != 0:
        print(f"Child script failed. Stderr: {result.stderr}")

    print(f"{command}")
    main()
    return f"{full_command}"

#    return command Schrille und operiere Zeilesuggerieren




def renumber_text(raw_text: str) -> str:
    """Removes existing line numbers (e.g., '1:', '2: ') and renumbers the text sequentially from 1."""

    logger.info("Starting text renumbering process.")

    # Regex to match existing line numbers at the start of a line (e.g., '1:', ' 42: ')
    LINE_NUMBER_PATTERN = re.compile(r"^\s*\d+:\s*")

    # Split the text by lines. splitlines() handles different newline types.
    lines = raw_text.splitlines()
    renumbered_lines = []
    line_counter = 1

    for line in lines:
        logger.info(f"Processing original line {line_counter}.")

        # 1. Clean the line by removing any previous line number pattern
        cleaned_line = LINE_NUMBER_PATTERN.sub("", line)

        # Check if the line contains any content after stripping old numbering and whitespace.
        if cleaned_line.strip() == "":
            # If the line is empty or contained only whitespace/old numbering, append the number followed by only a colon
            renumbered_lines.append(f"{line_counter}:")
            logger.info("Line was empty/whitespace, retaining sequential numbering.")
        else:
            # 2. Add the new sequential line number and the cleaned content
            renumbered_lines.append(f"{line_counter}: {cleaned_line.strip()}")
            logger.info(f"Line content set to: {cleaned_line.strip()}")

        line_counter += 1

    logger.info(f"Processed total {len(lines)} lines. Renumbering complete.")

    return "\n".join(renumbered_lines)

def main():
    """Fetches text from clipboard, renumbers it, and pastes it back."""

    # Delay to ensure the clipboard is stable, especially when invoked via a hotkey/external command
    WAIT_TIME_SECONDS = 0.1
    logger.info(f"Waiting {WAIT_TIME_SECONDS} seconds to ensure clipboard stability.")
    time.sleep(WAIT_TIME_SECONDS) # <<< NEW DELAY


    try:
        logger.info("Attempting to read text from clipboard.")
        clipboard_content = pyperclip.paste()

        if not clipboard_content:
            logger.warning("Clipboard is empty. Exiting without action.")
            return

        original_length = len(clipboard_content)
        logger.info(f"Successfully retrieved {original_length} characters from clipboard.")

        new_content = renumber_text(clipboard_content)

        pyperclip.copy(new_content)
        logger.info("Renumbered text successfully copied back to the clipboard.")

    except pyperclip.PyperclipException as e:
        logger.error(f"Error accessing the clipboard. Pyperclip might require installation of system dependencies (e.g., xclip/xsel on Linux). Details: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during execution: {e}")

if __name__ == "__main__":
    main()
