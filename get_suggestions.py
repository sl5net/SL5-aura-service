#!/usr/bin/env python3
import sys
import pyperclip
import requests
import subprocess
import logging
import os
import argparse
from pathlib import Path

# curl -X POST -d 'language=de-DE&text=Mond&level=picky&maxSuggestions=2' http://localhost:8082/v2/check
# OpenThesaurus.de: https://www.openthesaurus.de/synonyme/search?q=Mond&format=application/json

# --- Configurationio nix   ( nichts )---
LANGUAGETOOL_URL = "http://localhost:8082/v2/check"
XDOTOOL_PATH = "/usr/bin/xdotool"
LOGFILE = os.path.expanduser("~/projects/py/STT/get_suggestions.log")

def guess_lt_language_from_model(model_name):
    name = model_name.lower()
    if "-de-" in name:
        return "de-DE"
    elif "-en-" in name:
        return "en-US"
    elif "-fr-" in name:
        return "fr-FR"
    return "de-DE"

MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="LanguageTool suggestion helper.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
args = parser.parse_args()

SCRIPT_DIR = Path(__file__).resolve().parent
VOSK_MODEL_FILE = "/tmp/vosk_model"
vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / MODEL_NAME

LT_LANGUAGE = guess_lt_language_from_model(MODEL_NAME)

# --- Setup Logging ---
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

def get_suggestions(word: str) -> list:
    """Queries the LanguageTool server for suggestions for a single word."""
    suggestions = set()
    data = {
        'language': LT_LANGUAGE,
        'text': word,
        'level': 'picky',
        'maxSuggestions': 2
    }

    try:
        response = requests.post(LANGUAGETOOL_URL, data=data, timeout=2)
        response.raise_for_status()
        matches = response.json().get('matches', [])
        for match in matches:
            for replacement in match.get('replacements', []):
                suggestions.add(replacement['value'])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying LanguageTool: {e}")
        return []

    return list(suggestions)

def main():
    try:
        word_to_check = pyperclip.paste().strip()
    except Exception as e:
        logging.error(f"Error accessing clipboard: {e}")
        word_to_check = ""

    if not word_to_check or ' ' in word_to_check or len(word_to_check) > 50:
        logging.info("Clipboard content invalid or empty.")
        sys.exit()

    logging.info(f"Checking word: {LT_LANGUAGE}: '{word_to_check}'")
    suggestions = get_suggestions(word_to_check)

    if suggestions:
        output_string = f" ( {' | '.join(suggestions[:2])} )"
        try:
            subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", output_string])
            logging.info(f"Suggestions typed: {output_string}")
        except FileNotFoundError:
            logging.error(f"xdotool not found at {XDOTOOL_PATH}")
        except Exception as e:
            logging.error(f"Error typing suggestions: {e}")
    else:
        logging.info("No suggestions found or error occurred.")

if __name__ == "__main__":
    main()
