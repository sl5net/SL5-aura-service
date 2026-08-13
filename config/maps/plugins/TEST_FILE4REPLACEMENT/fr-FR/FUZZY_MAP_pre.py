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

# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py

from scripts.py.func.get_project_root import get_aura_project_root
import re # noqa: F401
import os
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

TEST_FILE4_path = SL5NET_AURA_PROJECT_ROOT / "tools" / "tests" /  "TEST_FILE4REPLACEMENT.txt"

# aussi<-de

FUZZY_MAP_pre = [
    # EXAMPLE: zèbre

    ('.Zebra.txt',r'^(zèbre)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     ),

    (f'{TEST_FILE4_path}',r'^(Chou-fleur|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]
