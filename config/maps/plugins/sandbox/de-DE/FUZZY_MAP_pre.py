# projects/py/STT/config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import platform
import re
from pathlib import Path

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))


SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

# Apparat suche Opera suche
AURA_VARIANTS = '(Aura|eurer?|Auch|Aurora|Nora|laura|dora|Ära|hurra|prora|Orange|rohre|rohrer|dora|woran|Zauberer|ora|suche|uwe|obwohl|over|oh|bohrer|aurore|rum|ruhe|tore|rot|robe|buchen|hoch|horror|auren|samurai|roche|brauche|Oprah|ohh|ore|ora|anbraten brauche|k|raucher|aachen|aber|ohren|ohr|lorenz|loser|Opera|Apparat)'
Auri_VARIANTS = '()'
FUZZY_MAP_pre = [

    #('ASp', fr'^(Auri)$', 100, {'flags': re.IGNORECASE,}),

    #('AS', fr'^{AURA_VARIANTS}\b.*\b(ölkjlkj|suchen|zu)$', 100, {'flags':re.IGNORECASE,}),


    #('A', fr'^{AURA_VARIANTS}\b.*\b(suche|zu)$', 100, {'flags': re.IGNORECASE,}),
    #ASASASAS
    # ASp

    #################################################
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    #(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[Path(PROJECT_ROOT) / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    # Aura Suche
    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}[^\w]?.*[^\w]?(suche|sucht|suchen|zu|buch|zug)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),
    ('Suche wird gestartet...', fr'^(rohre zu|rohrer suche)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),


    ('Handbuch wird durchsucht...', fr'^{AURA_VARIANTS}[^\w]?.*(dokumentation|Doku|handbuch|anleitung|hilfe suchen)$', 100, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent /  'run_doc_search.py']
    }),

    #
]

#Ohren sucheWo warst duHerr LudwigHurra Doku bittetEure Dokumentationloser DokumentationDoha Doku bittet schwimmen Hurra DokumentationHurra Doku bitteDora DokumentationTore Dokumentation
