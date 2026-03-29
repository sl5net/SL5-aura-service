# projects/py/STT/config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import platform
import re
from pathlib import Path

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))


SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

AURA_VARIANTS = '(Aura|Auch|Aurora|laura|dora|Ära|hurra|prora|Orange|rohre|rohrer|doras|woran|Zauberer)'
FUZZY_MAP_pre = [


    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}\b.*\b(suche|zu)$', 100, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"]
    }),


]

#Ohren sucheWo warst duHerr Ludwig
