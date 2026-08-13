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

# config/maps/koans_english/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401
from pathlib import Path

# ============================================================
# Koan 06 : Recherche Wikipédia vocale

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# on_match_exec peut interroger les API en ligne.

# Ici : Recherche Wikipédia par commande vocale.

#
# TÂCHE:

# 1. Activez la règle ci-dessous.

# 2. Dites : « Qu'est-ce que Londres ?

#
# DES ERREURS ? Vérifiez le journal :

# grep "wikipedia" log/aura_engine.log | queue -10

#
# OPTION HORS LIGNE :

# Voir config/maps/plugins/standard_actions/wikipedia_local/

#
# PROCHAINE ÉTAPE : Koan 07

# ============================================================

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # ('Qu'est-ce que Londres ?', r'^qu'est-ce que (?P<topic>.+)\?$', 90, {

    # 'command_flags' : re.IGNORECASE,

    # 'on_match_exec' : [CONFIG_DIR / 'wiki_search.py']

    # }),

]
