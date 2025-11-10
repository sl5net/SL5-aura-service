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

    # Deutsche p Nun sprechen wir durch

    #  Helps the Tool to switch to German
    # {'flags': {'flags': re.IGNORECASE}, 'skip_list': ['filter1', 'filter4']}
    ('Deutsch bitte', r'^\s*(deutsche) (pizza|pigeons|putin|bit|p)\s*$', 82, {'flags': re.IGNORECASE}),

    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),


    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),


    ('Manjaro', r'\b(much whole|munchau|mon travel|Manchu|Much\s*whole)\b', 82, {'flags': re.IGNORECASE}),
# Much whole Mon travel
# One troll Michelle


#    ('.', r'^\s*(punkt|pup)\s*$', 82, {'flags': re.IGNORECASE}),


#    ('zwei', r'ein|eins', 60, {'flags': re.IGNORECASE}),
#    ('drei', r'zwei', 60, {'flags': re.IGNORECASE}),




]
