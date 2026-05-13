# config/maps/plugins/it-begriffe/php/codeigniter/de-DE/FUZZY_MAP_pre.py
# file config/maps/plugins/it-begriffe----/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702


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
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: codeigniter
    ('~projects/php/codeigniter/', r'^\b(codeigniter|Gotik Dieter|gothic Dieter)(\b)$', 80, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: code
    ('~projects/php/codeigniter/', r'^\b(code|gothic|Gotik)\s*(igniter|ignite|eignete|knipser|igniter|Dieter|Dieter|wird|Wii|nette)(\b)$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),



]



