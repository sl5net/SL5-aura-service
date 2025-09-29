# config/languagetool_server/maps/de-DE/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use re.IGNORECASE for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.

    ('baue Haus', r'^\s*(baue auf|baue\s*\w*haus|Build House|Baue Haus)\s*$', 15, re.IGNORECASE),

    ('alt+i', r'^\s*(alt\s*e|alt\s*i|ald\s*i|select in).*\s*$', 20, re.IGNORECASE),

    ('alt+w', r'^\s*(select\s*wo|select\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*\s$', 20, re.IGNORECASE),
]
