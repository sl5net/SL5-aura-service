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

# configmaps/koans deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# ============================================================
# Koan 02: Tu primera regla de expresiones regulares: ¿activada o desactivada?

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# Las reglas de expresiones regulares pueden aplicar varias palabras habladas a una

# Comando de mapa. Aquí: Los grupos de letras controlan "activado"/"desactivado".

#
# TAREA:

# 1. Elimine el '#' antes de UNA de las dos reglas siguientes.

# 2. Guardar: Aura se recarga la próxima vez que presiones el botón.

# 3. Di una palabra que comience con a-m (por ejemplo, "hola")

# o uno que comience con n-z (por ejemplo, "agua").

#
# RESULTADO ESPERADO:

# "hola" → "a"

# "agua" → "fuera"

#
# PREGUNTA PARA PENSAR:

# ¿Qué pasa si activas ambas reglas al mismo tiempo?

# ¿Cuál ganará y por qué?

# Consejo: las reglas se procesan de arriba a abajo.

#
# PRÓXIMO PASO: Koan 03

# ============================================================

FUZZY_MAP_pre = [
    # ('an', r'^[a-m]+.*$'),

    # ('apagado', r'^[n-z]+.*$'),

]
