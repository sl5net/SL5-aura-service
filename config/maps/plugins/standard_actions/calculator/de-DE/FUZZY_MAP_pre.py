
import re # noqa: F401


from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

CONFIG_DIR = p(__file__).parent
FUZZY_MAP_pre = [

    # Das Ergebnis von 5 plus 3 ist 8.

    # Die Regex fängt zwei Zahlen (\d+) und einen Operator (plus|minus|mal|geteilt)
    # EXAMPLE: rechne
    ('', r'(?:rechne|was ist|was is|was)\s*(\d+)\s*([\+\-\*\/]|plus|minus|mal|geteilt durch)\s*(\d+)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'calculator.py']
    }),
]

