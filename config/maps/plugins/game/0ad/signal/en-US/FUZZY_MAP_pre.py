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

# config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py:1

import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702
# https://regex101.com/

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']
_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
}
FUZZY_MAP_pre = [
    # config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py:19

    # EXAMPLE: alarm

    ('ö', r'^(alarm|based on|n/a|to|occasion|all|anna|la|Hello|alarm send|alarm triggers|alarm trigger|alarm send alarm trigger alarm trigger attachment|alarm bell ring|alarm bells|pressure lloyd|poor bell ring alarm bells bell ringing|bell ringing|bell ring|bells ring the bell ring all into the|ali|alarm over|have on spread|threat ended)$',
     85,_common_meta),
]
