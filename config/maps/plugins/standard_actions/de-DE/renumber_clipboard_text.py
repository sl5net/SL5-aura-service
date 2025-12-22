# config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

import re
import logging
from pathlib import Path

# --- Configuration ---
# Bridge Input: The file continuously updated by the bash script FROM clipboard
CLIPBOARD_IN_FILE = Path("/tmp/aura_clipboard.txt")
# Bridge Output: The file checking by the bash script to write TO clipboard
CLIPBOARD_OUT_FILE = Path("/tmp/aura_clipboard_out.txt")

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def renumber_text(raw_text: str) -> str:
    """
    Removes existing line numbers and renumbers sequentially.
    """
    # Regex for "1: ", "  02:", etc.
    # EXAMPLE: s 123 s
    line_number_pattern = re.compile(r"^\s*\d+:\s*")

    lines = raw_text.splitlines()
    renumbered_lines = []
    line_counter = 1

    for line in lines:
        cleaned_line = line_number_pattern.sub("", line)

        if cleaned_line.strip() == "":
            renumbered_lines.append(f"{line_counter}:")
        else:
            renumbered_lines.append(f"{line_counter}: {cleaned_line.strip()}")

        line_counter += 1

    return "\n".join(renumbered_lines)

def execute(match_data):
    """
    Reads from bridge file, processes text, writes to output bridge file.
    """
    logger.info("Executing renumber_clipboard_text (File-Bridge Mode).")

    # 1. READ
    if not CLIPBOARD_IN_FILE.exists():
        logger.error(f"Input file not found: {CLIPBOARD_IN_FILE}")
        return "Error: Bridge input file missing."

    try:
        content = CLIPBOARD_IN_FILE.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to read input file: {e}")
        return "Error reading text."

    if not content:
        return "Clipboard is empty."

    # 2. PROCESS
    new_content = renumber_text(content)

    # 3. WRITE (Signal for the bash bridge)
    try:
        CLIPBOARD_OUT_FILE.write_text(new_content, encoding='utf-8')
        logger.info(f"Wrote processed text to {CLIPBOARD_OUT_FILE} for pickup.")
    except Exception as e:
        logger.error(f"Failed to write output file: {e}")
        return "Error saving processed text."

    return "Text renumbered. Waiting for bridge to update clipboard."
