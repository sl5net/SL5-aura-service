# config/maps/koans_deutsch/11_CopyQ_Benutzeroberflaeche/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702


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
