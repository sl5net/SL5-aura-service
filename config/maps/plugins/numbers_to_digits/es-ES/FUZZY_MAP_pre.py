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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP_pre.py


import re

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



    # EXAMPLE: Ninguno

    ('1', r'(\b|\d)(uno)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('2', r'(\b|\d)(dos)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('3', r'(\b|\d)(tres)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('4', r'(\b|\d)(cuatro)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('5', r'(\b|\d)(cinco)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('6', r'(\b|\d)(seis)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('7', r'(\b|\d)(Siete)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('8', r'(\b|\d)(ocho)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('9', r'(\b|\d)(nueve)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('10', r'(\b|\d)(diez)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Ninguno

    ('15', r'(\b|\d)(quince)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

# one2025-1005-1324 uno uno en Hola Heinz uno

# 5 3ich 5 río 4nlosönun0uno cero cinco


    # EXAMPLE: cero

    ('0', r'^(cero|no|entonces|ir)$', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: cero

    ('0', r'(\b|\d)(cero)(\b|\d)', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Ninguno

    ('1', r'(\b|\d)(uno)(\b|\d)', 99, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('2', r'(\b|\d)(dos|gritar|dos|u)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('3', r'(\b|\d)(tres)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('4', r'(\b|\d)(cuatro)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('5', r'(\b|\d)(cinco)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('6', r'(\b|\d)(seis|cheques)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('7', r'(\b|\d)(Siete|empujar)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('8', r'(\b|\d)(ocho)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('9', r'(\b|\d)(nueve)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('10', r'(\b|\d)(diez)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('11', r'(\b|\d)(once)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('12', r'(\b|\d)(doce)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('13', r'(\b|\d)(trece)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('14', r'(\b|\d)(catorce)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('15', r'(\b|\d)(quince)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('16', r'(\b|\d)(dieciséis)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('17', r'(\b|\d)(diecisiete)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('18', r'(\b|\d)(dieciocho)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('19', r'(\b|\d)(diecinueve)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('20', r'(\b|\d)(veinte)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('21', r'(\b|\d)(veintiuno)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('22', r'(\b|\d)(Veintidós)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('23', r'(\b|\d)(veintitrés)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('24', r'(\b|\d)(veinticuatro)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('25', r'(\b|\d)(cremallera se convierte veinte|Veinticinco)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('26', r'(\b|\d)(veintiséis)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('27', r'(\b|\d)(veintisiete)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('28', r'(\b|\d)(veintiocho)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('29', r'(\b|\d)(veintinueve)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('30', r'(\b|\d)(treinta)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('40', r'(\b|\d)(cuarenta)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('50', r'(\b|\d)(cincuenta)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('60', r'(\b|\d)(sesenta)(\b|\d)', 78, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('70', r'(\b|\d)(setenta)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('80', r'(\b|\d)(ochenta)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('90', r'(\b|\d)(noventa)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('100', r'(\b|\d)(centenar|ciento)(\b|\d)', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('1000', r'(\b|\d)(mil)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('2024', r'(\b|\d)(dos mil\s*veinticuatro)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('2025', r'(\b|\d)(dos mil\s*Veinticinco)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Ninguno

    ('2026', r'(\b|\d)(dos mil\s*veintiséis|dos mil\s*seis\s*y\b.*)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # JOIN_NUMBERS_EVERYWHERE: siempre junta los dígitos si son adyacentes. no funciona a plena potencia (en algún lugar de su cadena)

    # EXAMPLE: 1 1

    (r'\1', r'(\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # JOIN_NUMBERS_AT_END: junta los dígitos si solo siguen números/espacios

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']})

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']})


    # QUITAR 1 ESPACIO ENTRE 2 NÚMEROS fullmachtch

    # (r'\1\2', r'^(\d+)\s+(\d+)$', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




]


