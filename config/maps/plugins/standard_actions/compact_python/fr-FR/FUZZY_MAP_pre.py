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

FUZZY_MAP_pre = [

    # Règle courte pour le codage Python

    # EXAMPLE: compact_python

    ('', r'^(compact_python|Compact bien|Compact Brighton|Compact à)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'compact_python.py']
    }),

]

