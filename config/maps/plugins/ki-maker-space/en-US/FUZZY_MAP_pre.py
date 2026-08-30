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

# config/maps/plugins/ki-maker-space/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.




"""

Mi

 Reboot - Wednesday



Do

Scratch-Thursday

    OpenLab:  11:00 - 22:00 Uhr



Fr

Fabric-Friday:  Feiertag - 3.10.2025

Open Lab ist geschlossen.

DO
Do
Scratch-Thursday
    OpenLab:  11:00 - 22:00 Uhr

Sa

Supercreative-Saturday

"""
FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


    # ki make espace AI alarm clocks AI in the way is k Email conversation Via email conversation

    # K i Sacks Makerspace KI Sacks Aspen

    # Blocked by email ki-maker.space


    # EXAMPLE: ki maker

    ('ki-maker.space', r'^(ki-maker|ki[\s]*make[\se]*space|k i [\s]*make[\s\w]*space|space|ki alarm clock|AI in the away is|AI Sacks aspen|Cain blasted away|K \w*\s*make space|AI it|K i \w+ \w*|ki menkes)\s*\w*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Gregor

    ('Gregor Schulte, 07071- 6395627 Gregor.Schulte@ki-maker.space', r'^(Gregor|Schulte|ki-maker.space)\s*\w*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Office ki-maker.space x

    ('Bulsat', r'^(Office ki-maker.space)\s*\w*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # Gregor trained Gregor

    # By email conversation K i bags of respect


]

