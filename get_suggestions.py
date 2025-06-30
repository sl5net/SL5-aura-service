#!/usr/bin/env python3
import sys
import pyperclip
import requests
import subprocess
import logging
import os
import argparse
import json
import time
from pathlib import Path
from typing import Dict, Set, List

# --- Dependency Imports ---
try:
    import nltk
    from nltk.corpus import wordnet
    from cologne_phonetics import encode as cologne_encode
    import jellyfish
except ImportError as e:
    print(f"Error: A required library is missing: {e}")
    sys.exit(1)

# --- Constants & Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR
LOGFILE = PROJECT_DIR / "get_suggestions.log"
LOCK_FILE = Path("/tmp/get_suggestions.lock")
TIMESTAMP_FILE = Path("/tmp/get_suggestions.timestamp")
COOLDOWN_SECONDS = 2

LANGUAGETOOL_URL = "http://localhost:8082/v2/check"
XDOTOOL_PATH = "/usr/bin/xdotool"
NUM_SUGGESTIONS = 5
VOSK_MODEL_FILE = Path("/tmp/vosk_model")

GERMAN_THESAURUS_FILE = PROJECT_DIR / "openthesaurus.txt"
ENGLISH_WORD_LIST_FILE = PROJECT_DIR / "en_thesaurus.txt"

# --- Setup Logging ---
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# --- One-Time Setup ---
def ensure_nltk_data():
    try: nltk.data.find('corpora/wordnet.zip')
    except nltk.downloader.DownloadError:
        print("Downloading NLTK 'wordnet' corpus...")
        nltk.download('wordnet', quiet=False)

def ensure_english_word_list():
    if not ENGLISH_WORD_LIST_FILE.exists():
        print(f"'{ENGLISH_WORD_LIST_FILE}' not found. Creating it...")
        try: nltk.data.find('corpora/words.zip')
        except nltk.downloader.DownloadError:
            print("Downloading NLTK 'words' corpus...")
            nltk.download('words', quiet=False)
        from nltk.corpus import words
        with open(ENGLISH_WORD_LIST_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(words.words()))
        print(f"'{ENGLISH_WORD_LIST_FILE}' created.")

