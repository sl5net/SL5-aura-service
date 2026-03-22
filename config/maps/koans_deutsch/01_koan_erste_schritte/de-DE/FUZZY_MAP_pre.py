# config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401

# too<-from
FUZZY_MAP_pre = [

# ============================================================
# Koan 01: Deine erste Regel – Willkommen bei Aura!
# ============================================================
#
# Voraussetzung: Aura läuft bereits und dein Hotkey ist konfiguriert.
# Falls nicht: siehe docs/GettingStarted.md
#
# AUFGABE:
#   Entferne das '#' vor der Regel unten (Zeile mit 'hallo welt').
#   Speichere die Datei. Aura lädt die Regel beim nächsten Tastendruck
#   (Hotkey-Trigger) automatisch neu – im Ruhezustand schläft Aura komplett.
#   Drücke dann deinen Hotkey und sprich: "hallo welt"
#
# ERWARTETES ERGEBNIS:
#   Aura tippt: "Hallo Welt 01"
#
# WARUM STOPPT DIE PIPELINE DANACH?
#   Das Muster r'^.*$' passt auf ALLES. Sobald diese Regel greift,
#   wird keine weitere Regel mehr geprüft. Das ist der "Full Match Stop".
#   Mehr dazu: docs/FuzzyMapRuleGuide.md
#
# ============================================================

    # ('Hallo Welt 01', r'^hallo welt$', 0, {'flags': re.IGNORECASE}),
]
