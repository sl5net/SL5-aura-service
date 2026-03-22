# config/maps/koans_deutsch/11_CopyQ_Benutzeroberflaeche/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

# ============================================================
# Koan 11: Dein Sprach-Dashboard – Regeln visualisieren
# ============================================================
#
# LERNZIEL:
#   Alle deine Regeln durchsuchbar in CopyQ anzeigen.
#
# AUFGABE:
#   1. CopyQ installieren und starten
#   2. Im Terminal ausführen:
#      python tools/map_tagger.py
#      python tools/export_to_copyq.py
#   3. In CopyQ mit Strg+F nach "viele Grüße" suchen (aus Koan 09)
#
# NÄCHSTER SCHRITT: Du bist fertig mit den Basis-Koans!
#   Eigene Plugins: docs/CreatingNewPluginModules.md
# ============================================================

FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
