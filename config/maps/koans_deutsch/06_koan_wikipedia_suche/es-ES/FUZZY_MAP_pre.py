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

# configmaps/koans deutsch/06 koan_wikipedia search/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# ============================================================
# Koan 06: búsqueda en Wikipedia por voz

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# on_match_exec también puede consultar API en línea.

# Aquí: búsqueda en Wikipedia mediante comando de voz.

#
# TAREA:

# 1. Active la regla a continuación.

# 2. Diga: “¿Qué es Tubinga?”

#
# ¿ERROR? Verifique el registro:

# grep "wikipedia" registro/aura_engine.log | cola -10

#
# VERSIÓN SIN CONEXIÓN:

# Ver configuración/maps/plugins/standard_actions/wikipedia_local/

#
# PRÓXIMO PASO: Koan 07

# ============================================================


CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.



    # TODO: Activar la línea inferior eliminando el símbolo de comentario

    # ('¿Qué es Tubinga?', fr'^.*$', 90, {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


]



tips = r"""

TODO: Was passiert jetzt?
TODO: Mehr Informationen, Fehlermeldungen usw, erhalten wir meisens, wenn wir die Log lesen:

log/aura_engine.log

Den Fehler können wir unter Windows folgendermasen reparieen:

.\.venv\Scripts\activate.bat


.\.venv\Scripts\python.exe  -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install wikipedia

Warum bekommen wir immernoch einen Fehler das wikipediaapi nicht funktioniert?

Wir veruchen

.\.venv\Scripts\python.exe -m pip install wikipediaapi

aber bekommen:

ERROR: Could not find a version that satisfies the requirement wikipediaapi

Dieses Plugin beispiel wurde unter Linux erstellt, aber wird jetzt unter Windows ausgeführt.

Versuchen Sie

.\.venv\Scripts\python.exe -m pip install wikipedia-api

funktioniert es jetzt?

Warum?

# Wikipedia sin conexión #########################################################


Geht es auch komplett offline? Ja. Z.B.

mit Hilfe von

https://library.kiwix.org/#lang=deu&q=wikipedia



Nötige Speicherplatz zwischen 50 Gigabyte und 20 MB (Auswahl)

Gute Wahl: 3,54 GB ohne Bilder:
https://browse.library.kiwix.org/viewer#wikipedia_de_all_mini_2025-09
https://download.kiwix.org/zim/wikipedia/wikipedia_de_all_mini.zim

Eine der möglichen Variante der Nutzung ist über Docker:

sudo systemctl enable --now docker.socket

Jetzt, da der Inhalt als Webseite verfügbar ist, kann Ihr Python-Skript ihn wie jede andere Webseite verarbeiten.

Ein Beispiel-Py-Script dafür findet sich hier: config/maps/plugins/standard_actions/de-DE/wikipedia_local.py


"""




