# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
from scripts.py.func.get_project_root import get_aura_project_root
import re # noqa: F401
import os
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

TEST_FILE4_path = SL5NET_AURA_PROJECT_ROOT / "tools" / "tests" /  "TEST_FILE4REPLACEMENT.txt"

# too<-from
FUZZY_MAP_pre = [
    # EXAMPLE: Zebra
    ('.Zebra.txt',r'^(Zebra)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     ),

    (f'{TEST_FILE4_path}',r'^(Blumenkohl)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]
