import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702

# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE fuer Koan: 01_koan_erste_schritte
# Es gibt EINE auskommentierte Regel.
# -> Entferne das '#' um sie zu aktivieren.
# -> Was passiert danach in der Pipeline?
FUZZY_MAP_pre = [

    #TODO: Nur eine Aufgabe:
    #  Entferne das '#' vor der Regel unten.
    #  Was passiert? Warum stoppt die Pipeline danach?
    # ('hi 01_koan_erste__schritte', r'^.*$'),

]
