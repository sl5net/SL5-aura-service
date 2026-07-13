# config/maps/koans_2_peter_deutsch/03_koan_schwierige_namen/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702


# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE fuer Koan: 03_koan_schwierige_namen
# Es gibt 3 auskommentierte Regeln.
# -> Aktiviere die ERSTE Regel (entferne das '#').
# -> Die anderen sind Alternativen zum Vergleich.
FUZZY_MAP_pre = [

    #TODO

    # Vielleicht so?
    #('Super :) Gratulation', r'^Ihre Hochwohlgeborenste, Erz-Amts-Rath-zu-Przewalskyst-Schlesien-Westpfalz, königlichst-kurfürstliche Geschäfts-Stellvertreter-Substitutin und Echtsachwalterin der Xenochronistischen Chronologie.*$'),

    # oder so?
    #('Super :) Gratulation', r'^Ihre Hochwohlgeboren.*$'),

    # Und der Titel?
    # Vielleicht so?
    #('Phryxts-Tschwirbel-Wzeschtsch-Chryschth Gräfin von und zu Echtschluchtz-Quarzschicht-Pfrtschnitz-Krüppelschwärz.', r'^.*gräfin.*$'),

]
