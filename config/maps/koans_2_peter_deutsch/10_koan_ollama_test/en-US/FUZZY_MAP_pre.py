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

# config/maps/koans_2_peter_deutsch/10_koan_ollama_test/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# Rule format: ('replacement text', r'pattern', threshold, flags)

# Logic: Top-down, first hit wins. Fullmatch (^...$) stops the pipeline.


# PETER TASK: Use AutoFixModule - just write simple words without syntax

#
# Famous mathematicians are often misspelled by speech recognition systems.

# Examples:

# "gaus" -> should be: "Gauss"

# "oiler" -> should be: "Euler"

# "leibniz" -> correct, but capitalization is often missing

# "riemann" -> correct, but capitalization is often missing

#
# Task: Suggest rules that correct common STT errors in mathematician names.

# There are no commented out rules – be creative!


FUZZY_MAP_pre = [
]
