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

# config/maps/koans_2_peter_deutsch/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

# PETER TAREA para Koan: 06_koan_wikipedia_suche

#
# Este complemento busca el término hablado en Wikipedia.

# Ejemplo: El usuario dice "wiki que es una casa"

# -> El complemento busca "qué es una casa" en Wikipedia

#
# La siguiente regla activa el complemento de Wikipedia para TODAS las entradas (^.*$).

# Después del partido, el complemento se ejecuta y la canalización se detiene.

#
# TAREA: Elimina el '#' delante de la regla para activarla.

# PREGUNTA: ¿Qué pasa cuando dices algo? Luego mira en: log/aura_engine.log


FUZZY_MAP_pre = [
    # ('¿Qué es Tubinga?', fr'^.*$', 90, {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

]
