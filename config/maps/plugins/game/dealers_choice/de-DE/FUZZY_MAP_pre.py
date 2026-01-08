# config/maps/plugins/game/dealers_choice/de-DE/FUZZY_MAP_pre.py
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
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - means first is most importend, lower rules maybe not get read.

    # EXAMPLE: call
    ('c', r'^\s*(call|check)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: raise s
    ('r', r'^\s*(raise)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: fold s
    ('f', r'^\s*(fold)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: discard s
    ('d', r'^\s*(discard)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: bet s
    ('b', r'^\s*(bet)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: exchange s
    ('x', r'^\s*(exchange)\s*$', 85, {'flags': re.IGNORECASE}),
    # Amount keys
    # EXAMPLE: 100
    ('1', r'^\s*(100|one hundred)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: 280
    ('2', r'^\s*(280|two fifty)\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: 80
    ('3', r'^\s*(80|fifty)\s*$', 85, {'flags': re.IGNORECASE}),


]
