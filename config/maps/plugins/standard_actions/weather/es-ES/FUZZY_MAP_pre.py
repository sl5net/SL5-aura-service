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

# config/maps/plugins/standard_actions/weather/de-DE/FUZZY_MAP_pre.py:1

import re # noqa: F401

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702
CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: como el clima

    ('', r'^(Cómo\s*(?:es|se convierte)?\s*(?:el)?\s*clima( mañana)?|Cómo el clima mañana|Cómo es el gordo|El recibió Datos meteorológicos tenía a inesperado formato.|Cómo es el cama|Cómo es el aproximadamente|a mí es el clima|próximo imagen|Cómo es el chirrido|no el clima|próximo|Cómo es el|Cómo es él|próximo nosotros|leer él)$'
    , 95, {
             'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'weather.py'] # Passe den Pfad ggf. an
    }),

    # EXAMPLE: como esta el clima

    ('', r'^(Cómo (se convierte|es|próximo)\b.*\clima|informe meteorológico|pronóstico del tiempo)\??$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR /  '..' /  'weather.py']
    }),
]

