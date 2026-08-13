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

# config/maps/plugins/ki-maker-space/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.




"""

Mi

 Reboot - Wednesday



Do

Scratch-Thursday

    OpenLab:  11:00 - 22:00 Uhr



Fr

Fabric-Friday:  Feiertag - 3.10.2025

Open Lab ist geschlossen.

DO
Do
Scratch-Thursday
    OpenLab:  11:00 - 22:00 Uhr

Sa

Supercreative-Saturday

"""
FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


    # ki make espace AI despertadores AI en el camino es k Conversación por correo electrónico A través de una conversación por correo electrónico

    # Sacos K i Makerspace Sacos KI Aspen

    # Bloqueado por correo electrónico ki-maker.space


    # EXAMPLE: fabricante de ki

    ('ki-maker.space', r'^(ki-fabricante|ki[\s]*hacer[\sí]*espacio|k i [\s]*hacer[\s\w]*espacio|espacio|ki despertador|AI en el lejos es|AI Sacos álamo temblón|Caín destruido|K \w*\s*hacer espacio|AI él|K i \w+ \w*|ki menkes)\s*\w*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: gregorio

    ('Gregor Schulte, 07071- 6395627 Gregor.Schulte@ki-maker.space', r'^(gregorio|Schulte|ki-fabricante.espacio)\s*\w*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Oficina ki-maker.espacio x

    ('Bulsat', r'^(Oficina ki-fabricante.espacio)\s*\w*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # Gregor entrenó a Gregor

    # Por conversación por correo electrónico K i bolsas de respeto


]

