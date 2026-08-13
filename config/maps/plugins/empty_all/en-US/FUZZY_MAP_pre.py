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

# config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702





# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


# too<-from

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


    # Cumulation: Rules (accumulate) so that perhaps only the last rule is visible. Examples:


    # The following rule applies to everything:

    # ('---', r'^.*$', 5, # min_accuracy {'command_flags': re.IGNORECASE}),


    # The following rule applies to everything except the word house:

    # EXAMPLE: House

    # ('', r'^(?!Haus).*$', 5, {'command_flags': re.IGNORECASE}),

    # TestTestTestHouseHouseHouseWoman fromHouse Tree underGood dayCheckmateCheckmate

    # CheckmateCheckmate


    # The following rule applies to everything except the words check, mate:

    # EXAMPLE: Chess

    # ('', r'^(?!check|mate|bad|house).*$', 5, {'command_flags': re.IGNORECASE}),

    # ChessChessHouseChessChessBathroom

    # Checkmate


    # EXAMPLE: Chess

    # ('Checkmate', r'^(Checkmate|bad|House).*$', 5, {'command_flags': re.IGNORECASE}),

    # CheckmateCheckmate




    ('LECKER_EXAKT', 'Marmelade', 100, {'command_flags': re.IGNORECASE}),
    # Jam JamLECKER_EXAKT


    # Test 2: Tolerant rule (typing errors allowed)

    # 'Marmelada' or 'Marmelad' should also be recognized.

    # ('LECKER_FUZZY', 'JAM', 1, {'command_flags': re.IGNORECASE}),


    # Jam Jam Mammon Mammon Mama Marion Málaga

    # Mama MarionA is lean





]
