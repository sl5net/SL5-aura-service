# config/maps/koans_deutsch/11_CopyQ_Benutzeroberflaeche/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# too<-from
# PETER-AUFGABE fuer Koan: 11_copyq_benutzeroberflaeche
# Keine auskommentierten Regeln gefunden.
# -> Erstelle eine sinnvolle neue Regel fuer diesen Koan.
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarón|twain|kurt)$'),

    #
]
