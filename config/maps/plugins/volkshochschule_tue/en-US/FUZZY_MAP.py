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

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP.py

import re

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - means first is most important, lower rules maybe not get read.



    # EXAMPLE: Timo Stösser

    ('Timo Stösser', r'\b(thiem\w|timo|thema|ti\w+r)\s+(stäfa|steffen|Stefan|stripper|stefan|stürze\w*|stütze\w*|Sturz|stösse|Schlösser|stöße|stößt|Stöße|stöpsel|stärker|Störche)\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: Department manager

    ('Fachbereichsleitung', r'\bSubject\w*\s+Area management\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: PBW textix tx ex book

    ('Python-Buch', r'\b([PBW]\w+i\w*t\w*e\w* Book)\b', 60, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Instructor training

    ('Kursleiterschulung', r'\b(Instructor\s*sho\w*)\b', 60, {'command_flags': re.IGNORECASE})



]

