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


    ('',
     # EXAMPLE: Presse-papiers

     r'^(Presse-papiers|Presse-papiers|Doubler\w*|texte nouveau) (nombre\w*|suggérer|les stupides monté|fonctionner|nombre|nombre)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),
    ('',
     # EXAMPLE: numérotationex

     r'^(nombre\w*|suggérer|les stupides monté|fonctionner|nombre|nombre)\b\s*(?:!le)?(Presse-papiers|Presse-papiers|Doubler\w*|texte nouveau)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),

    # EXAMPLE: Numéro Linexx

    ('', r'^(Doubler\w* nombre\w*|lignes suggérer|Doubler les stupides monté|doubler\w* fonctionner|texte nouveau nombre|Presse-papiers nombre|En cours dexécution Numéros de ligne insérer|Numéros de ligne mise à jour|partager réparation|Non nombre|suggestion de ligne)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'renumber_clipboard_text.py']
    }),


]

