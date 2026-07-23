# config/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pre.py
# config/languagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.




FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.


    # EXAMPLE: VSP Peronal
    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(Person\w+)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Frau Geschäftsführerin
    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Hobbys Geschäftsführer
    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Hobbys)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Herr Schröder
    ('Herr Schröer', r'^(Herr Schröder|Herr hersteller|Herr Schröer|herr schrill)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx
    ('Schröer', r'^(Schrö\w*r|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergox Schröx
    ('Ergotherapie Schröer', r'^Ergo\w* (Schrö\w*|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx Ergo
    ('Schröer Ergotherapie', r'^(Schrö\w*|schwör\w*|schworen|schon besorgt)\b Ergo\w*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Früher ergo
    ('Schröer Ergotherapie', r'^(Früher|Speyer) (eher|ergo|erst)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


]
#Ergotherapie Schröer

