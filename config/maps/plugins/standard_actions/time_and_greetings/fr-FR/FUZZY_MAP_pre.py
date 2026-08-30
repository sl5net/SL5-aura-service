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

# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py

import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: salutation

    ('anrede', r'^(salutation|salutation|nouveau e-mail|Nouveau E-E-mail|Écrire salutation\w*|Écrire salutation)$', 95, {
        'flags': re.IGNORECASE,
        # Invoque notre nouveau script

        'on_match_exec': [CONFIG_DIR / '..' /  'greeting_generator.py']
    }),
]

