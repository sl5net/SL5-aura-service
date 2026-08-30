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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP.py

# https://regex101.com/

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


    # EXAMPLE: None

    ('5', r'(\b|\d)(five)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('6', r'(\b|\d)(six)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('7', r'(\b|\d)(seven)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('8', r'(\b|\d)(eight)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('9', r'(\b|\d)(nine)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('10', r'(\b|\d)(ten)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('11', r'(\b|\d)(eleven)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('12', r'(\b|\d)(twelve)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('13', r'(\b|\d)(thirteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('14', r'(\b|\d)(fourteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('15', r'(\b|\d)(fifteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('16', r'(\b|\d)(sixteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('17', r'(\b|\d)(seventeen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('18', r'(\b|\d)(eighteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('19', r'(\b|\d)(nineteen)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('20', r'(\b|\d)(twenty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('30', r'(\b|\d)(thirty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('40', r'(\b|\d)(forty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('50', r'(\b|\d)(fifty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('60', r'(\b|\d)(sixty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('70', r'(\b|\d)(seventy)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('80', r'(\b|\d)(eighty)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('90', r'(\b|\d)(ninety)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('100', r'(\b|\d)(hundred)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: None

    ('1000', r'(\b|\d)(thousand)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),


]
