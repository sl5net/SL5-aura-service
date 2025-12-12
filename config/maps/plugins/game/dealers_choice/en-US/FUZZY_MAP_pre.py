# config/  dealers_choice/maps/ FUZZY_MAP_pre.py
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

    # EXAMPLE: s call
    ('c', r'^\s*(call|check)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s raise s
    ('r', r'^\s*(raise)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s fold s
    ('f', r'^\s*(fold)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s discard s
    ('d', r'^\s*(discard)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s bet s
    ('b', r'^\s*(bet)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s exchange s
    ('x', r'^\s*(exchange)\s*$', 50, {'flags': re.IGNORECASE}),
    # Amount keys
    # EXAMPLE: s 100
    ('1', r'^\s*(100|one hundred)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s 250
    ('2', r'^\s*(250|two fifty)\s*$', 50, {'flags': re.IGNORECASE}),
    # EXAMPLE: s 50
    ('3', r'^\s*(50|fifty)\s*$', 50, {'flags': re.IGNORECASE}),


]
