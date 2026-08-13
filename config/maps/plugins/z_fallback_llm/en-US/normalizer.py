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

# config/maps/plugins/z_fallback_llm/de-DE/normalizer.py


import re

# from idna.idnadata import scripts


# import hashlib



import sys
from pathlib import Path

CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
# for _ in range(5):

# PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.parent


# Add the root directory to the Python path

# sys.path.append(str(PROJECT_ROOT_DIR))


# try:

# from scripts.py.func.audio_manager import * # noqa: F403 F401

# except ImportError as e:

# print(f"Error: Could not import 'audio_manager.py' as a module: {e}")

# utils.log_debug(f"Error: Could not import 'audio_manager' as a module: {e}")


# config/maps/plugins/z_fallback_llm/de-DE/normalizer.py

def _load_heavy_deps():
    global get_suggestions, utils
    try:
        from . import utils
    except ImportError:
        try:
            import utils
        except ImportError as e:
            raise RuntimeError(f"utils konnte nicht importiert werden: {e}")

    try:
        from config.maps.plugins.standard_actions.get_suggestions import get_suggestions # noqa: F401
    except ImportError as e:
        print(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
        utils.log_debug(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
        sys.exit(1)

# TODO: improve synonym




# ----------------------------------------------------

# DEFINITIONS:

# 1. The synonyms (from old function)

# 2. The extreme normalization (from last answer)

# ----------------------------------------------------


# (1) The synonyms that ensure a high match rate in the cache

COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",

    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",

    "lösche": "del", "entferne": "del", "vergiss": "del",

    # Contextual synonyms are risky but good for matches

    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}





def create_ultimate_cache_key(text):
    # -----------------------------------------------------

    # STEP 1: Synonym Replacement (The new, important step!)

    # -----------------------------------------------------

    text_lower = text.lower()
    words = text_lower.split()

    synonym_replaced_words = [COMMAND_SYNONYMS.get(word, word) for word in words]
    synonym_replaced_text = " ".join(synonym_replaced_words)

    # -----------------------------------------------------

    # STEP 2: Extreme Normalization (Stemming and Stopwords)

    # -----------------------------------------------------

    # Here we use the extremely aggressive function (extreme_standardize_prompt_text)

    # Note: This function must now contain the words 'new', 'info', 'del', 'rule' etc.

    # DO NOT remove from the stop word list because they come from the synonyms!


    final_cache_key = extreme_standardize_prompt_text(synonym_replaced_text)

    # Example:

    # prompt = "generate a new rule"

    # S1: "new a new rule"

    # S2: "new new rule" (after stemming and stop word removal)


    return final_cache_key

# ----------------------------------------------------

# ACTION:

# Perform the database migration with this

# new function 'create_ultimate_cache_key'!

# ----------------------------------------------------




def extreme_standardize_prompt_text(text):
    _load_heavy_deps()  # ensure utils is loaded

    # Initialize the German stemmer



    # 1. All lowercase

    text = text.lower()

    # 2. Replace ALL numbers, times and currency symbols with placeholders

    # EXAMPLE: 123. 123

    text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text)  # Z.B. '10', '10.5'
    # EXAMPLE: $

    text = re.sub(r'[€$£%]', ' ', text)

    # 3. Radical removal of almost all special characters and punctuation marks

    # EXAMPLE: a-zäöüß s

    text = re.sub(r'[^a-zäöüß\s]', ' ', text)

    # 4. Reduce whitespace to a single space and trim

    # EXAMPLE: 

    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Tokenization (separating words)

    words = text.split()

    # 6. Stop word removal and stemming

    stemmed_words = []
    for word in words:
        if word not in utils.STOP_WORDS_DE_EXTREME and len(word) > 8:
            stemmed_words.append(utils.GLOBAL_STEMMER.stem(word))
            # stemmed_words.append(stemmer.stem(word))


    unique_and_sorted_words = sorted(list(set(stemmed_words)))

    # 7. Reassemble words into a string

    text = ' '.join(unique_and_sorted_words)

    if not text:
        text = 'aura_empty_request'  # <-- Ein eindeutiger, kanonischer Fallback-Schlüssel

    # utils.log_debug(f"keywords<lastLine<extreme_standardize_prompt_text: 🔎 {text.strip()} 🔍")




    return text.strip()

