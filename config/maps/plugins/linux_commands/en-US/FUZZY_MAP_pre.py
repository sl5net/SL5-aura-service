# config/maps/plugins/linux_commands/en-US/FUZZY_MAP_pre.py
# file config/maps/plugins/it-begriffe/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

BenachrichtigungenPosition = """
    KDE
    Systemeinstellungen > Benachrichtigungen > Position wählen

    XFCE
    Einstellungen > Benachrichtigungen > Standardposition

    GNOME
    Erweiterung "Just Perfection" installieren > Benachrichtigungsposition

    Ganz ausschalten (alle)
    Klick auf Uhrzeit/Glocke > Nicht stören
"""


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: Benachritext stoeren
    (f'{BenachrichtigungenPosition}', r'^Benachri\w+ stoeren$'),
    # EXAMPLE: Benachrichtigtext Position
    (f'{BenachrichtigungenPosition}', r'^Benachrichtig\w+ Position$', 75, {'flags': re.IGNORECASE}),



    # EXAMPLE: AutoKey
    ('AutoKey', r'\bAuto k\b', 82, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe symbol|paid symbol|treib symbol|Paypal Symbol|pep|prep simba|treib simba|Paypal Simba)\b', 75, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe|paid|treib|Paypal|pep|prep|treib|Paypal) (symbol|simba|simpel|simbel|schimmer|SIM)\b', 75, # min_accuracy
 {'flags': re.IGNORECASE}),

    # === Linux/Unix Commands ===

    # Examples: disk usage
    ("gdu",
     # EXAMPLE: folder size
     r'^(folder size|directory size|disk usage|storage hog|gdu|disk full)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # Examples: disk space
    ("ncdu",
     # EXAMPLE: check storage
     r'^(check storage|ncdu|launch ncdu|how big are the folders|disk space)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


]
