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

# config/maps/plugins/wannweil/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


# Bratwurst would be internal


    # EXAMPLE: Share churches

    ('Kirchentellinsfurt', r'\b(churches\s*split|Kirchentellinsfurt|clinking holds)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: City hall

    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(City hall|contact)\b\s*\b(churches\s*split|Kirchentellinsfurt)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: town hall keeps clinking

    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(city hall clinking holds)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),


# zieglersche https://www.zieglersche.de/altenhilfe.html pflegheim


# Town Hall keeps clinking

# The sound of hardwood clinking


    # EXAMPLE: who puppy

    ('Wannweil', r'\b(who\s*Puppy)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: who puppy

    ('Wannweil', r'\b(who\s*Puppy)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),
    # EXAMPLE: When because

    ('Wannweil', r'^\s*(When because|Annweiler|When\s*because|When\s*When\s*because|When\s*was\s*Mister|When\s*was\s*he|To\s*because|When\s*cry\w*|When\s*wine|Van\s*because|When What)\s*$', 70, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Sebastian runner

    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura|lauf|lauf war)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: figure

    ('Sigune Lauffer', r'\b(Figur|Sekunde|zugrunde|sigourney|sheego|Sie gute|gun|Ski gute|c gute|Schick ohne|sheikh ohne|gleich ohne|shi gunilla|spione)'
                       # EXAMPLE: runner

                       r' (runner|runner|Lauffer|run|run|run|Laura|run was|on it wait|in heap|stop|nose)\b', 82, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: thisRegexWillNeverMatch123ABC

    ('TestFuzzyNiemalsMatchen', r'\b(this regex will never match123ABC)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # ('TestFuzzyAlways', r'\b(thisRegexWillAlwaysMatch)\b', 1, # min_accuracy{'command_flags': re.IGNORECASE}),



    # EXAMPLE: Paradigm Minds

    ('pragmatic minds GmbH 2019', r'\b(paradigm Minds)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),



]

