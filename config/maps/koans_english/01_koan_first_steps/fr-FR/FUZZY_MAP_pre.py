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

# config/maps/koans_english/01_koan_first_steps/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


BTW = """
'... regular expressions began in the 1950s... Different syntaxes for writing regular expressions have existed since the 1980s, one being the POSIX standard and another, widely used, being the Perl syntax.
... Regular expressions are used in search engines, in search and replace dialogs of word processors and text editors, in text processing utilities ... and in lexical analysis. Regular expressions are supported in many programming languages. '
( https://en.wikipedia.org/wiki/Regular_expression )

You probably know it already somehow or a part of it.
"""












FUZZY_MAP_pre = [

    # FAIRE

    # ('1', r'salut'),


    # ('2',r'.*'),





]

