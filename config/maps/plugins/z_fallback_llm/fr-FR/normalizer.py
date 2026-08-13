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

# à partir des scripts d'importation idna.idnadata


# importer du hashlib



import sys
from pathlib import Path

CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
# pour _ dans la plage (5) :

# PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.parent


# Ajoutez le répertoire racine au chemin Python

# sys.path.append(str(PROJECT_ROOT_DIR))


# try:

# depuis scripts.py.func.audio_manager import * # noqa : F403 F401

# sauf ImportError comme e :

# print(f"Erreur : impossible d'importer 'audio_manager.py' en tant que module : {e}")

# utils.log_debug(f"Erreur : impossible d'importer 'audio_manager' en tant que module : {e}")


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

# À FAIRE : améliorer le synonyme




# ----------------------------------------------------

# DÉFINITIONS :

# 1. Les synonymes (de l'ancienne fonction)

# 2. La normalisation extrême (de la dernière réponse)

# ----------------------------------------------------


# (1) Les synonymes qui assurent un taux de correspondance élevé dans le cache

COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",

    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",

    "lösche": "del", "entferne": "del", "vergiss": "del",

    # Les synonymes contextuels sont risqués mais bons pour les matchs

    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}





def create_ultimate_cache_key(text):
    # --------------------------------------------------------------------

    # ÉTAPE 1 : Remplacement des synonymes (la nouvelle étape importante !)

    # --------------------------------------------------------------------

    text_lower = text.lower()
    words = text_lower.split()

    synonym_replaced_words = [COMMAND_SYNONYMS.get(word, word) for word in words]
    synonym_replaced_text = " ".join(synonym_replaced_words)

    # --------------------------------------------------------------------

    # ÉTAPE 2 : Normalisation extrême (racine et mots vides)

    # --------------------------------------------------------------------

    # Ici nous utilisons la fonction extrêmement agressive (extreme_standardize_prompt_text)

    # Remarque : Cette fonction doit maintenant contenir les mots « nouveau », « info », « del », « règle », etc.

    # NE PAS supprimer de la liste des mots vides car ils proviennent des synonymes !


    final_cache_key = extreme_standardize_prompt_text(synonym_replaced_text)

    # Exemple:

    # prompt = "générer une nouvelle règle"

    # S1 : "une nouvelle règle"

    # S2 : "nouvelle nouvelle règle" (après radicalisation et suppression des mots vides)


    return final_cache_key

# ----------------------------------------------------

# ACTION:

# Effectuez la migration de la base de données avec ceci

# nouvelle fonction 'create_ultimate_cache_key' !

# ----------------------------------------------------




def extreme_standardize_prompt_text(text):
    _load_heavy_deps()  # ensure utils is loaded

    # Initialiser le stemmer allemand



    # 1. Tout en minuscules

    text = text.lower()

    # 2. Remplacez TOUS les chiffres, heures et symboles monétaires par des espaces réservés

    # EXAMPLE: 123. 123

    text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text)  # Z.B. '10', '10.5'
    # EXAMPLE: $

    text = re.sub(r'[€$£%]', ' ', text)

    # 3. Suppression radicale de presque tous les caractères spéciaux et signes de ponctuation

    # EXAMPLE: a-zäöüß s

    text = re.sub(r'[^a-zäöüß\s]', ' ', text)

    # 4. Réduisez les espaces à un seul espace et coupez-les

    # EXAMPLE: 

    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Tokenisation (séparation des mots)

    words = text.split()

    # 6. Arrêtez la suppression et la racine des mots

    stemmed_words = []
    for word in words:
        if word not in utils.STOP_WORDS_DE_EXTREME and len(word) > 8:
            stemmed_words.append(utils.GLOBAL_STEMMER.stem(word))
            # stemmed_words.append(stemmer.stem(mot))


    unique_and_sorted_words = sorted(list(set(stemmed_words)))

    # 7. Réassemblez les mots en une chaîne

    text = ' '.join(unique_and_sorted_words)

    if not text:
        text = 'aura_empty_request'  # <-- Ein eindeutiger, kanonischer Fallback-Schlüssel

    # utils.log_debug(f"keywords<lastLine<extreme_standardize_prompt_text : 🔎 {text.strip()} 🔍")




    return text.strip()

