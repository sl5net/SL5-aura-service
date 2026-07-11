# config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py
import os
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

from pathlib import Path
import runpy


tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent

acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]
suche = r'(such|suche|suche du|sucht|suchen|sure|Schuhe|hoover|buch|zug|Zuge|stiefel|schlüchtern)'

_meta_run_search_result = {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    # EXAMPLE: py
    'only_in_windows': [ r'\.py'],
}
# Sherlock
FUZZY_MAP_pre = [

    # EXAMPLE: log
    ('log', r'^(log|look|Programm geladen. Viel Spaß|woran lernmodus deaktivieren|ausprobieren|blumenkohl|das ist überraschend)$', 70, _meta_run_search_result),

    # EXAMPLE: log
    ('log', fr'^{AURA_VARIANTS}\s*(logik|logdateien|log-datei|logdateien|logging|rainer|ein rock|lockt hat|ein okt hat|log-datei|logdatei|eine logdatei|ein oktett|ein log-datei)$', 70, _meta_run_search_result),

    # EXAMPLE: log
    ('log', fr'^{AURA_VARIANTS}\s*(log|look)$', 70, _meta_run_search_result),

    # EXAMPLE: Lernmodus einschalten ausschalten
    ('Lernmodus...', fr'^{AURA_VARIANTS}.*lernmodus (an\w*|ein\w*|aus\w*|starten|stoppen|aktivier\w+|DEAKTIVIER\w*)\s*\w*$', 100, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),


    # --- Training-Plugin (wird vom Skript oben ein/ausgeschaltet) ---


    #Orange rot

    # EXAMPLE: Aura sourcecode
    ('scripts', fr'^{AURA_VARIANTS}\s*(als)?\s*(sourcecode|quelltext|schwarz quote|schwarz|funkt\w+|methoden|sowas|kuchen quelltext)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # EXAMPLE: Aura suche sourcecode
    (r'scripts', fr'^{AURA_VARIANTS}\s+{suche}\s+(sourcecode|quelltext|schwarz|schwarz # quote|funkt\w+|methoden|sowas|kuchen quelltext)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),


    # EXAMPLE: Aura Konfiguration
    (r'config', fr'^{AURA_VARIANTS}\s+(config\w*|konfig\w*|Einstell\w*|konfit\w*)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # aura konfitüre

    # EXAMPLE: Aura Suche result #  Homer suche Dokumente
    ('~/Dokumente', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<dirpath>(dok\w+|ducken))$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # deprecated method? Maybe use run_search_the_result.py?
    # EXAMPLE: Aura Suche subject
    ('Suche Subject wird gestartet...', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<dirpath>\w+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_subject.py"],
    }),

    # deprecated method? Maybe use run_search_the_result.py?
    # Aura Suche
    # EXAMPLE: AURA_VARIANTS x suche
    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}[^\w]?.*{suche}$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    # EXAMPLE: rohre zu
    ('Suche wird gestartet...', r'^(rohre zu|rohrer suche|orange hoch)$', 100, {
    'flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),


    # deprecated method? Maybe use run_search_the_result.py?
    # Handbuch wird durchsucht...
    # EXAMPLE: AURA_VARIANTS x dokux
    ('Handbuch wird durchsucht...', fr'^{AURA_VARIANTS}[^\w]?.*(doku\w*|handbuch\w*|anleitung\w*|gemündet|hilfe\w*|du güntert|der konvent touch|drucker mittels|logo mündel)\s*(zu|suchen|\w+)?$', 100, {
        'flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent /  'run_doc_search.py']
    }),

]