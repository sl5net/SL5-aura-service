# projects/py/STT/config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import platform
import re
from pathlib import Path

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))


SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

# Apparat suche Opera suche
AURA_VARIANTS = '(Aura|Auch|Aurora|laura|dora|Ära|hurra|prora|Orange|rohre|rohrer|doras|woran|Zauberer|ora|suche|uwe|obwohl|over|oh|bohrer|aurore|rum|ruhe|tore|rot|robe|buchen|hoch|horror|auren|samurai|roche|brauche|ohh|ore|anbraten brauche|k|raucher|aachen|aber|ohren|ohr|lorenz|Opera|Apparat)'
FUZZY_MAP_pre = [

    #('ASp', fr'^(lökjlkj)$', 100, {'flags': re.IGNORECASE,}),

    #('AS', fr'^{AURA_VARIANTS}\b.*\b(ölkjlkj|suchen|zu)$', 100, {'flags':re.IGNORECASE,}),


    #('A', fr'^{AURA_VARIANTS}\b.*\b(suche|zu)$', 100, {'flags': re.IGNORECASE,}),
    #ASASASAS

    #################################################
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[Path(PROJECT_ROOT) / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################


    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}\b.*\b(suche|suchen|zu|buch)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    #         'only_in_windows': ['Konsole', 'konsole', 'Console',
    #Ohren suchenAber sucheAuch als du



]

#Ohren sucheWo warst duHerr Ludwig
