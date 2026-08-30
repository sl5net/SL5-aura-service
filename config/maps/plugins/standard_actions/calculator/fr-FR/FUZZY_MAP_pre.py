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


import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

CONFIG_DIR = p(__file__).parent
FUZZY_MAP_pre = [

    # Le résultat de 5 plus 3 est 8.


    # L'expression régulière capture deux nombres (\d+) et un opérateur (plus|moins|fois|divisé)

    # EXAMPLE: calculer

    ('', r'(?:calculer|Quoi est|Quoi est|Quoi)\s*(\d+)\s*([\+\-\*\/]|plus|moins|juste|divisé à travers)\s*(\d+)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'calculator.py']
    }),
]

