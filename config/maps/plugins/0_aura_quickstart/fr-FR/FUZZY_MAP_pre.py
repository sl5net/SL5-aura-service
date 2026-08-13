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

# config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py

from scripts.py.func.get_project_root import get_aura_project_root
import os
import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702


from pathlib import Path
import runpy


tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

CONFIG_DIR = Path(__file__).parent

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]
suche = r'(recherche|recherche|recherche toi|cherche|chercher|bien sûr|Chaussures|aspirateur|livre|former|former|bottes|sommeil)'

_meta_run_search_result = {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    # EXAMPLE: py

    'only_in_windows': [ r'\.py'],
}
# Sherlock

FUZZY_MAP_pre = [

    # EXAMPLE: enregistrer

    ('log', r'^(enregistrer|regarder|programme chargé. Beaucoup Amusant|quoi mode dapprentissage désactiver|essayer|chou-fleur|le est surprenant)$', 70, _meta_run_search_result),

    # EXAMPLE: enregistrer

    ('log', fr'^{AURA_VARIANTS}\s*(logique|fichiers journaux|enregistrer-déposer|fichiers journaux|enregistrement|pluvieux|un rocher|tente a|un Octobre a|enregistrer-déposer|fichier journal|un fichier journal|un octuor|un enregistrer-déposer)$', 70, _meta_run_search_result),

    # EXAMPLE: enregistrer

    ('log', fr'^{AURA_VARIANTS}\s*(enregistrer|regarder)$', 70, _meta_run_search_result),

    # config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py:38

    # apprendre à allumer



    # Apprenez l'aura, éliminant ainsi

    # EXAMPLE: Activer et désactiver le mode d'apprentissage

    ('Lernmodus...', fr'^({AURA_VARIANTS}|Lauer vide).*(apprendre|vide|apprendre|Bruit|Monsieur)?\s*(mode|mode|doit|à travers lequel)\s*(à\w*|un\w*|de\w*|exc\w+|Absch\w+|commencer|arrêt|activer\w+|DÉSACTIVER\w*)?\s*\w*$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),



    # --- Plugin de formation (activé/désactivé par le script ci-dessus) ---



    # Rouge orangé


    # EXAMPLE: Code source de l'aura

    ('scripts', fr'^{AURA_VARIANTS}\s*(comme)?\s*(code source|code source|noir citation|noir|travaux\w+|méthodes|comme ça|gâteau code source)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # EXAMPLE: Code source de recherche Aura

    (r'scripts', fr'^{AURA_VARIANTS}\s+{suche}\s+(code source|code source|noir|noir # citation|travaux\w+|méthodes|comme ça|gâteau code source)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),


    # EXAMPLE: Configuration de l'aura

    (r'configuration', fr'^{AURA_VARIANTS}\s+(configuration\w*|configuration\w*|Paramètres\w*|confit\w*)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # confiture d'aura


    # EXAMPLE: Résultat de la recherche Aura # Documents de recherche Homer

    ('~/Dokumente', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<chemin de détour>(doc\w+|canard))$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # méthode obsolète ? Peut-être utiliser run_search_the_result.py ?

    # EXAMPLE: Sujet de recherche Aura

    ('Suche Subject wird gestartet...', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<chemin de détour>\w+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_subject.py"],
    }),

    # méthode obsolète ? Peut-être utiliser run_search_the_result.py ?

    # Recherche d'aura

    # EXAMPLE: AURA_VARIANTS x recherche

    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}[^\w]?.*{suche}$', 100, {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    # EXAMPLE: tuyaux fermés

    ('Suche wird gestartet...', r'^(tube à|Rohrer recherche|orange haut)$', 100, {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),


    # méthode obsolète ? Peut-être utiliser run_search_the_result.py ?

    # Recherche du manuel...

    # EXAMPLE: AURA_VARIANTS x dokux

    ('Handbuch wird durchsucht...', fr'^{AURA_VARIANTS}[^\w]?.*(documentaire\w*|manuel\w*|instructions\w*|abouti|aide\w*|toi Gunter|le couvent touche|imprimante au moyen de|logo salle)\s*(à|chercher|\w+)?$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent /  'run_doc_search.py']
    }),

]
