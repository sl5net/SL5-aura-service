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

# config/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.





FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.



    # EXAMPLE: Personal de VSP

    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(persona\w+)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Sra. Directora General

    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Mujer\s*s\s*p)\s*(Negocio\w+|Jefe)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Director General de Aficiones

    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Pasatiempos)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Mujer\s*s\s*p)\s*(Negocio\w+|Jefe)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Sr. Schröder

    ('Herr Schröer', r'^(Herr Schröder|Herr hersteller|Herr Schröer|herr schrill)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schroex

    ('Schröer', r'^(Schrö\w*r|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergox Schröx

    ('Ergotherapie Schröer', r'^Ergo\w* (Schrö\w*|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx Ergo

    ('Schröer Ergotherapie', r'^(Schroe\w*|jurar\w*|jurar|ya preocupado)\b Es decir\w*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergo, antes

    ('Schröer Ergotherapie', r'^(Más temprano|Espira) (bastante|es decir|primero)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


]
# Terapia ocupacional Schröer


