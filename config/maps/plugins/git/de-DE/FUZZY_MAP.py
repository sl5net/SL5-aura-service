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
    # EXAMPLE: lobt s Case
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: Manch paar
    ('Manjaro', r'\b(Manch paar|Mönche Euro)\b', 75, {'flags': re.IGNORECASE}),


#    ('.', r'^\s*(punkt|pup)\s*$', 82, {'flags': re.IGNORECASE}),


#    ('zwei', r'ein|eins', 60, {'flags': re.IGNORECASE}),
#    ('drei', r'zwei', 60, {'flags': re.IGNORECASE}),

 #  zweis drei
    # EXAMPLE: s pull s requests
    ('pull requests', r'^\s*(pull\s*requests?|Pullover\s*Quest)\s*$', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: null
    ('pull requests', r'\b(null|pull) requests\b', 82, {'flags': re.IGNORECASE}),




    # EXAMPLE: Feature s prince
    ('feature branch', r'\bFeature\s*prince\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: Branch
    ('git branch -d', r'\b(Branch|Prince)\s*löschen\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: Ranch s Namen
    ('Branch Name', r'\bRanch\s*Namen\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: komm s mit
    (' Commit ', r'\bkomm\s*mit\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: kommen s mit s Message
    (' Commit Message', r'\bkommen\s*mit\s*Message\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: neues s Verlies
    ('neues Release', r'\bneues\s*Verlies\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: Kot s abschnittt
    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: stob s Button
    ('StopButton', r'\bstob\s*Button\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: lobt s Case
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: AutoKey
    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),


    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    # EXAMPLE: s git
    ('git status', r'^\s*(git|geht|gitter|kids)\s+(status|staates|statt|stade|dates)\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git add . ---
    # geht statt
    # EXAMPLE: s git
    ('git add .', r'^\s*(git|geht|geh|gitter|kate|fiat|mit)\s+(add|at|tat|dad|hat|duett|es)\s*(\.|\bpunkt\b)?\s*$', 82, {'flags': re.IGNORECASE}),


    # --- git commit mitten im text irgendwo: ---
    # EXAMPLE: Geht
    ('git commit ', r'\b(Geht|git|gut|mit) (Commit)\b', 80, {'flags': re.IGNORECASE}),


    # --- git commit ---
    #  Kate Commit einen  git commit

    # EXAMPLE: s Klitschko mit s
    ('git commit ', r'^\s*Klitschko mit\s*$', 80, {'flags': re.IGNORECASE}),
    # EXAMPLE: s kate Commit s
    ('git commit ', r'^\s*kate Commit\s*$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: s Geht Komet
    ('git commit ', r'^\s*Geht (Komet|kommend|korrekt|Commit)\s*$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: s Einen Kometen s
    ('git commit ', r'^\s*Einen Kometen\s*$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: s Geht Commit s
    ('git commit ', r'^\s*Geht Commit\s*$', 80, {'flags': re.IGNORECASE}),


    # EXAMPLE: s Geht komm Commit s
    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: s Geht
    ('git commit ', r'^\s*(Geht|git|gut|mit) (komm|Kometen|Commit|kevin)\s*$', 80, {'flags': re.IGNORECASE}),




    # EXAMPLE: Komet
    (' commit ', r'\s+Komet\s+', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: s git
    ('git commit ', r'^\s*(git|mit) komm\s*mit\s*$', 80, {'flags': re.IGNORECASE}),
    # EXAMPLE: s womit s
    ('git commit ', r'^\s*womit\s*$', 85, {'flags': re.IGNORECASE}),
    # EXAMPLE: s git
    ('git commit -m "', r'^\s*(git|geht) komm?\s*mit\s*$"', 80, {'flags': re.IGNORECASE}),
    # EXAMPLE: s git
    ('git commit -m "', r'^\s*(git|Gilt|geht) (Komet|komme)\s*$"', 80, {'flags': re.IGNORECASE}),
    # Gilt komme komme

    # now also inline replacments:
    # EXAMPLE: git
    ('git commit "', r'\b(git|Gilt|geht) (Komet|komme|kubitz)\b"', 80, {'flags': re.IGNORECASE}),




    # --- git push ---
    # EXAMPLE: s git
    ('git push', r'^\s*(git|geht|gitter)\s*(busch|frisch|push|wohl)\s*$', 85, {'flags': re.IGNORECASE}),


    # --- git pull ---
    # EXAMPLE: s git
    ('git pull', r'^\s*(git|geht|gitter)\s*(pohl|pool)\s*$', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: s git s pull s
    ('git pull', r'^\s*git\s*pull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git diff ---
    # EXAMPLE: s git
    ('git diff', r'^\s*(git|geht|peach)\s*(diff|tief|juice)\s*$', 75, {'flags': re.IGNORECASE}),
]
