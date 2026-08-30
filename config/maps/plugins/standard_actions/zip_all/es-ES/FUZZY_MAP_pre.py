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

# config/maps/plugins/standard_actions/zip_all/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: utilice {'flags': ...} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


CONFIG_DIR = Path(__file__).parent

    # Un archivo de tipo de cursointernalsSearch levanta el hogarinternalsChips Actualizar base de datosinternalsScript Renovar base de datosinternalsActualizar chip twitter shareinternalsTodas las carpetas SkillinternalsTodas las carpetas actualizadasinternalsUn diseño hecho por míinternalsLeer todas las carpetasTeclado MorphinReadinternalsDatos de Zwick eninternalsDatos de Jeep eninternals


    # Buscar archivos zip internos Actualizar todos los archivos Informe Actualizar archivos zip internos Encuentra tus archivos zip Informe de viaje


    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.

FUZZY_MAP_pre = [
    ('find all zips', r'''^(
            (Alle\s)?(ZIP|Sip|Chip|Tipp|Zipp|Seb)[-\s]?(Dateien|Ordner|Daten|s)?\s(suchen|hinzu|scannen|aktualisieren|einlesen|finden|checken|neu laden)
            |
            (Scanne|Suche|Aktualisiere)\s(alle\s)?(Zips|Zip-Dateien|Chips|Tipps)
            |
            (Zip|Zips)\s(Registry|Datenbank)\s(aktualisieren|erneuern)
            |
            jagen aktualisieren
            )$''', 90, {
                'flags': re.IGNORECASE | re.VERBOSE,
                'on_match_exec': [CONFIG_DIR / 'zip.py']
            }
        ),
]

# Agregar archivo zipEscaneo completo. Encontré 11 objetivos. Cremalleras actualizadas.


readme = '''
Was deckt das jetzt alles ab?
Dank der Kombinationen funktionieren nun hunderte Varianten. Hier ein paar Beispiele, die jetzt erkannt werden:

Der Standard:

"Zip Dateien suchen"
"Zips scannen"
"Zip Ordner aktualisieren"
"Alle Zips neu laden"

Die "Kreativen" (Verhörer):

"Chips suchen"
"Tipps scannen"
"Sip Dateien finden"
"Seb Ordner checken"
"Zipps einlesen"

Die Befehlsform:

"Scanne Zips"
"Aktualisiere alle Chips"

Technische Begriffe:

"Zip Registry aktualisieren"
"Zip Datenbank erneuern"

Hinweis: Ich habe re.VERBOSE (in den Flags) hinzugefügt, damit wir den Regex über mehrere Zeilen schreiben können (bessere Lesbarkeit). Falls deine Engine re.VERBOSE nicht unterstützt oder mag, sag Bescheid, dann schrumpfe ich es wieder in eine lange Zeile.

'''
