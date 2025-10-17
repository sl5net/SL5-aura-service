# file config/maps/plugins/it-begriffe/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401

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
    # - means first is most imported, lower rules maybe not get read.


    ('Logdatei', r'^(\b)(Logdatei|Kochdatei)(\b)$', 80, {'flags': re.IGNORECASE}),

    ('Logfile', r'^(\b)(Logfile)(\b)$', 80, {'flags': re.IGNORECASE}),

    ('release', r'^(\b)(Relief|release|Relief|wer dies)(\b)$', 75, {'flags': re.IGNORECASE}),

    ('Python', r'^(\b)(Brighton|breit schon|Fallschirm|peitschen)(\b)$', 75, {'flags': re.IGNORECASE}),

    ('default', r'^(\b)(d fahl)(\b)$', 75, {'flags': re.IGNORECASE}),

    ('String', r'^(\b)(Dringen)(\b)$', 75, {'flags': re.IGNORECASE}),


    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, {'flags': re.IGNORECASE}),

    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    ('StopButton', r'\bstob\s*Button\b', 82, {'flags': re.IGNORECASE}),
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),

    ('Build Prozess', r'\bbild prozess\b', 82, {'flags': re.IGNORECASE}),

    ('opensource', r'\bopensource\b', 75, {'flags': re.IGNORECASE}),

    ('|', r'\b(pipe|pipe symbol|paid symbol|treib symbol|Paypal Symbol|pep|prep simba|treib simba|Paypal Simba)\b', 75, {'flags': re.IGNORECASE}),

    ('|', r'\b(pipe|pipe|paid|treib|Paypal|pep|prep|treib|Paypal) (symbol|simba|simpel|simbel|schimmer|SIM)\b', 75, {'flags': re.IGNORECASE}),

    ('@', r'\b(at|ed) (symbol|simba|simpel|simbel|schimmer|SIM|shampoo|schimpfwort|Zeichen)\b', 75, {'flags': re.IGNORECASE}),
# ed shampoo denSchätzchen wurdenEr schimpft
#HiPaypalPaid symbolPepWeib SymbolTreib SymbolPythonPaypal SymbolWeibchenbrät SimbaWeibchenPaypal Simbafeit SchimpfTreibt simpelVeit SchimmelPep Schimmer
#Häppchenbei SIMPaypal SIMHalb SIMPep simpel||Plätzchenbacken

 # Logfile-Duden  Logfile-Duden Logfile-Logdatei Nordwärts erreicht Logfile-Logdatei Logfile-Logdatei  Edits Relief Vernissage Kredit Kredit feststellt Wer dies Edit Wer dies




]



