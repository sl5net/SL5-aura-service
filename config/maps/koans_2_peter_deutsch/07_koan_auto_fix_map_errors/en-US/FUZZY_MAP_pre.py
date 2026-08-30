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

# config/maps/koans_2_peter_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py

import re

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch', 1, {'command_flags': re.IGNORECASE}),
]

# ============================================================
# Koan 07: Auto-Fix — Aura repairs corrupt map files

# ============================================================
#
# WHAT IT DOES:

# If a map file contains a "bare word" (not a tuple format),

# Aura's Auto-Fix automatically corrects it when loading.

#
# IMPORTANT:

# Auto-Fix only works on files smaller than ~1KB.

# This is intentional — uncontrolled rewriting of great ones

# This prevents map files.

#
# TASK:

# 1. Insert a single word into FUZZY_MAP_pre (not a tuple):

# hand towel

# 2. Save. Aura automatically corrects it to a valid rule.

# 3. Check the log for "Auto-Fix".

#
# NEXT STEP: Koan 08

# ============================================================

import re

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())



# Rule format: ('replacement text', r'pattern', threshold, flags)

# Logic: Top-down, first hit wins. Fullmatch (^...$) stops the pipeline.


# PETER TASK for Koan: 07_koan_auto_fix_map_errors

# No commented out rules found.

# -> Create a meaningful new rule for this koan.

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'command_flags': re.IGNORECASE}),
]
