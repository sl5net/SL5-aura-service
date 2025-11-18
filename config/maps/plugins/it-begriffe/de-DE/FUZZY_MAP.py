# config/languagetool_server/maps/  /de-DE/FUZZY_MAP.py
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


    ('Python', r'^(\b)(Brighton|breit schon|Fallschirm|peitschen|Zeiten|Titan|Scheitern)(\b)$', 75, {'flags': re.IGNORECASE}),



    # a bit radial with following lines but i like it acually 17.11.'25 16:12 Mon
    ('Python', r'(\b)(Brighton|peitschen|Titan)(\b)', 75, {'flags': re.IGNORECASE}),

    ('Python prog', r'\bZeiten prog', 80, {'flags': re.IGNORECASE}),

    ('Virtual environment', r'\b(ritual|Virtuell|virtual|witwe\w*|witwer|wird schon|wird schwer|wirtschaft|wildschwein)\w* (in |wei |im |ein )?(Environment|Weibe|white|weima|metall|wei|warm|wei mit|wirbeln|et Deibel|in Reiben|reiben|Hinweis)\w*\b', 75, {'flags': re.IGNORECASE}),


]
