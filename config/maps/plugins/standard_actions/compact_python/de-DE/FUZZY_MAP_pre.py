import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [

    # Regel für Python coding short
    # EXAMPLE: compact_python
    ('', r'^(compact_python|Kompakt fein|Kompakt Brighton|Kompakt bei)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'compact_python.py']
    }),

]

