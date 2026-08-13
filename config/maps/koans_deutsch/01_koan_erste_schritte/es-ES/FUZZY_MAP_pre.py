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

# configmaps/koans deutsch/01_koan_erste_stiege/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# también <-de

FUZZY_MAP_pre = [

# ============================================================
# Koan 01: Tu primera regla – ¡Bienvenido a Aura!

# ============================================================
#
# Requisito: Aura ya se está ejecutando y su tecla de acceso rápido está configurada.

# Si no: consulte docs/GettingStarted.md

#
# TAREA:

# Elimine el '#' delante de la regla siguiente (línea con 'hola mundo').

# Guarde el archivo. Aura carga la regla en la siguiente pulsación de tecla

# (Activador de tecla de acceso rápido) automáticamente nuevo: en modo inactivo, Aura duerme completamente.

# Luego presione su tecla de acceso rápido y diga: "hola mundo"

#
# RESULTADO ESPERADO:

# Tipos de aura: “Hola mundo 01”

#
# ¿POR QUÉ SE DETIENE EL TUBO DESPUÉS DE ESTO?

# El patrón r'^.*$' se adapta a TODO. Tan pronto como se aplique esta regla,

# no se verifica ninguna otra regla. Esta es la “Parada completa del partido”.

# Más sobre esto: docs/FuzzyMapRuleGuide.md

#
# ============================================================

    # ('Hola mundo 01', r'^hola mundo$', 0, {'command_flags': re.IGNORECASE}),

]
