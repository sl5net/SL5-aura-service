# config/maps/koans_deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
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
