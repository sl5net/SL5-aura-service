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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP_pre.py


import re

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



    # EXAMPLE: None

    ('1', r'(\b|\d)(one)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('2', r'(\b|\d)(two)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('3', r'(\b|\d)(three)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('4', r'(\b|\d)(four)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('5', r'(\b|\d)(five)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('6', r'(\b|\d)(six)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('7', r'(\b|\d)(seven)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('8', r'(\b|\d)(eight)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('9', r'(\b|\d)(nine)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('10', r'(\b|\d)(ten)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: None

    ('15', r'(\b|\d)(fifteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

# one2025-1005-1324 one one in Hi Heinz one

# 5 3ich 5 river 4nlosönun0one zero five


    # EXAMPLE: zero

    ('0', r'^(zero|nope|so|go)$', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: zero

    ('0', r'(\b|\d)(zero)(\b|\d)', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: None

    ('1', r'(\b|\d)(one)(\b|\d)', 99, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('2', r'(\b|\d)(two|shout out|two|u)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('3', r'(\b|\d)(three)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('4', r'(\b|\d)(four)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('5', r'(\b|\d)(five)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('6', r'(\b|\d)(six|checks)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('7', r'(\b|\d)(seven|push)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('8', r'(\b|\d)(eight)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('9', r'(\b|\d)(nine)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('10', r'(\b|\d)(ten)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('11', r'(\b|\d)(eleven)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('12', r'(\b|\d)(twelve)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('13', r'(\b|\d)(thirteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('14', r'(\b|\d)(fourteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('15', r'(\b|\d)(fifteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('16', r'(\b|\d)(sixteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('17', r'(\b|\d)(seventeen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('18', r'(\b|\d)(eighteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('19', r'(\b|\d)(nineteen)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('20', r'(\b|\d)(twenty)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('21', r'(\b|\d)(twenty-one)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('22', r'(\b|\d)(twenty-two)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('23', r'(\b|\d)(twenty-three)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('24', r'(\b|\d)(twenty-four)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('25', r'(\b|\d)(zip becomes twenty|twenty-five)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('26', r'(\b|\d)(twenty-six)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('27', r'(\b|\d)(twenty-seven)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('28', r'(\b|\d)(twenty-eight)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('29', r'(\b|\d)(twenty-nine)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('30', r'(\b|\d)(thirty)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('40', r'(\b|\d)(forty)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('50', r'(\b|\d)(fifty)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('60', r'(\b|\d)(sixty)(\b|\d)', 78, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('70', r'(\b|\d)(seventy)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('80', r'(\b|\d)(eighty)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('90', r'(\b|\d)(ninety)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('100', r'(\b|\d)(hundred|one hundred)(\b|\d)', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('1000', r'(\b|\d)(thousand)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('2024', r'(\b|\d)(two thousand\s*twenty-four)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('2025', r'(\b|\d)(two thousand\s*twenty-five)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None

    ('2026', r'(\b|\d)(two thousand\s*twenty-six|two thousand\s*six\s*and\b.*)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # JOIN_NUMBERS_EVERYWHERE: Always pulls digits together if they are adjacent. works not as full power (somewhere in your string)

    # EXAMPLE: 1 1

    (r'\1', r'(\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # JOIN_NUMBERS_AT_END: Pulls digits together if only numbers/spaces follow

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']})

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']})


    # REMOVE 1 SPACES BETWEEN 2 NUMBERS fullmachtch

    # (r'\1\2', r'^(\d+)\s+(\d+)$', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




]


