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

import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
# https://regex101.com/

zad_variants = [
    "0ad", "zad", "aed", "chihuahua", "cio", "cyra", "d", "di", "die", "dir",
    "februar", "fever", "fewo", "fiera", "fira", "führer", "give",
    "hier mal", "hierbei", "in", "it", "joa", "rohrer", "seo", "sie",
    "sie war", "sie wollen", "silva", "syrer", "tyrannei", "über",
    "weberei", "wieweit", "zebra", "zero", "zero ein"
]
zad_variants.sort(key=len, reverse=True)
zad = rf"({'|'.join(zad_variants)})"


zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']
_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
}
FUZZY_MAP_pre = [
    # config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py:19

    # EXAMPLE: alarma

    ('ö', r'^(alarma|Residencia en|n / A|a|ocasión|todo|anna|la|Hola|alarma enviar|alarma desencadenantes|alarma desencadenar|alarma enviar alarma desencadenar alarma desencadenar adjunto|timbre de alarma anillo|campanas de alarma|presión lloyd|pobre campana anillo campanas de alarma campana sonando|campana sonando|campana anillo|campanas anillo el campana anillo todo en el|alí|alarma encima|llevar desparramar|amenaza terminó)$',
     85,_common_meta),

    # EXAMPLE: 0ad voice
    (r'do you know you can play 0ad by voice?',
     rf'^{zad}\s+vo\w+$',85,_common_meta),

]
