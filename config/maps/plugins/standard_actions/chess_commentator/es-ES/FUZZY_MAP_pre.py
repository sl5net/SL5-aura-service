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

# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [

    # --- Regla para el comentarista de ajedrez ---

    # Esta regla detecta diversas formas de diálogo interno negativo durante un juego.

    # EXAMPLE: error

    ( 'schach_kommentator_negativ', r'^\b(error|tonterías|Entonces a Tonterías|maldito|mierda|estúpido|mudo|estúpido|no Cuidado|irritante|Oh venir|el fue|perdido|I nacido\w? en)\b$', 90, { 'flags': re.IGNORECASE, 'on_match_exec': [CONFIG_DIR / '..' / 'chess_commentator.py'] }),

]

