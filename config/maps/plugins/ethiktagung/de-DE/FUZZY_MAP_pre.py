# config/maps/plugins/ethiktagung/de-DE/FUZZY_MAP_pr.py
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
    # - means first is most imported, lower rules maybe not get read.
    #
    ('Ethiktagung 2025', r'\b(ethik tiago|Ethik\s*Tag\w*|Ethiktagung|ethik tagung|Ethik\s*Tagung|Ethikrat|Ethik\s*Togo)\b', 80, re.IGNORECASE)

]

#  Ethik schreiben Ethik trägt Ethik Tag