# --- Caching and Data Loading ---
_cache = {}
def load_or_create_cache(source_path: Path, creation_func, *args):
    cache_path = source_path.with_suffix(f"{source_path.suffix}.{creation_func.__name__}.cache.json")
    if str(cache_path) in _cache: return _cache[str(cache_path)]
    if (cache_path.exists() and source_path.exists() and cache_path.stat().st_mtime > source_path.stat().st_mtime):
        logging.info(f"Loading from cache: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                for key in data: data[key] = set(data[key])
            _cache[str(cache_path)] = data
            return data
    logging.info(f"Cache is old or missing. Generating from {source_path} using {creation_func.__name__}")
    data = creation_func(source_path, *args)
    json_safe_data = {k: list(v) for k, v in data.items()} if isinstance(data, dict) else data
    with open(cache_path, "w", encoding="utf-8") as f: json.dump(json_safe_data, f)
    _cache[str(cache_path)] = data
    return data

def create_thesaurus_phonetic_index(path: Path) -> Dict[str, Set[str]]:
    phonetic_index = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_content = line.strip()
            if not line_content or line_content.startswith("#"): continue
            terms = [t.strip() for t in line_content.split(";") if t.strip()]
            for term in terms:
                key = term.lower()
                try:
                    code = cologne_encode(key)[0][1]
                    if code in phonetic_index:
                        phonetic_index[code].add(key)
                    else:
                        phonetic_index[code] = {key}
                except (IndexError, TypeError):
                    logging.warning(f"Could not generate code for '{key}'")
    return phonetic_index

def create_wordlist_phonetic_index(path: Path) -> Dict[str, Set[str]]:
    phonetic_index = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            term = line.strip().lower()
            if not term: continue
            code = jellyfish.soundex(term)
            if code in phonetic_index:
                phonetic_index[code].add(term)
            else:
                phonetic_index[code] = {term}
    return phonetic_index

def create_synonym_map(path: Path) -> Dict[str, Set[str]]:
    synonyms = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or ";" not in line: continue
            terms = {t.strip().lower() for t in line.split(";") if t.strip()}
            for term in terms:
                syns = terms - {term}
                if term in synonyms: synonyms[term].update(syns)
                else: synonyms[term] = syns
    return synonyms

# --- Suggestion Logic ---
def get_phonetically_similar(word: str, phonetic_index: Dict[str, Set[str]], language: str) -> List[str]:
    word_lower = word.lower()
    try:
        if language == "de-DE":
            word_code = cologne_encode(word_lower)[0][1]
        else:
            word_code = jellyfish.soundex(word_lower)
    except (IndexError, TypeError):
        return []

    similar_words = phonetic_index.get(word_code, set()) - {word_lower}
    if not similar_words: return []

    ordered = sorted(similar_words, key=lambda w: jellyfish.levenshtein_distance(word_lower, w))
    return ordered[:NUM_SUGGESTIONS]

def get_suggestions_from_lt(word: str, language: str) -> List[str]:
    try:
        response = requests.post(LANGUAGETOOL_URL, data={'language': language, 'text': word}, timeout=1.0)
        response.raise_for_status()
        return list({r['value'] for m in response.json().get('matches', []) for r in m.get('replacements', [])})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying LanguageTool: {e}")
        return []

def get_english_synonyms(word: str) -> List[str]:
    synonyms = {l.name().replace('_', ' ') for s in wordnet.synsets(word) for l in s.lemmas()}
    synonyms.discard(word.lower())
    return list(synonyms)[:NUM_SUGGESTIONS]

def guess_lt_language_from_model(model_name: str) -> str:
    name = model_name.lower()
    if "-de-" in name: return "de-DE"
    if "-en-" in name: return "en-US"
    if "-fr-" in name: return "fr-FR"
    return "de-DE"

def main():
    if TIMESTAMP_FILE.exists() and time.time() - TIMESTAMP_FILE.stat().st_mtime < COOLDOWN_SECONDS:
        logging.warning("Cooldown active. Exiting.")
        sys.exit(1)
    if LOCK_FILE.exists():
        logging.warning("Script is already running. Exiting.")
        sys.exit(1)

    try:
        LOCK_FILE.touch()
        ensure_nltk_data()
        ensure_english_word_list()

        parser = argparse.ArgumentParser(description="Get suggestions.")
        args, _ = parser.parse_known_args()

        vosk_model_from_file = VOSK_MODEL_FILE.read_text().strip() if VOSK_MODEL_FILE.exists() else ""
        model_name = vosk_model_from_file or "vosk-model-de-0.21"
        lt_language = guess_lt_language_from_model(model_name)

        try:
            word_to_check = pyperclip.paste().strip()
            if not word_to_check or ' ' in word_to_check or len(word_to_check) > 50:
                word_to_check = "Huas"
        except Exception:
            word_to_check = "Huas"

        logging.info(f"Processing '{word_to_check}' for language '{lt_language}'")
        suggestions = get_suggestions_from_lt(word_to_check, lt_language)

        if not suggestions:
            if lt_language == 'de-DE':
                phonetic_index = load_or_create_cache(GERMAN_THESAURUS_FILE, create_thesaurus_phonetic_index)
                suggestions = get_phonetically_similar(word_to_check, phonetic_index, 'de-DE')
                if not suggestions:
                    synonym_map = load_or_create_cache(GERMAN_THESAURUS_FILE, create_synonym_map)
                    suggestions = list(synonym_map.get(word_to_check.lower(), []))[:NUM_SUGGESTIONS]

            elif lt_language == 'en-US':
                # --- THIS LOGIC IS NOW CORRECT ACCORDING TO YOUR PRIORITY ---
                # 1. Phonetic search is MOST IMPORTANT
                phonetic_index = load_or_create_cache(ENGLISH_WORD_LIST_FILE, create_wordlist_phonetic_index)
                suggestions = get_phonetically_similar(word_to_check, phonetic_index, 'en-US')

                # 2. Synonyms are the LAST RESORT
                if not suggestions:
                    suggestions = get_english_synonyms(word_to_check)

        if suggestions:
            unique_suggestions = list(dict.fromkeys(suggestions))
            output_string = f" ( {' | '.join(unique_suggestions[:NUM_SUGGESTIONS])} )"
            print(f"--> Found suggestions. Typing: {output_string}")
            try:
                subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", output_string], check=True)
                TIMESTAMP_FILE.touch()
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                logging.error(f"Failed to type with xdotool: {e}")
        else:
            print(f"--> No suggestions found for '{word_to_check}'.")
    finally:
        if LOCK_FILE.exists(): LOCK_FILE.unlink()

if __name__ == "__main__":
    main()
