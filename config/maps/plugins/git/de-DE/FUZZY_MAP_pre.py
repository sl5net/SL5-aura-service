# config/maps/plugins/git/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

# kit cubic
gitGit = r'(git|Geht|Sie geht|git|get|gitter|glitch|Gliedstaat|kids|kate|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit|kit|peach|quitt)'

commitGit = r'(Komet|Komik|Comics|Gummi|gummis|kommt|kommend|Commit|mit|hitch|komm|Kometen|kubicki|komisch|gewinnen|gromit|komme|kubis|cobit|cubic|beach|gemütlich|quitt|google)'

FUZZY_MAP_pre = [

    # geht geht cobit


    # novell fall



    # git commit -m "..." --no-verify
    #nö very far
    #no very far
    ('n --no-verify', rf'^(no|nur|nö|nur|novell|Numeri) (frei|verify|fall|very far|fein)$', 80, {'flags': re.IGNORECASE}),

    #no-verifyno-verifyl --no-verifyNumeri fein



    ('git commit ', rf'^\s*{gitGit}\s+{commitGit}\s*$', 80, {'flags': re.IGNORECASE}),

    # happens very seldem :D 18.11.'25 17:53 Tue
    ('git commit message ', rf'\bQuarzwerk gibt komm Mitmensch\b ', 80, {'flags': re.IGNORECASE}),


    ('git commit', rf'\bgibt kaum mit\w*', 80, {'flags': re.IGNORECASE}),



    ('git clone ', rf'^\s*{gitGit}\s+(klar|klon)\s*$', 80, {'flags': re.IGNORECASE}),

    # git@github.com:kiwix/kiwix-tools.git
    #


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
    (' Commit', r'\bkomm\s*mit\b', 82, {'flags': re.IGNORECASE}),
    (' Commit Message', r'\bkommen\s*mit\s*Message\b', 82, {'flags': re.IGNORECASE}),

    ('neues Release', r'\bneues\s*Verlies\b', 82, {'flags': re.IGNORECASE}),



    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    # geht's starte Gliedstaat ist
    # Geht Staat git status git status Jetzt startet

    ('git status', r'^\s*(Geht|Sie geht|git|get|gitter|glitch|Gliedstaat|kids|kate)\s+(status|Staat|staates|statisch|staatlich|start|startet|starten|stadel|dates)\s*$', 82, {'flags': re.IGNORECASE}),



    ('git status', r'^\s*(Gliedstaat|Gliedstaaten|Jetzt Stadt|Geht Staat ist|geht status)\s+(ist)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git status', r'^\s*(Gliedstaat|Kickstarter|Jetzt startet)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git status', r'^\s*(gitschtal|glitschte|quatscht hatte|quitscht|quitscht werden|Geht tat uns)\s+$', 80, {'flags': re.IGNORECASE}),

#geht statisch


    # --- git add . --- git add .
    # Gitta hat
    ('git add .', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|jetzt|App|er hat)\s*(\.|\bpunkt\b)?\s*$', 82, {'flags': re.IGNORECASE}),

    ('git add .', r'^\s*(Gitterbett|Geht er hin|kredit|quitte hat)\s*$', 78, {'flags': re.IGNORECASE}),

    # Geht er hat



    ############################################
    # too powerful a feature I would like to temporarily deactivate it (original:'ein zu mächtiges feature ich möchte das vorübergehend deaktivieren', SL5.de/Aura ).

    # if you not have enabled "git wip   " or you may want use:
    # say: git add quick
    #gehtHat quickGeht schnell
    #git add . && git commit -m "WIP" && git push; && git

    (f'!git add . && git commit -m "WIP" && git push', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|jetzt|App)\s*(quick|schnell|dirty|wip)?\s*$', 82, {'flags': re.IGNORECASE}),


    (f'!git add . && git commit -m "WIP" && git push; && git ', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s*(quick|schnell|dirty|wip)?\s*$', 82, {'flags': re.IGNORECASE}),
    ############################################

    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|jetzt|App)\s*(quick|schnell|dirty|wip)?\s*$', 82, {'flags': re.IGNORECASE}),

    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|geht[^\s]*|geh|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s*(quick|schnell|dirty|wip)?\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git commit ---
    ('git commit ', r'^\s*Klitschko mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*kate Commit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*Einen Kometen\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*(Geht Commit|Geht womit|petkovic)\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*(gehst du mit)\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*womit\s*$', 85, {'flags': re.IGNORECASE}),
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),

    ('git push ', r'^\s*(git|big|geht|gitter)\s*(busch|push|pushen|prüfen|futsch)\s*$', 85, {'flags': re.IGNORECASE}),
    ('git push ', r'^\s*kate\s+bush\s*$', 80, {'flags': re.IGNORECASE}),

    ('git push ', r'^\s*pitbull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git pull ---
    ('git pull', r'^\s*(git|geht|quiet|gitter)\s*(pohl|pool)\s*$', 82, {'flags': re.IGNORECASE}),
    ('git pull', r'^\s*git\s*pull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git diff ---
    ('git diff', r'^\s*(kit|git|geht|peach)\s*(diff|tief|tiff|tüv|juice|tipps|geht\'s|kittys|dies|die)\s*$', 75, {'flags': re.IGNORECASE}),

    ('git switch ', r'^\s*(git|geht|peach)\s*(switch|Schmidt)\s*$', 75, {'flags': re.IGNORECASE}),

    ('git fetch; git pull"', r'^\s*(git|Gilt|geht) (fett)\s*$"', 80, {'flags': re.IGNORECASE}),

##################################################################

    ('pull requests', r'^\s*(pull\s*requests?|Pullover\s*Quest)\s*$', 82, {'flags': re.IGNORECASE}),

    ('pull requests', r'\b(null|pull) requests\b', 82, {'flags': re.IGNORECASE}),

# bitte schreib mir denn geht kommen mit text'
    ('git commit text', r'\b(geht kommen mit text)\b', 75, {'flags': re.IGNORECASE}),


    ('feature branch', r'\bFeature\s*prince\b', 82, {'flags': re.IGNORECASE}),
    ('git branch -d', r'\b(Branch|Prince)\s*löschen\b', 82, {'flags': re.IGNORECASE}),
    ('Branch Name', r'\bRanch\s*Namen\b', 82, {'flags': re.IGNORECASE}),
    (' Commit', r'\bkomm\s*mit\b', 82, {'flags': re.IGNORECASE}),
    (' Commit Message', r'\bkommen\s*mit\s*Message\b', 82, {'flags': re.IGNORECASE}),
    ('neues Release', r'\bneues\s*Verlies\b', 82, {'flags': re.IGNORECASE}),
    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, {'flags': re.IGNORECASE}),
    ('StopButton', r'\bstob\s*Button\b', 82, {'flags': re.IGNORECASE}),
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),

    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---
    # This one regex replaces 5 old entries.
    ('git status', r'^\s*(git|geht|gitter|kids)\s+(status|staates|dates)\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git add . ---
    ('git add .', r'^\s*(git|geht|geh|gitter|kate|fiat|mit)\s+(add|ab|at|ritt|tat|dad|hat|duett|es)\s*(\.|\bpunkt\b)?\s*$', 82, {'flags': re.IGNORECASE}),

    # --- git commit ---
    #  Kate Commit einen  git commit

    ('git commit ', r'^\s*Klitschko mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*kate Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht (Komet|kommend|Commit)\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Einen Kometen\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*Geht komm Commit\s*$', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(Geht|git|mit) (komm|Kometen|Commit)\s*$', 80, {'flags': re.IGNORECASE}),

    ('commit ', r'\s+Komet\s+', 80, {'flags': re.IGNORECASE}),

    ('git commit ', r'^\s*(git|mit) komm\s*mit\s*$', 80, {'flags': re.IGNORECASE}),
    ('git commit ', r'^\s*womit\s*$', 85, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|geht) komm?\s*mit\s*$"', 80, {'flags': re.IGNORECASE}),
    ('git commit -m "', r'^\s*(git|Gilt|geht) (Komet|komme)\s*$"', 80, {'flags': re.IGNORECASE}),

    # --- git push ---
    ('git push', r'^\s*(git|geht|gitter)\s*(busch|push)\s*$', 85, {'flags': re.IGNORECASE}),

    # --- git pull ---
    ('git pull', r'^\s*(git|geht|gitter)\s*(pohl|pool)\s*$', 82, {'flags': re.IGNORECASE}),
    ('git pull', r'^\s*git\s*pull\s*$', 80, {'flags': re.IGNORECASE}),

    # --- git diff ---
    ('git diff', r'^\s*(git|geht|peach)\s*(diff|tief|juice)\s*$', 75, {'flags': re.IGNORECASE}),

    ('.gitignore', r'^\s*(Kritik knurren|Kritik Noah|Kritiken|kitte Knorr|Kritik Knorr)\s*$', 75, {'flags': re.IGNORECASE}),

    ('.gitignore', r'\b(gibt Knorr)\b$', 75, {'flags': re.IGNORECASE}),

    ("alias release_protokoll='gh release list --limit 100 | awk \"{print $1}\" | while read tag; do if [ -n \"$tag\" ]; then echo -e \"\n\n--- RELEASE: $tag ---\n\"; gh release view \"$tag\"; fi; done > all_releases.txt && kate all_releases.txt'", r'\b(releas\w* protokoll\w*|Relais\w* Protokolle|alle releases|releas\w* export\w*|frites Protokolle)\b$', 75, {'flags': re.IGNORECASE}),

]


"""
gh release list --limit 100 | awk '{print $1}' | while read tag; do
    if [ -n "$tag" ]; then
        echo -e "\n\n--- RELEASE: $tag ---"
        gh release view "$tag" --json body -q '.body'
    fi
done > all_releases.txt && kate all_releases.txt
"""

