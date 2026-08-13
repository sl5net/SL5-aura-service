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

# configmaps/koans english/04 little helper/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




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
    # Pôles technologiques et villes mondiales

    # EXAMPLE: indicatif régional de la Silicon Valley

    ('408', r'^zone code (de )?Silicium Vallée$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: indicatif régional de New York Manhattan

    ('212', r'^zone code (de )?Nouveau York( Manhattan)?$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: indicatif régional de Londres

    ('020', r'^zone code (de )?Londres$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: indicatif régional de Tokyo

    ('03', r'^zone code (de )?Tokyo$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: indicatif régional de Seattle

    ('206', r'^zone code (de )?Seattle$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: indicatif régional de Paris

    ('01', r'^zone code (de )?Paris$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
]

#
