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


from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




CONFIG_DIR = p(__file__).parent


FUZZY_MAP_pre = [


    # EXAMPLE: a

    ('add to einkaufsliste', r'\b(.+) (a|en el) lista de compras\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR /  '..' / 'shopping_list.py']
    }),

    # Regla para mostrar

    # EXAMPLE: mostrar la lista de compras

    ('', r'espectáculo el lista de compras', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'shopping_list.py']
    }),

]

