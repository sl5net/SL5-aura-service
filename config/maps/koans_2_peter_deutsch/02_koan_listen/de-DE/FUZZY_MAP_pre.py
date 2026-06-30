# config/maps/koans_2_peter_deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702

# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE fuer Koan: 02_koan_listen
# Es gibt 2 auskommentierte Regeln.
# -> Aktiviere die ERSTE Regel (entferne das '#').
# -> Die anderen sind Alternativen zum Vergleich.
FUZZY_MAP_pre = [

    #TODO
    #('an', r'^[a-m]+.*$'),
    #('aus', r'^[n-z]+.*$'),

]
