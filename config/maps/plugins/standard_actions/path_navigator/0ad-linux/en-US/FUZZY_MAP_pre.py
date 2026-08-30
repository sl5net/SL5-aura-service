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

# config/maps/plugins/standard_actions/path_navigator/0ad-linux/de-DE/FUZZY_MAP_pre.py

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

    # EXAMPLE: 0ad configuration

    (r'tilde/.config/0ad/config/',
     rf'^({zad}|0ad)\s+[ck]onf\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad mods

    (r'tilde/.local/share/0ad/mods',
     rf'^({zad}|0ad)\s+mod[s]?$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad mods autocivp

    (r'tilde/.local/share/0ad/mods/autocivp',
     rf'^({zad}|0ad)\s+mod[s]?\s*autocivp$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad github autocivp

    (r'CD tilde/projects/github/0ad/autocivp/',
     rf'^({zad}|0ad)\s+github\s*autocivp$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad AppImage

    (r'tilde/Apps/0ad-0.28.0-x86_64.AppImage',
     rf'^({zad}|0ad)\s+App\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]
