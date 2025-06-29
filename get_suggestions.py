#!/usr/bin/env python3
import sys
import pyperclip
import requests
import subprocess
import logging
import os
import argparse
from pathlib import Path
import json
import nltk
nltk.download('wordnet', quiet=True)
from nltk.corpus import wordnet

# --- Configuration ---
LANGUAGETOOL_URL = "http://localhost:8082/v2/check"
XDOTOOL_PATH = "/usr/bin/xdotool"
LOGFILE = os.path.expanduser("~/projects/py/STT/get_suggestions.log")
GERMAN_THESAURUS_FILE = os.path.expanduser("~/projects/py/STT/openthesaurus-data.json")  # Adjust path as needed

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

# --- Load German Synonyms DB (from OpenThesaurus JSON) ---
def load_german_thesaurus(path):
    if not Path(path).exists():
        logging.error(f"German thesaurus file not found: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Build a fast lookup dictionary: word -> set([syn1, syn2, ...])
    synmap = {}
    for synset in data.get("synsets", []):
        terms = [term["term"] for term in synset.get("terms", [])]
        for term in terms:
            synmap.setdefault(term.lower(), set()).update([t for t in terms if t != term])
    return synmap

german_synonyms = load_german_thesaurus(GERMAN_THESAURUS_FILE)

def get_german_synonyms(word: str) -> list:
    """Get German synonyms from the loaded OpenThesaurus DB."""
    if not german_synonyms:
        return []
    return list(german_synonyms.get(word.lower(), []))

def get_suggestions(word: str) -> list:
    """Queries the LanguageTool server for suggestions for a single word."""
    suggestions = set()
    data = {
        'language': LT_LANGUAGE,
        'text': word,
        'level': 'picky',
        'maxSuggestions': 3
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

def get_english_synonyms(word: str) -> list:
    """Get English synonyms using NLTK WordNet."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym.lower() != word.lower():
                synonyms.add(synonym)
    return list(synonyms)

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

    # If no suggestions from LanguageTool, try synonyms
    if not suggestions:
        if LT_LANGUAGE == 'en-US':
            suggestions = get_english_synonyms(word_to_check)
            if suggestions:
                logging.info(f"Synonyms suggested for '{word_to_check}': {suggestions}")
        elif LT_LANGUAGE == 'de-DE':
            suggestions = get_german_synonyms(word_to_check)
            if suggestions:
                logging.info(f"German synonyms suggested for '{word_to_check}': {suggestions}")
        # Add more languages as needed

    if suggestions:
        output_string = f" ( {' | '.join(suggestions[:3])} )"
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
