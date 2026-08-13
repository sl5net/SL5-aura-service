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

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP_pr.py

import re

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


"""
Important: Please apply the regular expressions in the correct order.

You must use the composite (more general) regular expression first, and then apply the specialized one.

The reason is that if the shorter, specialized regex runs first, it might match a part of the string that is essential for the larger, composite regex. This would make it impossible for the composite regex to find its match afterwards.
"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.

    # EXAMPLE: texto del título

    ('Timo Stösser', r'^(ti\w+r|T\w+i\w+o)\s+(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Stoffe|Schlösser|stöße|stöpsel|Störche)$', 7, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: texto del título

    ('Timo', r'\b(ti\w+r|T\w+i\w+o)\b', 70, {'command_flags': re.IGNORECASE,
        'only_in_windows': [r'correo electrónico',r'gmail',r'correo electrónico',r'bandeja de entrada']}),

    # EXAMPLE: Stäfa

    ('Stösser', r'^(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Schlösser|stöße|stöpsel|Störche)$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: jefe de departamento

    ('Fachbereichsleitung', r'^(jefe de departamento)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: libro de texto

    ('Python-Buch', r'^(\w+t\wn Libro)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: libro de pitón

    ('Python-Buch', r'^(Python Libro)$', 60, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Btextixtlibro de texto

    ('Python-Buch', r'^(B\w+i\peso\w+ Libro)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: libro de pitón

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Libro)$', 60, {'command_flags': re.IGNORECASE}),

    # ('Curso de formación de instructores', r'^(Curso de instructor\s*schu\w*| Formación de profesores Formación de profesores)$', 60, {'command_flags': re.IGNORECASE})


    # EXAMPLE: Instructor

    ('Kursleiterschulung', r'^(Instructor|Profesores)[\w\s]*(\s*sho\w*|Formación adicional)$', 60, {'command_flags': re.IGNORECASE})

]

# Timo Stösser



# Libro de Python para la formación de instructores, jefe de departamento

# Libro de Python libro amplio Libro de Python Libro de Python en en el libro

# Libro Brighton Libro Python Libro Whip Libro anchoTimoTchibo Plunge

# Segundo libro en Dead Book Libro de Python Libro ancho Libro ancho Libro de Python

# Saludos libro

# libro de pitón

