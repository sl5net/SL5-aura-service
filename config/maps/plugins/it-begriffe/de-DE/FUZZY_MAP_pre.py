# file config/maps/plugins/it-begriffe/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
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


    ('Logdatei', r'^(\b)(Logdatei|Kochdatei)(\b)$', 80, re.IGNORECASE),

    ('Logfile', r'^(\b)(Logfile)(\b)$', 80, re.IGNORECASE),

    ('release', r'^(\b)(Relief|release|Relief|wer dies)(\b)$', 75, re.IGNORECASE),

    ('Python', r'^(\b)(Brighton)(\b)$', 75, re.IGNORECASE),

    ('default', r'^(\b)(d fahl)(\b)$', 75, re.IGNORECASE),

    ('String', r'^(\b)(Dringen)(\b)$', 75, re.IGNORECASE),


    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, re.IGNORECASE),

    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    ('StopButton', r'\bstob\s*Button\b', 82, re.IGNORECASE),
    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    ('AutoKey', r'\bAuto k\b', 82, re.IGNORECASE),

    ('Build Prozess', r'\bbild prozess\b', 82, re.IGNORECASE),

    ('opensource', r'\bopensource\b', 75, re.IGNORECASE),



 # Logfile-Duden  Logfile-Duden Logfile-Logdatei Nordwärts erreicht Logfile-Logdatei Logfile-Logdatei  Edits Relief Vernissage Kredit Kredit feststellt Wer dies Edit Wer dies


]



