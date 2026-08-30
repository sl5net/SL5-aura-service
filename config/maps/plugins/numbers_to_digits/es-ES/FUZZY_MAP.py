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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP.py

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


    # EXAMPLE: Ninguno

    ('5', r'(\b|\d)(cinco)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('6', r'(\b|\d)(seis)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('7', r'(\b|\d)(Siete)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('8', r'(\b|\d)(ocho)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('9', r'(\b|\d)(nueve)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('10', r'(\b|\d)(diez)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('11', r'(\b|\d)(once)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('12', r'(\b|\d)(doce)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('13', r'(\b|\d)(trece)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('14', r'(\b|\d)(catorce)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('15', r'(\b|\d)(quince)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('16', r'(\b|\d)(dieciséis)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('17', r'(\b|\d)(diecisiete)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('18', r'(\b|\d)(dieciocho)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('19', r'(\b|\d)(diecinueve)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('20', r'(\b|\d)(veinte)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('30', r'(\b|\d)(treinta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('40', r'(\b|\d)(cuarenta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('50', r'(\b|\d)(cincuenta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('60', r'(\b|\d)(sesenta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('70', r'(\b|\d)(setenta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('80', r'(\b|\d)(ochenta)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('90', r'(\b|\d)(noventa)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('100', r'(\b|\d)(centenar)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Ninguno

    ('1000', r'(\b|\d)(mil)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),


]
