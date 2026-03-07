# config/maps/koans_deutsch/03_koan_schwierige_namen/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
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
