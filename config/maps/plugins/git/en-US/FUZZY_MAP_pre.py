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

# config/maps/plugins/git/de-DE/FUZZY_MAP_pre.py

import re

# from pathlib import Path as p;import os as o
# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


CONFIG_DIR = Path(__file__).parent


# EXAMPLE: git

gitGit = r'(git|Goes|She goes|git|get|grid|glitch|member state|kids|Kate|goes[^\s]*|go|grid|Gitta|Kate|kathe|kitten|fiat|with|kit|peach|quit)'

# a kit with text in English


# EXAMPLE: Commit

commitGit = r'(Commit|comet|Comedy|comics|rubber|rubbers|comes|coming|with|hitch|come|Comets|kubicki|funny|win|gromit|come|kubis|cobit|cubic|beach|cozy|quit|google)'

FUZZY_MAP_pre = [



    # EXAMPLE: version number

    ('git describe --tags --abbrev=0', r'^(version number|version number)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),

    # EXAMPLE: no verify

    ('n --no-verify', r'^(no|only|nope|only|novell|Numbers) (free|verify|case|very far|fine)$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # no-verifyno-verifyl --no-verifyNumeri fine



    # EXAMPLE: b point chemnitz b

    ('PUNCTUATION_MAP ', r'\b(point Chemnitz)\b', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: git commit

    ('git commit ', rf'^\s*{gitGit}\s+{commitGit}\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],}),
    # here only_in_windows is removed because it's tested in the esl-test, and we maybe in some other windows 17.4.'26 15:08 Fri



    # happens very rarely :D 11/18/25 5:53 p.m. Tue

    # EXAMPLE: Quartz movement gives come fellow human being

    ('git commit message ', r'\bQuartz movement gives come fellow human being\b ', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: hardly gives any input

    ('git commit ', r'\bgives barely with\w*', 80,   {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # EXAMPLE: git commit

    ('git commit ', r'\bgit commit\b\s*', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # EXAMPLE: git commit

    ('git commit ', r'\bgrid comet\b\s*', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: git commit text in English

    ('bitte Commit-Message for uncommitted changes', rf'\b{gitGit}\b\s*\b{commitGit} text in english\b', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: git clone

    ('git clone ', rf'^\s*{gitGit}\s+(klar|klon|clone)\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # git@github.com:kiwix/kiwix-tools.git



    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


    # EXAMPLE: pull requests

    ('pull requests', r'^\s*(pull\s*requests.requests?|Sweater\s*Quest)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: pull requests

    ('pull requests', r'\b(zero|pull) requests.requests\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: he broke

    ('er branch', r'he\b (broke|Prime)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Feature prince

    ('feature branch ', r'\bFeature\s*prince\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Feature prince

    ('feature branch ', r'\bFeature\s*(prince|ranch)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE}),


    # EXAMPLE: git checkout

    ('git checkout ', r'^\s*(git|goes)\s+(Git Check out|Check-out)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git checkout

    ('git checkout ', r'^\s*(cheesier|Goes Cheka)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: git branch

    ('git branch -d', r'\b(Branch|Prince)\s*delete\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Branch name

    ('Branch Name', r'\branch\s*names\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Commit

    (' Commit ', r'\bcome\s*with\b\s*', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Commit message

    (' Commit Message ', r'\receive\s*with\s*Message\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: new release

    ('neues Release ', r'\bnew\s*(Release|dungeon)\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- git status ---

    # This one regex replaces 5 old entries.

    # Let's start the state

    # Goes state git status git status Starting now


    # EXAMPLE: gitstatus

    ('git status ', r'^\s*(Goes|She goes|git|get|grid|glitch|member state|kids|Kate)\s+(status|State|state|static|state|start|starts|start|barn|dates)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: member states

    ('git status ', r'^\s*(member state|member states|Now City|Goes State is|goes status)\s+(is)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: member state

    ('git status ', r'^\s*(member state|Kickstarter|Now starts)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: gitschtal

    ('git status', r'^\s*(gitschtal|slid|chats had|squeaks|squeaks become|Nonsense had|Goes did us)\s+$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # is static



    # --- git add . --- git add .

    # Gitta has

    # EXAMPLE: git add .

    ('git add .', r'^\s*(git|goes[^\s]*|go|grid|Gitta|Kate|kathe|kitten|fiat|with)\s+(add|at|did|dad|has|duet|slide|it|now|app|he has)\s*(\.|\bpoint\b)?\s*$', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Cot

    ('git add .', r'^\s*(Cot|Goes he there|credit|quince has)\s*$', 78, # min_accuracy
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # Goes he has




    ############################################
    # too powerful a feature I would like to temporarily deactivate it (original: 'too powerful a feature I would like to temporarily deactivate it', SL5.de/Aura ).


    # if you do not have enabled "git wip " or you may want to use:

    # say: git add quick

    # goesHas quickGoes quickly

    # git add . && git commit -m "WIP" && git push; && git


    # EXAMPLE: git WIP push

    ('!git add . && git commit -m "WIP" && git push', r'^\s*(git|goes[^\s]*|go|grid|Gitta|Kate|kathe|kitten|fiat|with)\s+(add|at|did|dad|has|duet|slide|it|now|app)\s*(quick|fast|dirty|wip)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: git WIP push

    ('!git add . && git commit -m "WIP" && git push; && git ', r'^\s*(git|goes[^\s]*|go|grid|Gitta|Kate|kathe|kitten|fiat|with)\s*(quick|fast|dirty|wip)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    ############################################

    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|now|app)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['console', 'console', 'Terminal', 'Console']}),


    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|with)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'Konsole', 'Terminal', 'Console']}),


    # --- git commit ---

    # EXAMPLE: Klitschko with

    ('git commit ', r'^\s*Klitschko with\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Kate Commit

    ('git commit ', r'^\s*Kate Commit\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: A comet

    ('git commit ', r'^\s*A Comets\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Go commit

    ('git commit ', r'^\s*(Goes Commit|Goes with what|petkovic)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Go come commit

    ('git commit ', r'^\s*Goes come Commit\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: you go with me

    ('git commit ', r'^\s*(go you with)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: with what

    ('git commit ', r'^\s*with what\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: goes cobit one

    ('git commit ', r'^goes cobit a$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git push

    ('git push ', r'^\s*(git|big|goes|grid)\s*(bush|push|push|check|gone)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Kate Bush

    ('git push ', r'^\s*Kate\s+bush\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: pitbull

    ('git push ', r'^\s*pitbull\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git pull ---

    # EXAMPLE: git pull

    ('git pull ', r'^\s*(git|goes|quiet|grid)\s*(pull|pohl|pool)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: s git pull s

    ('git pull ', r'^\s*git\s*pull\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git diff ---

    # EXAMPLE: git diff

    ('git diff ', r'^\s*(kit|git|goes|peach)\s*(diff|deep|tiff|tuv|juice|tips|goes\'s|kittys|dies|die)\s*$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Comparison with the penultimate commit s

    ('git diff HEAD~1', r'^Comparison with penultimate Commit\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Last commit with diff s

    ('git log -p -1', r'^Last Commit with Diff\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Shows staged but not committed changes s

    ('git diff --cached', r'^Shows staged (but not committed) changes\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # EXAMPLE: git switch

    ('git switch ', r'^\s*(git|goes|peach)\s*(switch|Schmidt)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git pull

    ('git fetch; git pull"', r'^\s*(git|Applies|goes) (pull|fat)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

##################################################################

    # EXAMPLE: pull requests

    ('pull requests', r'^\s*(pull\s*requests.requests?|Sweater\s*Quest)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: pull requests

    ('pull requests', r'\b(zero|pull) requests.requests\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

# please write to me because it will come with text'

    # EXAMPLE: comes with text

    ('git commit text', r'\b(goes come with text)\b', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Feature prince

    ('feature branch', r'\bFeature\s*prince\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Delete branch

    ('git branch -d', r'\b(Branch|Prince)\s*delete\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Ranch names

    ('Branch Name', r'\branch\s*names\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Commit message

    (' Commit', r'\bcome\s*with\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: come with message

    (' Commit Message', r'\receive\s*with\s*Message\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: new release

    ('neues Release', r'\bnew\s*(dungeon|Release)\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: Code section

    ('Code Abschnitt', r'\bKot\s*sections\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: stop button

    ('StopButton', r'\bstob\s*button\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: praises Case

    ('lowerCase', r'\blobs\s*Case\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git status ---

    # This one regex replaces 5 old entries.

    # EXAMPLE: gitstatus

    ('git status', r'^\s*(git|goes|grid|kids)\s+(status|state|dates)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git add . ---

    # EXAMPLE: git add

    ('git add .', r'^\s*(git|goes|go|grid|Kate|fiat|with)\s+(add|away|at|ride|did|dad|has|duet|it)\s*(\.|\bpoint\b)?\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git commit ---

    # Kate commit a git commit


    # EXAMPLE: Klitschko with s

    ('git commit ', r'^\s*Klitschko with\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: kate commit s

    ('git commit ', r'^\s*Kate Commit\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Go comet

    ('git commit ', r'^\s*Goes (comet|coming|Commit)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: A comet s

    ('git commit ', r'^\s*A Comets\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Go Commit s

    ('git commit ', r'^\s*Goes Commit\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Go come commit s

    ('git commit ', r'^\s*Goes come Commit\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Goes

    ('git commit ', r'^\s*(Goes|git|with) (come|Comets|Commit)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: comet

    ('commit ', r'\s+comet\s+', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git

    ('git commit ', r'^\s*(git|with) come\s*with\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: with what s

    ('git commit ', r'^\s*with what\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|goes) come?\s*with\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Applies|goes) (comet|come)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git push ---

    # EXAMPLE: git

    ('git push', r'^\s*(git|goes|grid)\s*(bush|push)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git pull ---

    # EXAMPLE: git

    ('git pull', r'^\s*(git|goes|grid)\s*(pohl|pool)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),
    # EXAMPLE: s git pull s

    ('git pull', r'^\s*git\s*pull\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # --- git diff ---

    # EXAMPLE: git

    ('git diff', r'^\s*(git|goes|peach)\s*(diff|deep|juice)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Show what was changed in the last commit s

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^\s*Show What in the last Commit changed became\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Growl criticism

    ('.gitignore', r'^\s*(criticism growl|criticism Noah|Reviews|kitten Knorr|criticism Knorr)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: gives Knorr

    ('.gitignore', r'\b(gives Knorr)\b$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: new release

    ("alias release_protokoll='gh release list --limit 100 | awk \"{print $1}\" | while read tag; do if [ -n \"$tag\" ]; then echo -e \"\n\n--- RELEASE: $tag ---\n\"; gh release view \"$tag\"; fi; done > all_releases.txt && kate all_releases.txt'", r'\b(releases\w* protocol\w*|relay\w* Protocols|all releases|releases\w* export\w*|fries Protocols)\b$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


]





"""
gh release list --limit 100 | awk '{print $1}' | while read tag; do
    if [ -n "$tag" ]; then
        echo -e "\n\n--- RELEASE: $tag ---"
        gh release view "$tag" --json body -q '.body'
    fi
done > all_releases.txt && kate all_releases.txt
"""

