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

# config/maps/plugins/bible_search/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


CONFIG_DIR = Path(__file__).parent

examples = r"""

Verwendung:

Beispiele:

Suche in Ruth Kapitel 1 Vers 1
Suche in erster Dave Kapitel 1 Vers halten
Suche in 1 Chroniken 1 Kapitel 1

Varianten um das gleiche zu Fragen:

Suche in Ruth Kapitel 1 Vers 1
# EXAMPLE: recherche itext x texte chapitre 123 vfdph texte 123

('bible suche', r'^recherche (i\w+ )?(?P<livre>\w*[ ]?\w+) chapitre (?P<chapitre>\d+) [vfdph]\w+ (?P<versets>\d+)$', 90, { ...

Suche in Ruth Kapitel 1 1 Vers
# EXAMPLE: recherche itext x texte chapitre 123 123 texte vfdph

('bible suche', r'^recherche (i\w+ )?(?P<livre>\w*\s*\w+) chapitre (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {...

Suche in Ruth 1 Kapitel 1 Vers
# EXAMPLE: recherche itext x texte 123 chapitre 123 texte vfdph

('bible suche', r'^recherche (i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) chapitre (?P<versets>\d+) [vfdph]\w+$', 90, {...

"in" kann auch weggelassen werden.


Suche in Ruth Kapitel 1 Vers 1
Ruth 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Und es geschah in den Tagen, als die Richter richteten, da entstand eine Hungersnot im Lande. Und ein Mann von Bethlehem-Juda zog hin, um sich in den Gefilden Moabs aufzuhalten, er und sein Weib und seine beiden Söhne.

Suche in erster Dave Kapitel 1 Vers halten

Suche in 1 Chroniken 1 Kapitel 1
Joel 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Das Wort Jehovas, welches zu Joel, dem Sohne Pethuels, geschah.
suche ihn 1 codec les kapitel 1 ps ein

I Chronicles 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Adam, Seth, Enos,

Suche in 1 t'gallo tot als 1 Kapitel 1 Vers'

"""


# EXAMPLE: recherche ãJ bible

searchCmd=r'(recherche \w+ Bible|recherche|Bible)'

# EXAMPLE: la via

Thessalonians = r"(ils via|t[\w ']*chal[\w ]*w[\w ]*o[\w ]*a[\w ]*s|t\w*\s*\w*s|k\w*e\w*alonia\w*\s*\w*)\b"



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.



    # Le livre « Lévitique » n'existe pas dans la traduction « GerElb1905 ».

    # EXAMPLE: Lévitique

    ('Leviticus', r'\blévitikus\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: cx lire

    ('Chronicles', r'\b(c\w*\s*lire|Manuscrit\s*lire|frère\w*\s*permettons)\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),





    # ('Timothée', rf"(timotheus|tee[ \w]*io[ \w\-]*tee|t[ \w]+tes)\b", 90, {

    # 'command_flags' : re.IGNORECASE,

    # 'skip_list' : ['LanguageTool'],

    # }),



    # À FAIRE : la recherche dans II Timothy est buggée 9.11.'25

    # ('recherche dans II Timothée', rf"(recherche en seconde) ([\w ]+ee|[\w ]+sy)\b", 90, {

    # 'command_flags' : re.IGNORECASE,

    # 'skip_list' : ['LanguageTool'],

    # }),








    # EXAMPLE: rechercher dans 1

    ('suche in I Thessalonians', rf"suche in (1|erster) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: recherche en 2

    ('suche in II Thessalonians', rf"suche in (2|zweiter) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: Rechercher dans

    ('suche in II', r'^Recherche (dans le|dans) \continuer\w*', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: recherche dans le deuxième texte

    ('suche in II Samuel', r'recherche dans deuxième (s\w+|rencontré)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: premierex

    # ('1', r'\b(premier\w*|plus sérieux)\b', 90, {

    # 'command_flags' : re.IGNORECASE,

    # 'skip_list' : ['LanguageTool'],

    # }),

    # EXAMPLE: secondex

    ('2', r'\respectivement\w*\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: Rechercher dans Levx

    ('Suche in Leviticus', r'\bRecherche dans (Lév\w*\b|\w.*court\b|.*baiser)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),




    # EXAMPLE: verset

    ('Vers 1', r'\b(verset|lecteurs) (un|mentionné|loin)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: sois juste

    ('Vers 1', r'\b(équitable être)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: VAR itext x texte chapitre 123 verset texte 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*[ ]?\w+) chapitre (?P<chapitre>\d+) [vfdph]\w+ (?P<versets>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: VAR itext x texte chapitre 123 123 texte du verset

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*\s*\w+) chapitre (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: VAR itext x texte 123 chapitre 123 texte du verset

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) chapitre (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    # EXAMPLE: VAR itext x texte 123 Texte du verset 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*[ ]?\w+) (?P<chapitre>\d+) [vfdph]\w+ (?P<versets>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Rechercher Ruth 123 123 verset

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Rechercher Ruth 123 123 verset

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),


    # maintenant recherche expérimentale plus agressive (cela écrase peut-être d'autres plugins) (S.11.11.'25 09:13 mar)


    # EXAMPLE: Ruth chapitre 123 verset 123

    ('bible suche', r'^(i\w+ )?(?P<livre>\w*[ ]?\w+) chapitre (?P<chapitre>\d+) [vfdph]\w+ (?P<versets>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Texte de Ruth chapitre 123 123 verset

    ('bible suche', r'^(i\w+ )?(?P<livre>\w*\s*\w+) chapitre (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Ruth 123 chapitre 123 verset

    ('bible suche', r'^(i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) chapitre (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),




    # ce qui suit est en conflit avec des règles telles que : combien font 5 plus 3 (voir, 11.11.'25 13:35 mar)

    # C'était un peu difficile à trouver


    # ('recherche biblique', fr'^(i\w+ )?(?P<livre>\w*[ ]?\w+) (?P<chapitre>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {

    # 'command_flags' : re.IGNORECASE,

    # 'on_match_exec' : [CONFIG_DIR / 'bible_search.py']

    # }),



    # EXAMPLE: Ruth 123 123 verset

    ('bible suche', r'^(i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Qu'est-ce que Ruth 1 1 verset

    ('bible suche', r'^(i\w+ )?(?P<livre>\w*\s*\w+) (?P<chapitre>\d+) (?P<versets>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),



]















