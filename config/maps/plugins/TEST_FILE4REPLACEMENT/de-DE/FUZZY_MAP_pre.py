# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
import os
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

TEST_FILE4_path = PROJECT_ROOT / "tools" / "tests" /  "TEST_FILE4REPLACEMENT.txt"

# too<-from
FUZZY_MAP_pre = [
    # EXAMPLE: Zebra
    ('.Zebra.txt',r'^(Zebra|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     ),

    (f'{TEST_FILE4_path}',r'^(Blumenkohl|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]