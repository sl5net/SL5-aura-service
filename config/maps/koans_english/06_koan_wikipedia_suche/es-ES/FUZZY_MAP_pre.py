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

# config/maps/koans_english/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401
from pathlib import Path

# ============================================================
# Koan 06: Búsqueda en Wikipedia por voz

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# on_match_exec puede consultar API en línea.

# Aquí: búsqueda en Wikipedia mediante comando de voz.

#
# TAREA:

# 1. Active la regla a continuación.

# 2. Diga: "¿Qué es Londres?"

#
# ¿ERRORES? Verifique el registro:

# grep "wikipedia" registro/aura_engine.log | cola -10

#
# OPCIÓN SIN CONEXIÓN:

# Ver configuración/maps/plugins/standard_actions/wikipedia_local/

#
# PRÓXIMO PASO: Koan 07

# ============================================================

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # ('¿Qué es Londres?', r'^qué es (?P<tema>.+)\?$', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'on_match_exec': [CONFIG_DIR / 'wiki_search.py']

    # }),

]
