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

# configmaps/koans alemán/05_koan_such ejemplo/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# ============================================================
# Koan 05: Búsqueda de bases de datos por voz – on_match_exec

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# Las reglas pueden ejecutar scripts de Python externos.

# Aquí: búsqueda en base de datos mediante comando de voz.

#
# TAREA:

# Diga: "Mira en Rut capítulo 1 versículo 1"

#
# RESULTADO ESPERADO:

# Aura ejecuta bible_search.py e imprime el versículo.

#
# REQUISITO:

# bible_search.py y GerElb1905.db están en la misma carpeta.

#
# PRÓXIMO PASO: Koan 06

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
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.



    # TODO: Activar la línea inferior eliminando el símbolo de comentario

    # ('buscar en Rut capítulo 1 versículo 1', fr'^.*$', 90, {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),




    # TODO: ¿Qué pasa ahora?


    # EXAMPLE: buscar en x texto capítulo 123 vfdph texto 123

    ('bible suche', r'^buscar en (?P<libro>\w*[ ]?\w+) capítulo (?P<capítulo>\d+) [vfdph]\w+ (?P<versos>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # TODO: ¿Podrías inventar otras opciones de búsqueda?



]


