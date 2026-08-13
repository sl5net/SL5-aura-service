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

import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [

    # Regla para codificación corta en Python

    # EXAMPLE: compacto_python

    ('', r'^(compacto_python|Compacto bien|Compacto Brighton|Compacto en)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'compact_python.py']
    }),

]

