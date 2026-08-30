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

# config/maps/plugins/wannweil/de-DE/FUZZY_MAP_pre.py

import re

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


# La salchicha sería interna


    # EXAMPLE: Compartir iglesias

    ('Kirchentellinsfurt', r'\b(iglesias\s*dividir|Kirchentellinsfurt|cantarín sostiene)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ayuntamiento

    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(Ayuntamiento|contacto)\b\s*\b(iglesias\s*dividir|Kirchentellinsfurt)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: el ayuntamiento sigue tintineando

    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(ayuntamiento cantarín sostiene)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),


# zieglersche https://www.zieglersche.de/altenhilfe.html pflegheim


# El Ayuntamiento sigue tintineando

# El sonido de la madera dura tintineando


    # EXAMPLE: quien cachorro

    ('Wannweil', r'\b(OMS\s*Cachorro)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: quien cachorro

    ('Wannweil', r'\b(OMS\s*Cachorro)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),
    # EXAMPLE: cuando porque

    ('Wannweil', r'^\s*(cuando porque|Annweiler|Cuando\s*porque|Cuando\s*Cuando\s*porque|Cuando\s*era\s*Señor|Cuando\s*era\s*él|A\s*porque|Cuando\s*llorar\w*|Cuando\s*vino|Furgoneta\s*porque|Cuando Qué)\s*$', 70, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: corredor sebastian

    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura|lauf|lauf war)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: cifra

    ('Sigune Lauffer', r'\b(Figur|Sekunde|zugrunde|sigourney|sheego|Sie gute|gun|Ski gute|c gute|Schick ohne|sheikh ohne|gleich ohne|shi gunilla|spione)'
                       # EXAMPLE: corredor

                       r' (corredor|corredor|Lauffer|correr|correr|correr|laura|correr era|en eso esperar|en montón|detener|nariz)\b', 82, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: estaRegexWillNeverMatch123ABC

    ('TestFuzzyNiemalsMatchen', r'\b(esta expresión regular nunca coincidirá123abecedario)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # ('TestFuzzyAlways', r'\b(thisRegexWillAlwaysMatch)\b', 1, # min_accuracy{'command_flags': re.IGNORECASE}),



    # EXAMPLE: Mentes paradigmáticas

    ('pragmatic minds GmbH 2019', r'\b(paradigma Mentes)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),



]

