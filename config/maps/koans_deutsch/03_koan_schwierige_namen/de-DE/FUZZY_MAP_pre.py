# config/maps/koans_deutsch/03_koan_schwierige_namen/de-DE/FUZZY_MAP_pre.py
# ============================================================
# Koan 03: Schwierige Namen – Fuzzy Matching in der Praxis
# ============================================================
#
# LERNZIEL:
#   Vosk erkennt schwierige Namen oft falsch. Mit Regex kannst
#   du trotzdem zuverlässig matchen – auch bei Tippfehlern.
#
# AUFGABE:
#   Versuche diesen Titel einzusprechen:
#   "Ihre Hochwohlgeborenste Erz-Amts-Rath Schlesien"
#
#   Schau danach ins Log was Vosk wirklich gehört hat:
#   grep "📢📢📢" log/aura_engine.log | tail -5
#
#   Aktiviere dann die Regel die am besten passt (# entfernen).
#
# FRAGE ZUM NACHDENKEN:
#   Welche Regel ist robuster – die exakte oder die mit .*?
#   Was sind die Vor- und Nachteile von r'^Ihre Hochwohlgeboren.*$'?
#
# NÄCHSTER SCHRITT: Koan 04
# ============================================================

FUZZY_MAP_pre = [


    # EXAMPLE: Tante
    ('Tante Emmelie', r'^(Tante|tandy|Und|an der|and in|und wie) (Emmelie|emil\w*|Amélie|vivien)*$'),


    # Exakter Match (präzise aber fragil):
    # ('Super :) Gratulation', r'^Ihre Hochwohlgeborenste.*Schlesien.*$'),

    # Robuster Match (flexibel aber unspezifisch):
    # ('Super :) Gratulation', r'^Ihre Hochwohlgeboren.*$'),

    # Fuzzy Match für den Namen:
    # ('Grafin erkannt!', r'^.*gr[äa]fin.*$', 0, {'flags': re.IGNORECASE}),
]
