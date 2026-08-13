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

# config/maps/plugins/standard_actions/weather/de-DE/FUZZY_MAP_pre.py:1

import re # noqa: F401

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702
CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: comme la météo

    ('', r'^(Comment\s*(?:est|devient)?\s*(?:le)?\s*météo( matin)?|Comment le météo matin|Comment est le graisse|Le reçu Données météorologiques avait un inattendu format.|Comment est le lit|Comment est le environ|moi est le météo|suivant image|Comment est le gazouiller|pas le météo|suivant|Comment est le|Comment est il|suivant nous|lire il)$'
    , 95, {
             'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'weather.py'] # Passe den Pfad ggf. an
    }),

    # EXAMPLE: comment est le temps

    ('', r'^(Comment (devient|est|suivant)\b.*\météo|bulletin météo|prévisions météorologiques)\??$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR /  '..' /  'weather.py']
    }),
]

