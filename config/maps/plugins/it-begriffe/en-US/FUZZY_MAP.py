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

# config/maps/plugins/it-terms/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/ /de-DE/FUZZY_MAP.py

# https://regex101.com/

import re # noqa: F401

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



    # EXAMPLE: Brighton

    ('Python', r'^(\b)(Brighton|broad already|Parachute|whip|times|titanium|Fail)(\b)$', 75, {'command_flags': re.IGNORECASE}),



    # a bit radial with following lines but i like it actually 17.11.'25 16:12 Mon

    # EXAMPLE: Brighton

    ('Python', r'(\b)(Brighton|whip|titanium)(\b)', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Times prog

    ('Python prog', r'\bTimes prog', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: ritual

    ('Virtual environment', r'\b(ritual|Virtual|virtual|widow\w*|widower|becomes already|becomes difficult|business|wild boar)\w* (in |white |in the |a )?(Environment|woman|white|weima|metal|white|warm|white with|whirl|et Deibel|in Rub|rub|Notice)\w*\b', 75, {'command_flags': re.IGNORECASE}),


]
