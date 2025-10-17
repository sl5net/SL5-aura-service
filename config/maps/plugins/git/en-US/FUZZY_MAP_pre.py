# config/languagetool_server/maps/de-DE/FUZZY_MAP.py
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
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.

    ('c', r'^\s*(call|check)\s*$', 50, {'flags': re.IGNORECASE}),
    ('r', r'^\s*(raise)\s*$', 50, {'flags': re.IGNORECASE}),
    ('f', r'^\s*(fold)\s*$', 50, {'flags': re.IGNORECASE}),
    ('d', r'^\s*(discard)\s*$', 50, {'flags': re.IGNORECASE}),
    ('b', r'^\s*(bet)\s*$', 50, {'flags': re.IGNORECASE}),
    ('x', r'^\s*(exchange)\s*$', 50, {'flags': re.IGNORECASE}),
    # Amount keys
    ('1', r'^\s*(100|one hundred)\s*$', 50, {'flags': re.IGNORECASE}),
    ('2', r'^\s*(250|two fifty)\s*$', 50, {'flags': re.IGNORECASE}),
    ('3', r'^\s*(50|fifty)\s*$', 50, {'flags': re.IGNORECASE}),


]
