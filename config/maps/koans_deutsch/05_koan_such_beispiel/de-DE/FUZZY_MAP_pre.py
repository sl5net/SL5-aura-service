# config/maps/koans_deutsch/05_koan_such_beispiel/de-DE/FUZZY_MAP_pre.py
# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite

import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

einleitung = """
Für diese technische Demonstration benötigen wir ein komplexes, öffentlich verfügbares Dataset in einem gängigen Format (hier: SQLite). Die Bibel dient uns in diesem Zusammenhang lediglich als ein bekanntes, frei verfügbares und vielschichtiges Beispieldokument zur Veranschaulichung von Datenbankabfragen und Recherche-Logiken.

Ich möchte betonen, dass es in dieser Einheit nicht um theologische, religiöse oder inhaltliche Interpretationen geht. Unser Fokus liegt rein auf der Implementierung und der Anwendung zur Analyse von strukturierten Textdaten.

Der entscheidende Punkt ist die Verfügbarkeit solcher Daten. Viele historische und kulturelle Texte, wie auch die Bibel in verschiedenen Übersetzungen, sind glücklicherweise als Open-Source-Datenbestände verfügbar, was uns die technische Arbeit ermöglicht. Wir könnten an dieser Stelle ebenso gut ein juristisches Kompendium oder einen wissenschaftlichen Fachartikel analysieren.


"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    #TODO: Untere Zeile aktivieren, duch entfernen des Kommentar Symbols
    #('suche in Ruth kapitel 1 vers 1', fr'^.*$', 90, {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    #


    #TODO: Was passiert jetzt?

    # EXAMPLE: suche in x text kapitel 123 vfdph text 123
    ('bible suche', fr'^suche in (?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    #TODO: Könnten sie noch ein paar andere Suchmöglichkeiten erfinden?


]


