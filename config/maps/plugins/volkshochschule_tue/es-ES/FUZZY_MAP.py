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

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP.py

import re

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - significa que primero es lo más importante, es posible que las reglas inferiores no se lean.



    # EXAMPLE: Timo Stösser

    ('Timo Stösser', r'\b(thiem\w|timo|thema|ti\w+r)\s+(stäfa|steffen|Stefan|stripper|stefan|stürze\w*|stütze\w*|Sturz|stösse|Schlösser|stöße|stößt|Stöße|stöpsel|stärker|Störche)\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: Gerente de departamento

    ('Fachbereichsleitung', r'\bAsunto\w*\s+Gestión de área\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: PBW textix tx ex libro

    ('Python-Buch', r'\b([PBW]\w+i\w*t\w*e\w* Libro)\b', 60, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: formación de instructores

    ('Kursleiterschulung', r'\b(Instructor\s*sho\w*)\b', 60, {'command_flags': re.IGNORECASE})



]

