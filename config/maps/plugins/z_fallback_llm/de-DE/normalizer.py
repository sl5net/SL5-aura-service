import re

from idna.idnadata import scripts

#import hashlib
from . import utils


import sys
from pathlib import Path

CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
# for _ in range(5):
#     PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.parent

# Fügen Sie das Stammverzeichnis zum Python-Pfad hinzu
# sys.path.append(str(PROJECT_ROOT_DIR))

try:
    from scripts.py.func.audio_manager import *
except ImportError as e:
    print(f"Fehler: Konnte 'audio_manager.py' nicht als Modul importieren: {e}")
    utils.log_debug(f"Fehler: Konnte 'audio_manager' nicht als Modul importieren: {e}")
try:
    from config.maps.plugins.standard_actions.get_suggestions import get_suggestions # noqa: F401
except ImportError as e:
    print(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
    utils.log_debug(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
    sys.exit(1)

# TODO: synonym verbessern



# ----------------------------------------------------
# DEFINITIONEN:
# 1. Die Synonyme (aus alter Funktion)
# 2. Die extreme Normalisierung (aus letzter Antwort)
# ----------------------------------------------------

# (1) Die Synonyme, die für eine hohe Match-Rate im Cache sorgen
COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",

    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",

    "lösche": "del", "entferne": "del", "vergiss": "del",

    # Kontext-Synonyme sind riskant, aber gut für Matches
    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}





def create_ultimate_cache_key(text):
    # -----------------------------------------------------
    # SCHRITT 1: Synonym-Ersetzung (Der neue, wichtige Schritt!)
    # -----------------------------------------------------
    text_lower = text.lower()
    words = text_lower.split()

    synonym_replaced_words = [COMMAND_SYNONYMS.get(word, word) for word in words]
    synonym_replaced_text = " ".join(synonym_replaced_words)

    # -----------------------------------------------------
    # SCHRITT 2: Extreme Normalisierung (Stemming und Stoppwörter)
    # -----------------------------------------------------
    # Hier verwenden wir die extrem aggressive Funktion (extreme_standardize_prompt_text)
    # Beachten Sie: Diese Funktion muss jetzt die Wörter 'neu', 'info', 'del', 'regel' etc.
    # NICHT aus der Stoppwortliste entfernen, da sie von den Synonymen kommen!

    final_cache_key = extreme_standardize_prompt_text(synonym_replaced_text)

    # Beispiel:
    # prompt = "generiere eine neue regel"
    # S1: "neu eine neue regel"
    # S2: "neu neu regel" (nach Stemming und Stoppwort-Entfernung)

    return final_cache_key

# ----------------------------------------------------
# AKTION:
# Führen Sie die Datenbank-Migration mit dieser
# neuen Funktion 'create_ultimate_cache_key' durch!
# ----------------------------------------------------



def extreme_standardize_prompt_text(text):

    # Den deutschen Stemmer initialisieren


    # 1. Alles in Kleinbuchstaben
    text = text.lower()

    # 2. ALLE Zahlen, Zeitangaben und Währungszeichen durch Platzhalter ersetzen
    text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text)  # Z.B. '10', '10.5'
    text = re.sub(r'[€$£%]', ' ', text)

    # 3. Radikale Entfernung von fast allen Sonderzeichen und Satzzeichen
    text = re.sub(r'[^a-zäöüß\s]', ' ', text)

    # 4. Whitespace auf ein einzelnes Leerzeichen reduzieren und trimmen
    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Tokenisierung (Wörter trennen)
    words = text.split()

    # 6. Entfernung von Stoppwörtern und Stemming
    stemmed_words = []
    for word in words:
        if word not in utils.STOP_WORDS_DE_EXTREME and len(word) > 8:
            stemmed_words.append(utils.GLOBAL_STEMMER.stem(word))
            # stemmed_words.append(stemmer.stem(word))

    unique_and_sorted_words = sorted(list(set(stemmed_words)))

    # 7. Wörter wieder zu einem String zusammensetzen
    text = ' '.join(unique_and_sorted_words)

    if not text:
        text = 'aura_empty_request'  # <-- Ein eindeutiger, kanonischer Fallback-Schlüssel

    # utils.log_debug(f"keywords<lastLine<extreme_standardize_prompt_text: 🔎 {text.strip()} 🔍")



    return text.strip()

