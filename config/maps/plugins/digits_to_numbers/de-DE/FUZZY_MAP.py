# config/languagetool_server/maps/plugins//de-DE/FUZZY_MAP.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.

    ('null', r'\b(0)\b', 100, {'flags': re.IGNORECASE}),
    ('eins', r'\b(1)\b', 100, {'flags': re.IGNORECASE}),
    ('zwei', r'\b(2)\b', 80, {'flags': re.IGNORECASE}),
    ('drei', r'\b(3)\b', 80, {'flags': re.IGNORECASE}),
    ('vier', r'\b(4)\b', 80, {'flags': re.IGNORECASE}),
    ('fünf', r'\b(5)\b', 80, {'flags': re.IGNORECASE}),
    ('sechs', r'\b(6)\b', 80, {'flags': re.IGNORECASE}),
    ('sieben', r'\b(7)\b', 80, {'flags': re.IGNORECASE}),
    ('acht', r'\b(8)\b', 80, {'flags': re.IGNORECASE}),
    ('neun', r'\b(9)\b', 100, {'flags': re.IGNORECASE}),
    ('zehn', r'\b(10)\b', 80, {'flags': re.IGNORECASE}),
    ('elf', r'\b(11)\b', 80, {'flags': re.IGNORECASE}),
    ('zwölf', r'\b(12)\b', 80, {'flags': re.IGNORECASE}),
    ('dreizehn', r'\b(13)\b', 80, {'flags': re.IGNORECASE}),
    ('vierzehn', r'\b(14)\b', 80, {'flags': re.IGNORECASE}),
    ('fünfzehn', r'\b(15)\b', 80, {'flags': re.IGNORECASE}),
    ('sechzehn', r'\b(16)\b', 80, {'flags': re.IGNORECASE}),
    ('siebzehn', r'\b(17)\b', 80, {'flags': re.IGNORECASE}),
    ('zwanzig', r'\b(20)\b', 80, {'flags': re.IGNORECASE}),
    ('dreißig', r'\b(30)\b', 80, {'flags': re.IGNORECASE}),
    ('vierzig', r'\b(40)\b', 80, {'flags': re.IGNORECASE}),
    ('fünfzig', r'\b(50)\b', 80, {'flags': re.IGNORECASE}),
    ('sechzig', r'\b(60)\b', 80, {'flags': re.IGNORECASE}),
    ('siebzig', r'\b(70)\b', 80, {'flags': re.IGNORECASE}),
    ('achtzig', r'\b(80)\b', 80, {'flags': re.IGNORECASE}),
    ('neunzig', r'\b(90)\b', 80, {'flags': re.IGNORECASE}),
    ('hundert', r'\b(100)\b', 80, {'flags': re.IGNORECASE}),
    ('tausend', r'\b(1000)\b', 80, {'flags': re.IGNORECASE}),



]
