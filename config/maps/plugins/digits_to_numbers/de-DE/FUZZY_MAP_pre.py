# config/maps/plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py
# # file config/maps/plugins/digits_to_numbers/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    #  1  2  3  ein  2 3 test

    # EXAMPLE: b 1 b
    ('one', r'\b(1)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 2 b
    ('two', r'\b(2)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 3 b
    ('three', r'\b(3)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 4 b
    ('four', r'\b(4)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 5 b
    ('five', r'\b(5)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 6 b
    ('six', r'\b(6)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 7 b
    ('seven', r'\b(7)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 8 b
    ('eight', r'\b(8)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 9 b
    ('nine', r'\b(9)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 10
    ('ten', r'\b(10)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 15
    ('fifteen', r'\b(15)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 0 b
    ('null', r'\b(0)\b', 89, {'flags': re.IGNORECASE}),

    # EXAMPLE: b 1 b
    ('eins', r'\b(1)\b', 100, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 2 b
    ('zwei', r'\b(2)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 3 b
    ('drei', r'\b(3)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 4 b
    ('vier', r'\b(4)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 5 b
    ('fünf', r'\b(5)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 6 b
    ('sechs', r'\b(6)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 7 b
    ('sieben', r'\b(7)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 8 b
    ('acht', r'\b(8)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: b 9 b
    ('neun', r'\b(9)\b', 100, {'flags': re.IGNORECASE}),
    # EXAMPLE: 10
    ('zehn', r'\b(10)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 11
    ('elf', r'\b(11)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 12
    ('zwölf', r'\b(12)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 13
    ('dreizehn', r'\b(13)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 14
    ('vierzehn', r'\b(14)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 15
    ('fünfzehn', r'\b(15)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 16
    ('sechzehn', r'\b(16)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 17
    ('siebzehn', r'\b(17)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 20
    ('zwanzig', r'\b(20)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 30
    ('dreißig', r'\b(30)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 40
    ('vierzig', r'\b(40)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 50
    ('fünfzig', r'\b(50)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 60
    ('sechzig', r'\b(60)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 70
    ('siebzig', r'\b(70)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 80
    ('achtzig', r'\b(80)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 90
    ('neunzig', r'\b(90)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 100
    ('hundert', r'\b(100)\b', 89, {'flags': re.IGNORECASE}),
    # EXAMPLE: 1000
    ('tausend', r'\b(1000)\b', 89, {'flags': re.IGNORECASE}),

]



