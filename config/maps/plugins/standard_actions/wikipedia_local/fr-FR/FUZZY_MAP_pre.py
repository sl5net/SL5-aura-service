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

# config/maps/plugins/standard_actions/wikipedia_local/de-DE/FUZZY_MAP_pre.py

import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
wikipedia = r"\s*\b(?:wikipédia|pédia|wiki|pédicure|wik|pe|recherche sur wikipédia après)\b\s*"
FUZZY_MAP_pre = [
    # EXAMPLE: qu'est-ce qu'une maison

    ("Wiki was ist ein haus Begriffsklärung", rf'^{wikipedia}was ist (ein|dein|den) haus$', 90,
     {
    'flags': re.IGNORECASE,
    'skip_list': ['LanguageTool','fullMatchStop'],
    }),
    # EXAMPLE: ordinateur

    ('', rf'^(?!Computer|Aura){wikipedia}(?:suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| dein| den| die| das| der| Herr)* (?P<search>.*)', 90, { 'flags': re.IGNORECASE,
     'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),
    # EXAMPLE: ordinateur

    ('', rf'^(?!Computer|Aura){wikipedia}(?: ein| die| das| der| Herr)? (?P<search>.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),
]
