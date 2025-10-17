# config/maps/plugins/git/de-DE/FUZZY_MAP_pr.py
import re

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
    # - means first is most imported, lower rules maybe not get read.

    ('Lauffer', r'\b(Läufer|laufer|Lauscha|lauf war|lauf er)\b', 70, {'flags': re.IGNORECASE}),  # Exact match, but ignore case
# lautLauffer3 4 5 73p 3 9 chatEs sitzt ein Vogel auf dem Leim er flattert sehr und kann nicht heim ein schwarzer Kater kommt hin zu den Augen grau die Augen.oute#
]

