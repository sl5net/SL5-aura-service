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

    #switch to english no

    #  Helps the Tool to switch to English
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, re.IGNORECASE),
    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, re.IGNORECASE),

#

    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, re.IGNORECASE),

    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, re.IGNORECASE),
    # ('Wannweil', r'^\s*(wann weil|Ran weil)\s*$', 82, re.IGNORECASE),
    ('Wannweil', r'^\s*(Wannweil|Annweiler|wann\s*weil|Wann\s*wann\s*weil|Wann\s*war\s*Herr|Wann\s*war\s*er|An\s*weil|Wann\s*weine\w*|Wann\s*wein)\s*$', 70, re.IGNORECASE),
#  wann weil
# wann weil Wannweil Wannweil
#  Sieben zwo acht zwo sieben

 #  zweis drei
    ('pull requests', r'^\s*(pull\s*requests?|Pullover\s*Quest)\s*$', 82, re.IGNORECASE),

    ('pull requests', r'\b(null|pull) requests\b', 82, re.IGNORECASE),


    ('feature branch', r'\bFeature\s*prince\b', 82, re.IGNORECASE),

    ('feature branch', r'\bFeature\s*(prince|ranch)\b', 82, re.IGNORECASE),


    ('git checkout ', r'^\s*(git|geht)\s+(Git Checkout|Check-out)\s*$', 80, re.IGNORECASE),

    ('git checkout ', r'^\s*(kitschiger|Geht Tscheka)\s*$', 80, re.IGNORECASE),




    ('git branch -d', r'\b(Branch|Prince)\s*löschen\b', 82, re.IGNORECASE),
    ('Branch Name', r'\bRanch\s*Namen\b', 82, re.IGNORECASE),
    ('Commit', r'\bkomm\s*mit\b', 82, re.IGNORECASE),
    ('Commit Message', r'\bkommen\s*mit\s*Message\b', 82, re.IGNORECASE),
    ('neues Release', r'\bneues\s*Verlies\b', 82, re.IGNORECASE),
    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, re.IGNORECASE),
    ('StopButton', r'\bstob\s*Button\b', 82, re.IGNORECASE),
    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    ('AutoKey', r'\bAuto k\b', 82, re.IGNORECASE),


    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura)\b', 82, re.IGNORECASE),
    ('Sigune Lauffer', r'\b(Figur|Sekunde) (Läufer|laufer|Laura)\b', 82, re.IGNORECASE),

    ('Lauffer', r'\b(Läufer|laufer)\b', 82, re.IGNORECASE), # Exact match, but ignore case

    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    # geht's starte
    ('git status', r'^\s*(git|geht|gitter|kids|kate)\s+(status|staates|startet|dates)\s*$', 82, re.IGNORECASE),

    # --- git add . ---
    ('git add .', r'^\s*(git|geht[^\s]*|geh|gitter|kate|käthe|fiat|mit)\s+(add|at|tat|dad|hat|duett|es)\s*(\.|\bpunkt\b)?\s*$', 82, re.IGNORECASE),



    # --- git commit ---
    #  Kate Commit einen  git commit

    ('git commit ', r'^\s*Klitschko mit\s*$', 80, re.IGNORECASE),
    ('git commit ', r'^\s*kate Commit\s*$', 80, re.IGNORECASE),

    ('git commit ', r'^\s*Geht (Komet|kommend|Commit)\s*$', 80, re.IGNORECASE),

    ('git commit ', r'^\s*Einen Kometen\s*$', 80, re.IGNORECASE),

    ('git commit ', r'^\s*Geht Commit\s*$', 80, re.IGNORECASE),


    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, re.IGNORECASE),

    ('git commit ', r'^\s*(Geht|git|mit) (komm|Kometen|Commit)\s*$', 80, re.IGNORECASE),


    ('commit ', r'\s+Komet\s+', 80, re.IGNORECASE),

    ('git commit ', r'^\s*(git|mit) komm\s*mit\s*$', 80, re.IGNORECASE),
    ('git commit ', r'^\s*womit\s*$', 85, re.IGNORECASE),
    ('git commit -m "', r'^\s*(git|geht) komm?\s*mit\s*$"', 80, re.IGNORECASE),
    ('git commit -m "', r'^\s*(git|Gilt|geht) (Komet|komme)\s*$"', 80, re.IGNORECASE),
    # Gilt komme komme

    # --- git push ---
    ('git push', r'^\s*(git|geht|gitter)\s*(busch|push)\s*$', 85, re.IGNORECASE),

    # --- git pull ---
    ('git pull', r'^\s*(git|geht|quiet|gitter)\s*(pohl|pool)\s*$', 82, re.IGNORECASE),
    ('git pull', r'^\s*git\s*pull\s*$', 80, re.IGNORECASE),

    ('git push', r'^\s*kate\s+bush\s*$', 80, re.IGNORECASE),



    # --- git diff ---
    ('git diff', r'^\s*(git|geht|peach)\s*(diff|tief|juice)\s*$', 75, re.IGNORECASE),
]
