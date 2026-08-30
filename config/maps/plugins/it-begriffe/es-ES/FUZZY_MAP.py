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

# config/maps/plugins/it-terms/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/ /de-DE/FUZZY_MAP.py

# https://regex101.com/

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



    # EXAMPLE: Brighton

    ('Python', r'^(\b)(Brighton|amplio ya|Paracaídas|látigo|veces|titanio|Fallar)(\b)$', 75, {'command_flags': re.IGNORECASE}),



    # un poco radial con las siguientes líneas pero en realidad me gusta 17.11.'25 16:12 lunes

    # EXAMPLE: Brighton

    ('Python', r'(\b)(Brighton|látigo|titanio)(\b)', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Prog de tiempos

    ('Python prog', r'\bveces programa', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: ritual

    ('Virtual environment', r'\b(ritual|Virtual|virtual|viuda\w*|viudo|se convierte ya|se convierte difícil|negocio|jabalí)\w* (en |blanco |en el |a )?(Ambiente|mujer|blanco|weima|metal|blanco|cálido|blanco con|giro|y Deibel|en Frotar|frotar|Aviso)\w*\b', 75, {'command_flags': re.IGNORECASE}),


]
