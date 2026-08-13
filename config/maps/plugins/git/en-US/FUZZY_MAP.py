# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/git/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/de-DE/FUZZY_MAP.py

import re

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - means first is most important, lower rules maybe not get read.

    # EXAMPLE: praises Case

    ('lowerCase', r'\blobs\s*Case\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Some few

    ('Manjaro', r'\b(Some couple|Monks euro)\b', 75, {'command_flags': re.IGNORECASE}),


# ('.', r'^\s*(dot|pup)\s*$', 82, {'command_flags': re.IGNORECASE}),





    # EXAMPLE: pull requests

    ('pull requests', r'^\s*(pull\s*requests.requests?|Sweater\s*Quest)\s*$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: zero

    ('pull requests', r'\b(zero|pull) requests.requests\b', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Feature prince

    ('feature branch', r'\bFeature\s*prince\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Branch

    ('git branch -d', r'\b(Branch|Prince)\s*delete\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Ranch names

    ('Branch Name', r'\branch\s*names\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: come with me

    (' Commit ', r'\bcome\s*with\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: come with bitkom

    (' Commit ', r'\bcome\s*with\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    ('git commit ', r'^bitkom with$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: come with message

    (' Commit Message', r'\receive\s*with\s*Message\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: new dungeon

    ('neues Release', r'\bnew\s*dungeon\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Feces cut off

    ('Code Abschnitt', r'\bKot\s*sections\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: stob button

    ('StopButton', r'\bstob\s*button\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: praises Case

    ('lowerCase', r'\blobs\s*Case\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # --- git status ---

    # This one regex replaces 5 old entries.


    # EXAMPLE: gitstatus

    ('git status', r'^(slid|member states|kick start|squeaks away|it Status)$', 82,
     {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: gitstatus

    ('git status', r'^\s*(git|goes|grid|kids)\s+(status|state|instead of|stadium|dates)\s*$', 82,  {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # --- git add . ---

    # takes place

    # EXAMPLE: git add

    ('git add .', r'^\s*(git|goes|go|grid|Kate|fiat|with)\s+(add|at|did|dad|has|duet|it)\s*(\.|\bpoint\b)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # --- git commit in the middle of the text somewhere: ---

    # EXAMPLE: git commit

    ('git commit ', r'\b(Goes|git|good|with) (Commit)\b\s*', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # --- git commit ---

    # Kate commit a git commit


    # EXAMPLE: Klitschko with

    ('git commit ', r'^\s*Klitschko with\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: kate commit s

    ('git commit ', r'^\s*Kate Commit\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Go comet

    ('git commit ', r'^\s*Goes (comet|coming|correctly|Commit)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: A comet s

    ('git commit ', r'^\s*A Comets\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Go commit

    ('git commit ', r'^\s*Goes Commit\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: Go come commit

    ('git commit ', r'^\s*Goes come Commit\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Goes

    ('git commit ', r'^\s*(Goes|git|good|with) (come|Comets|Commit|Kevin)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),





    # EXAMPLE: comet

    (' commit ', r'\s+comet\s+', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: git

    ('git commit ', r'^\s*(git|with) come\s*with\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: with what

    ('git commit ', r'^\s*with what\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|goes) come?\s*with\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Applies|goes) (comet|come)\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Gilt come come


    # now also in line replacements:

    # EXAMPLE: git commit

    ('git commit "', r'\b(git|Applies|goes) (comet|come|kubitz)\b\s*"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),





    # --- git push ---

    # EXAMPLE: git push

    ('git push', r'^\s*(git|goes|grid)\s*(bush|fresh|push|probably)\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # --- git pull ---

    # EXAMPLE: git pull

    ('git pull', r'^\s*(git|goes|grid)\s*(pohl|pool)\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git pull

    ('git pull', r'^\s*git\s*pull\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # --- git diff ---

    # EXAMPLE: git diff

    ('git diff', r'^\s*(git|goes|peach)\s*(diff|deep|juice)\s*$', 75, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

]
