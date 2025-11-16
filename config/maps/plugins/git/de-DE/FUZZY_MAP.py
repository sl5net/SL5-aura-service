# config/languagetool_server/maps/de-DE/FUZZY_MAP.py
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
    # - means first is most importend, lower rules maybe not get read.
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    ('Manjaro', r'\b(Manch paar|Mönche Euro)\b', 75, {'flags': re.IGNORECASE}),


#    ('.', r'^\s*(punkt|pup)\s*$', 82, {'flags': re.IGNORECASE}),


#    ('zwei', r'ein|eins', 60, {'flags': re.IGNORECASE}),
#    ('drei', r'zwei', 60, {'flags': re.IGNORECASE}),

 #  zweis drei
    ('pull requests', r'^\s*(pull\s*requests?|Pullover\s*Quest)\s*$', 82, {'flags': re.IGNORECASE}),

    ('pull requests', r'\b(null|pull) requests\b', 82, {'flags': re.IGNORECASE}),




    ('feature branch', r'\bFeature\s*prince\b', 82, {'flags': re.IGNORECASE}),
    ('git branch -d', r'\b(Branch|Prince)\s*löschen\b', 82, {'flags': re.IGNORECASE}),
    ('Branch Name', r'\bRanch\s*Namen\b', 82, {'flags': re.IGNORECASE}),
    ('Commit', r'\bkomm\s*mit\b', 82, {'flags': re.IGNORECASE}),
    ('Commit Message', r'\bkommen\s*mit\s*Message\b', 82, {'flags': re.IGNORECASE}),
    ('neues Release', r'\bneues\s*Verlies\b', 82, {'flags': re.IGNORECASE}),
    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, {'flags': re.IGNORECASE}),
    ('StopButton', r'\bstob\s*Button\b', 82, {'flags': re.IGNORECASE}),
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),


    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    ('git status', r'^\s*(git|geht|gitter|kids)\s+(status|staates|statt|stade|dates)\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git add . ---
    # geht statt
    ('git add .', r'^\s*(git|geht|geh|gitter|kate|fiat|mit)\s+(add|at|tat|dad|hat|duett|es)\s*(\.|\bpunkt\b)?\s*$', 82, {'flags': re.IGNORECASE}),


    # --- git commit mitten im text irgendwo: ---
    ('git commit ', r'\b(Geht|git|gut|mit) (Commit)\b', 80, {'flags': re.IGNORECASE}),


    # --- git commit ---
    #  Kate Commit einen  git commit

    ('git commit ', r'^\s*Klitschko mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*kate Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht (Komet|kommend|korrekt|Commit)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Einen Kometen\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht Commit\s*$', 80, {'flags': re.IGNORECASE}),


    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(Geht|git|gut|mit) (komm|Kometen|Commit|kevin)\s*$', 80, {'flags': re.IGNORECASE}),




    ('commit ', r'\s+Komet\s+', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(git|mit) komm\s*mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*womit\s*$', 85, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|geht) komm?\s*mit\s*$"', 80, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|Gilt|geht) (Komet|komme)\s*$"', 80, {'flags': re.IGNORECASE}),
    # Gilt komme komme

    # --- git push ---
    ('git push', r'^\s*(git|geht|gitter)\s*(busch|frisch|push|wohl)\s*$', 85, {'flags': re.IGNORECASE}),


    # --- git pull ---
    ('git pull', r'^\s*(git|geht|gitter)\s*(pohl|pool)\s*$', 82, {'flags': re.IGNORECASE}),
    ('git pull', r'^\s*git\s*pull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git diff ---
    ('git diff', r'^\s*(git|geht|peach)\s*(diff|tief|juice)\s*$', 75, {'flags': re.IGNORECASE}),
]
