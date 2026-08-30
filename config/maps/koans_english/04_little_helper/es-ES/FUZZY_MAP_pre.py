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

# configmaps/koans español/04 pequeño ayudante/de-DE/FUZZY_MAP_pre.py

import re

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




littleHelpers = """
Aura can serve as a quick reference tool.
We are using famous international Area Codes for this Koan.

Try to ask:
- 'Area code of Silicon Valley'
- 'Area code of New York'
- 'Area code of Tokyo'

Can you find your own city's code?
Check log/aura_engine.log to see the transcription!
"""

FUZZY_MAP_pre = [
    # Centros tecnológicos y ciudades globales

    # EXAMPLE: código de área de Silicon Valley

    ('408', r'^área código (de )?Silicio Valle$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: código de área de Nueva York Manhattan

    ('212', r'^área código (de )?Nuevo york( manhattan)?$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: código de área de Londres

    ('020', r'^área código (de )?Londres$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: código de área de tokio

    ('03', r'^área código (de )?Tokio$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: código de área de seattle

    ('206', r'^área código (de )?seattle$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: código de área de París

    ('01', r'^área código (de )?París$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
]

