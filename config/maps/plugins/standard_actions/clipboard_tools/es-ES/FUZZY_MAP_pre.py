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
     # EXAMPLE: Portapapeles

     r'^(Portapapeles|Portapapeles|Línea\w*|texto nuevo) (número\w*|sugerir|los estúpidos montado|funcionar|número|número)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),
    ('',
     # EXAMPLE: numeraciónex

     r'^(número\w*|sugerir|los estúpidos montado|funcionar|número|número)\b\s*(?:!el)?(Portapapeles|Portapapeles|Línea\w*|texto nuevo)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),

    # EXAMPLE: Número de líneax

    ('', r'^(Línea\w* número\w*|pauta sugerir|Línea los estúpidos montado|línea\w* funcionar|texto nuevo número|Portapapeles número|Correr Números de línea insertar|Números de línea actualizar|compartir reparar|No número|línea sugerir)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'renumber_clipboard_text.py']
    }),


]

