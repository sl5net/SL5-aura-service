# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401


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

    ('baue Baracke', r'^\s*(baue|baue|Build)\s+(Ba\w+)$', 15, re.IGNORECASE),

    ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 15, re.IGNORECASE),

    # paul barras
    ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Bar\w+)$', 15, re.IGNORECASE),



    # select Verwaltungssitz
    # kontroll c
    # kontroll chi
    # 📢kontrollzwecken
    # controll c
    ('ctrl+c', r'^\s*([kc]ontroll\w*) c.*$', 20, re.IGNORECASE),
    ('ctrl+c', r'^\s*kontrollzwecken$', 20, re.IGNORECASE),

    # Select all infrantry
    ('alt+i', r'^\s*(alt\s*e|alt\s*i|ald\s*i|select in).*\s*$', 20, re.IGNORECASE),

    ('alt+#', r'^\s*Select all iddle workers*\s*$', 20, re.IGNORECASE),

    ('alt+w', r'^\s*(select\s*wo|select\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*\s$', 20, re.IGNORECASE),
]
