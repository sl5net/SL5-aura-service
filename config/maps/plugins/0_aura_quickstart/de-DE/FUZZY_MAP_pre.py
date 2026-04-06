# config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py
import os
import re # noqa: F401
from pathlib import Path
import runpy


tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent

acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]

FUZZY_MAP_pre = [
    # ('zyäzwnyöxü', r'^(zyxü)$', 10),

    # --- Sprachsteuerung für den Lernmodus ---
    ('Lernmodus...', fr'^{AURA_VARIANTS}.*lernmodus (an\w*|ein\w*|aus\w*|starten|stoppen)$', 100, {
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),


    # --- Training-Plugin (wird vom Skript oben ein/ausgeschaltet) ---
    # (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),

    # EXAMPLE: Aura Suche subject
    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}\s+(such|suche|sucht|suchen|sure|buch|zug|stiefel|schlüchtern)\s+(?P<dirpath>\w+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_subject.py"],
    }),
    # Oberstufe KonfigurationAura stiefel Kon   figuration

    # Aura Suche
    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}[^\w]?.*(such|suche|sucht|suchen|buch|zug)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    ('Suche wird gestartet...', r'^(rohre zu|rohrer suche)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    #
    # Handbuch wird durchsucht...
    ('Handbuch wird durchsucht...', fr'^{AURA_VARIANTS}[^\w]?.*(doku\w*|handbuch\w*|anleitung\w*|gemündet|hilfe\w*|du güntert|der konvent touch|drucker mittels|logo mündel)\s*(zu|suchen|\w+)?$', 100, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent /  'run_doc_search.py']
    }),

]
