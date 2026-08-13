# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# configmaps/koans allemand/05_koan_such exemple/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path

# ============================================================
# Koan 05 : Recherche vocale dans la base de données – on_match_exec

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# Les règles peuvent exécuter des scripts Python externes.

# Ici : recherche dans la base de données par commande vocale.

#
# TÂCHE:

# Dites : « Regardez dans Ruth chapitre 1 verset 1 »

#
# RÉSULTAT ATTENDU :

# Aura exécute bible_search.py et imprime le verset.

#
# EXIGENCE:

# bible_search.py et GerElb1905.db sont dans le même dossier.

#
# PROCHAINE ÉTAPE : Koan 06

# ============================================================

CONFIG_DIR = Path(__file__).parent

einleitung = """
Für diese technische Demonstration benötigen wir ein komplexes, öffentlich verfügbares Dataset in einem gängigen Format (hier: SQLite). Die Bibel dient uns in diesem Zusammenhang lediglich als ein bekanntes, frei verfügbares und vielschichtiges Beispieldokument zur Veranschaulichung von Datenbankabfragen und Recherche-Logiken.

Ich möchte betonen, dass es in dieser Einheit nicht um theologische, religiöse oder inhaltliche Interpretationen geht. Unser Fokus liegt rein auf der Implementierung und der Anwendung zur Analyse von strukturierten Textdaten.

Der entscheidende Punkt ist die Verfügbarkeit solcher Daten. Viele historische und kulturelle Texte, wie auch die Bibel in verschiedenen Übersetzungen, sind glücklicherweise als Open-Source-Datenbestände verfügbar, was uns die technische Arbeit ermöglicht. Wir könnten an dieser Stelle ebenso gut ein juristisches Kompendium oder einen wissenschaftlichen Fachartikel analysieren.

Bitte fragen Sie Ihren Admin, das er
aura.sl5.de:8831
einschaltet. Dies demonstriert die Nutzung von Aura auch Online für Web-Seiten.
Diese Demo-Seite ( aura.sl5.de:8831 ) wird nur auf Anfrage aktiviert.

"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.



    # À FAIRE : Activez le résultat net en supprimant le symbole de commentaire

    # ('recherche dans Ruth chapitre 1 verset 1', fr'^.*$', 90, {'command_flags' : re.IGNORECASE,'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    #


    # À FAIRE : Que se passe-t-il maintenant ?


    # EXAMPLE: recherche dans le texte x chapitre 123 texte vfdph 123

    ('bible suche', r'^recherche dans (?P<livre>\w*[ ]?\w+) chapitre (?P<chapitre>\d+) [vfdph]\w+ (?P<versets>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # À FAIRE : Pourriez-vous inventer d’autres options de recherche ?



]


