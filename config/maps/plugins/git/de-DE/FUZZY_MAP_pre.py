# config/maps/plugins/git/de-DE/FUZZY_MAP_pr.py
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

    ('pull requests', r'^\s*(pull\s*requests?|Pullover\s*Quest)\s*$', 82, {'flags': re.IGNORECASE}),

    ('pull requests', r'\b(null|pull) requests\b', 82, {'flags': re.IGNORECASE}),


    ('er branch', r'er\b (brach|Prime)\b', 82, {'flags': re.IGNORECASE}),



    ('feature branch', r'\bFeature\s*prince\b', 82, {'flags': re.IGNORECASE}),

    ('feature branch', r'\bFeature\s*(prince|ranch)\b', 82, {'flags': re.IGNORECASE}),


    ('git checkout ', r'^\s*(git|geht)\s+(Git Checkout|Check-out)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git checkout ', r'^\s*(kitschiger|Geht Tscheka)\s*$', 80, {'flags': re.IGNORECASE}),




    ('git branch -d', r'\b(Branch|Prince)\s*löschen\b', 82, {'flags': re.IGNORECASE}),
    ('Branch Name', r'\bRanch\s*Namen\b', 82, {'flags': re.IGNORECASE}),
    ('Commit', r'\bkomm\s*mit\b', 82, {'flags': re.IGNORECASE}),
    ('Commit Message', r'\bkommen\s*mit\s*Message\b', 82, {'flags': re.IGNORECASE}),
    ('neues Release', r'\bneues\s*Verlies\b', 82, {'flags': re.IGNORECASE}),



    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    # geht's starte Gliedstaat ist
    # Geht Staat git status git status

    ('git status', r'^\s*(Geht|Sie geht|git|get|gitter|Gliedstaat|kids|kate)\s+(status|Staat|staates|statisch|start|startet|starten|stadel|dates)\s*$', 82, {'flags': re.IGNORECASE}),

    ('git status', r'^\s*(Gliedstaat)\s+(ist)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git status', r'^\s*(Gliedstaat|Kickstarter)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git status', r'^\s*(gitschtal|quatscht hatte|Geht tat uns)\s+$', 80, {'flags': re.IGNORECASE}),

#geht statisch


    # --- git add . --- git add .
    # Gitta hat
    ('git add .', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|jetzt|App)\s*(\.|\bpunkt\b)?\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git commit ---

    ('git commit ', r'^\s*Klitschko mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*kate Commit\s*$', 80, {'flags': re.IGNORECASE}),

    # Geht kommt
    ('git commit ', r'^\s*(git|geht[^\s]*|geh|gitter|kate|käthe|fiat|mit)\s+(Komet|Komik|Comics|Gummi|kommt|kommend|Commit|mit|hitch)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Einen Kometen\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht Commit\s*$', 80, {'flags': re.IGNORECASE}),


    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(Geht|git|mit) (komm|Kometen|Commit)\s*$', 80, {'flags': re.IGNORECASE}),


    ('commit ', r'\s+Komet\s+', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(git|mit) komm\s*mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*womit\s*$', 85, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|geht) komm?\s*mit\s*$"', 80, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|Gilt|geht) (Komet|komme|beach|gemütlich)\s*$"', 80, {'flags': re.IGNORECASE}),
    # Gilt komme komme

    # --- git push --- Gibt eine gibt git pull big push pitbull Geht prüfen

    ('git push ', r'^\s*(git|big|geht|gitter)\s*(busch|push|prüfen)\s*$', 85, {'flags': re.IGNORECASE}),
    ('git push ', r'^\s*kate\s+bush\s*$', 80, {'flags': re.IGNORECASE}),

    ('git push ', r'^\s*pitbull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git pull ---
    ('git pull', r'^\s*(git|geht|quiet|gitter)\s*(pohl|pool)\s*$', 82, {'flags': re.IGNORECASE}),
    ('git pull', r'^\s*git\s*pull\s*$', 80, {'flags': re.IGNORECASE}),


# einen git add . Ihnen geht App Geht prüft git push

    # --- git diff ---
    ('git diff', r'^\s*(kit|git|geht|peach)\s*(diff|tief|tiff|tüv|juice|tipps|geht\'s|kittys|dies|die)\s*$', 75, {'flags': re.IGNORECASE}),

    ('git switch ', r'^\s*(git|geht|peach)\s*(switch|Schmidt)\s*$', 75, {'flags': re.IGNORECASE}),

    ('git fetch; git pull"', r'^\s*(git|Gilt|geht) (fett)\s*$"', 80, {'flags': re.IGNORECASE}),


]

