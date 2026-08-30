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

# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py

# file config/maps/plugins/it-terms/FUZZY_MAP_pr.py

# Beispiel: https://www.it-begriffe.de/#L

import re

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py:17

FUZZY_MAP_pre = [
    # EXAMPLE: debugABZ

    ('debugABZxxx', r'debugABZ'),  # ← komplett standalone, keine Gruppe

    # Start rule: Triggers the group 'sandbox_test' at "start sandbox"

    # EXAMPLE: sta box

    ('Sandbox', r'^sta\w* .*box.*', 100, {'group_start': 'sandbox_test'}),

    # Inner rule 1: Replace “apple” with “pear” (if available)

    # EXAMPLE: apple

    ('birne', r'apple'),

    # Inner rule 2: Replace "banana" (if present), otherwise "banana" is appended!

    # EXAMPLE: banana

    ('banane', r'banana'),

    # Passive end marker for 'sandbox_test'

    (None, r'', 100, {'group_end': 'sandbox_test'}),
    (None, r'', 100, {'group_end': 'sandbox_test'}),

    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: JSON file


    ('JSON Datei', r'^\b(JSON(\sFile)?|hunting|Jacen|jason|wander)\s*(file|detail)(\b)$', 80, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: JSON export


    ('JSON Export', r'^\b(JSON export|Jacen export)(\b)$', 80, {'command_flags': re.IGNORECASE}),


    # Try it out


    # the liquid chair

    # EXAMPLE: the LanguageTool

    # LanguageTool

    # EXAMPLE: liquid stool

    ('das LanguageTool', r'\b(the) (LanguageTool|liquid Chair)(\b)', 80, {'command_flags': re.IGNORECASE}),
    ('LanguageTool', r'\b(liquid Chair)(\b)', 80, {'command_flags': re.IGNORECASE}),

    # of the link wich tools

    # EXAMPLE: LanguageTool


    ("des LanguageTool's", r'\b(LanguageTool|des link w\w+ tools)(\b)', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Manjaro


    ('Manjaro Linux', r'^(Manjaro|whatchado|monk|matcha where) (Linux|Carolin\w*)$', 80, {'command_flags': re.IGNORECASE}),

    # Monk CarolinWith CarolinIf CarolineManjaro Linux

    # EXAMPLE: Linux Manjaro

    ('Linux Manjaro', r'^(Linux) (Manjaro|man Check|just jaro|becomes jaro|matcha rub)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Linux Manjaro

    ('Linux Manjaro', r'^(Linux) ma\w*\s*\w*a\s*r[ou]m?$', 80, {'command_flags': re.IGNORECASE}),


    # Monk CarolinWith CarolinIf CarolineManjaro Linux

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^(Linux|velux) (Manjaro|matcha|becomes jaro|becomes jaro|with jaro)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^velux m\w+\s*[ou]$', 80, {'command_flags': re.IGNORECASE}),

    # velux m\w+\s*[ou]


    # velux matcha r u

    # velux with jaro


    # Velux matche


    # Linux Manjaro Velux times Karo

    # match where Linux




    # EXAMPLE: debate issues

    ('Debug-Ausgaben', r'^(debate expenditure)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: program loaded

    ('Programm geladen. Viel Spaß', r'^(Program[m]+ loaded)$', 80, {'command_flags': re.IGNORECASE}),




    # EXAMPLE: Log file

    ('Logdatei', r'^(Log file|cooking file|log-file)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Log file

    ('Logfile', r'^(\b)(Log file)(\b)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: relief

    ('release', r'^(\b)(release|relief|release|relief|who this)(\b)$', 75, {'command_flags': re.IGNORECASE}),

# Virtually in women

# Ritual in Deibel

# virtual in weibel

# Virtually at a distance

# virtual in white

# Ritual in Weimarvirtual in Weimar

# Virtual environment

# virtual in white widows in WeimarRitual in white#Virtual environment

# Ritual in Deibelvirtual in weibelVirtual in DeibelWill already be in wine

# will already be in wine, will be difficult in warm

# becomes difficult in warm economy in Weimar economy in Weimar Virtual environment

# widower in white with

# Heathens will each connect a virtual woman. It will be in Deibel

# Bachelorette DeibelVirtual in courtingVirtual in whirling Wild boars in rooms Virtual environment Titan is used here in a ritual environment

# virtual in whitevirtual in rooms


    # EXAMPLE: Virtual

    ('Virtual environment', r'\b(Virtual|virtual|widow\w*|widower|becomes already|becomes difficult|business|wild boar)\w* (in |white |in the )?(woman|white|weima|metal|white|warm|white with|whirl|clear|proofs|wallet)\w*\b', 75, {'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
    }),


# Titanium is used here in a virtual in white

# Virtual environment Titan will connect here in a ritual environment

# Biden is confused into a virtual woman here

# Titanium is used in every widow's wife

# Titan will, here lies a person no, both here will be your widow's anoint to become both here your widow's anoint will be to whom stupid

# Biden is confused into a virtual woman here

# Both will be joined here in a ride for the body

# Titanium is used here in a virtual woman

# titan will be in weibel

# Both are used here in one case

# Furthermore, a virtual in with is used here

# Every widow shall use his wife

# Titanium is used here in a virtual white metal

# Times will connect here in a widows in Weimar

# times will connect here in a widow in Weimar

# Failure hereSkaterTitan will ever be used in a widower in with

# Titanium will ever be used in a widower in white

# Times is used here in a wild boar in female

# ützensagTitan is used here in a ritual environment


    # EXAMPLE: Brighton

    ('Python', r'^(\b)(B2026-0131-2125righton|broad already|Parachute|whip)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Both are used here in a virtual environment

    ('Python wird hier in einer Virtual environment verwendet', r'^(both becomes here in one Virtual environment also used|Both becomes here in one becomes for the fall used|Furthermore becomes here in one virtual in at with used|Hold becomes anyone widow becomes woman use|titanium becomes here in one virtual in woman used|both becomes here in one virtual in white also used)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: sdf b bytes charm b

    ('PyCharm', r'^sdf(\b)(bytes charm)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: d pale

    ('default', r'^(\b)(d pale)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Penetrate

    ('String', r'^(\b)(Penetrate)(\b)$', 75, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Feces cut off

    ('Code Abschnitt', r'\bKot\s*sections\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: praises Case

    ('lowerCase', r'\blobs\s*Case\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: stob button

    ('StopButton', r'\bstob\s*button\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: praises Case

    ('lowerCase', r'\blobs\s*Case\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: AutoKey

    ('AutoKey', r'\bCar\s*k\w+\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 0 A.D.

    ('0 A.D.', r'\or zewa d\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: 0 A.D. game

    ('0 A.D. spiel', r'\or zewa d game\W*\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: 0 A.D. game

    ('GitHub SL5', r'\github it are 5\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: war x

    ('regex', r'\b(war x|rekik|Mike x|rick x|Recaps)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: image process

    ('Build Prozess', r'\picture process\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: open source

    ('opensource', r'\bopensource\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: pipe

    ('|', r'\b(pipe|pipe symbol|paid symbol|drive symbol|Paypal symbol|pep|prep Simba|drive Simba|Paypal Simba)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: pipe

    ('|', r'\b(pipe|pipe|paid|drive|Paypal|pep|prep|drive|Paypal) (symbol|Simba|simple|simble|shimmer|SIM)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: at

    ('@', r'\b(at|ed) (symbol|Simba|simple|simble|shimmer|SIM|shampoo|swear word|Sign)\b', 75, {'command_flags': re.IGNORECASE}),
# ed shampoo the sweetheart was complaining

# HiPaypalPaid symbolPepFemale symbolTreib symbolPythonPaypal symbolFemale roast SimbaFemalePaypal Simbafeit SchimpfTribst simpleVeit SchimmelPep shimmer

# Snacks at SIMPaypal SIMHalf SIMPep simple||Baking cookies


 # Logfile-Duden Logfile-Duden Logfile-Logfile Reached Northward Logfile-Logfile Logfile-Logfile Edits Relief Vernissage Credit Credit establishes Who this Edit Who this





]



