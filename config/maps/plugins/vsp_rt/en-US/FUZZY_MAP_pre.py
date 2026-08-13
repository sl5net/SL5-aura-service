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

# config/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.





FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: VSP staff

    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(person\w+)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ms. Managing Director

    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Woman\s*s\s*p)\s*(Business\w+|Boss)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Hobbies Managing Director

    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Hobbies)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Woman\s*s\s*p)\s*(Business\w+|Boss)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Mr. Schröder

    ('Herr Schröer', r'^(Herr Schröder|Herr hersteller|Herr Schröer|herr schrill)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx

    ('Schröer', r'^(Schrö\w*r|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergox Schröx

    ('Ergotherapie Schröer', r'^Ergo\w* (Schrö\w*|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx Ergo

    ('Schröer Ergotherapie', r'^(Schrö\w*|swear\w*|swear|already worried)\b Ergo\w*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergo, earlier

    ('Schröer Ergotherapie', r'^(Earlier|Speyer) (rather|ergo|first)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


]
# Occupational therapy Schröer


