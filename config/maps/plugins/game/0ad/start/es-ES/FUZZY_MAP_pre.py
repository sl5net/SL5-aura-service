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


import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

zad_variants = [
    "0ad", "zad", "aed", "chihuahua", "cio", "cyra", "d", "di", "die", "dir",
    "februar", "fever", "fewo", "fiera", "fira", "führer", "give",
    "hier mal", "hierbei", "in", "it", "joa", "rohrer", "seo", "sie",
    "sie war", "sie wollen", "silva", "syrer", "tyrannei", "über",
    "weberei", "wieweit", "zebra", "zero", "zero ein"
]
zad_variants.sort(key=len, reverse=True)
zad = rf"({'|'.join(zad_variants)})"
FUZZY_MAP_pre = [

    # EXAMPLE: configuración 0ad

    (r'tilde/.configuración/0anuncio/configuración/',
     rf'^{zad}\s+[ck]onf\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0 modificaciones publicitarias

    (r'tilde/.local/compartir/0anuncio/modificaciones',
     rf'^{zad}\s+mod[s]?$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Imagen de aplicación 0ad

    (r'tilde/Aplicaciones/0anuncio-0.28.0-x86_64.Imagen de aplicación',
     rf'^{zad}\s+App\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]
