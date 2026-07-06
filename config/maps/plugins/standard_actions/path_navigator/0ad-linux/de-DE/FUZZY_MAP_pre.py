# config/maps/plugins/standard_actions/path_navigator/0ad-linux/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
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
     rf'^{zad}\s+[ck]onf\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad mods
    (r'tilde/.local/share/0ad/mods',
     rf'^{zad}\s+mod[s]?$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: 0ad AppImage
    (r'tilde/Apps/0ad-0.28.0-x86_64.AppImage',
     rf'^{zad}\s+App\w+$',
     ('90', r'^90$'),
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]
