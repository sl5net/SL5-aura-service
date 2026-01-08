# config/maps/plugins/bible_search/de-DE/FUZZY_MAP_pre.py
# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite

import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

examples = r"""

Verwendung:

Beispiele:

Suche in Ruth Kapitel 1 Vers 1
Suche in erster Dave Kapitel 1 Vers halten
Suche in 1 Chroniken 1 Kapitel 1

Varianten um das gleiche zu Fragen:

Suche in Ruth Kapitel 1 Vers 1
# EXAMPLE: suche itext x text kapitel 123 vfdph text 123
('bible suche', r'^suche (i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, { ...

Suche in Ruth Kapitel 1 1 Vers
# EXAMPLE: suche itext x text kapitel 123 123 vfdph text
('bible suche', r'^suche (i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {...

Suche in Ruth 1 Kapitel 1 Vers
# EXAMPLE: suche itext x text 123 kapitel 123 vfdph text
('bible suche', r'^suche (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) kapitel (?P<verse>\d+) [vfdph]\w+$', 90, {...

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


# EXAMPLE: suche ãJ bibel
searchCmd=r'(suche \w+ bibel|suche|bibel)'

# EXAMPLE: dem via
Thessalonians = r"(dem via|t[\w ']*chal[\w ]*w[\w ]*o[\w ]*a[\w ]*s|t\w*\s*\w*s|k\w*e\w*alonia\w*\s*\w*)\b"



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.


    # Das Buch 'levitikus' existiert nicht in der Übersetzung 'GerElb1905'.
    # EXAMPLE: levitikus
    ('Leviticus', r'\blevitikus\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: cx les
    ('Chronicles', r'\b(c\w*\s*les|Kodex\s*lese|bro\w*\s*läßt)\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),





    # ('Timothy', rf"(timotheus|tee[ \w]*io[ \w\-]*tee|t[ \w]+tes)\b", 90, {
    #     'flags': re.IGNORECASE,
    #     'skip_list': ['LanguageTool'],
    # }),


    # TODO: suche in II Timothy is buggy 9.11.'25
    #('suche in II Timothy', rf"(suche in zweiter) ([\w ]+ee|[\w ]+sy)\b", 90, {
    #    'flags': re.IGNORECASE,
    #    'skip_list': ['LanguageTool'],
    #}),







    # EXAMPLE: suche in 1
    ('suche in I Thessalonians', rf"suche in (1|erster) {Thessalonians}\b", 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: suche in 2
    ('suche in II Thessalonians', rf"suche in (2|zweiter) {Thessalonians}\b", 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: Suche ins
    ('suche in II', r'^Suche (ins|in) \wweiter\w*', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: suche in zweiter stext
    ('suche in II Samuel', r'suche in zweiter (s\w+|trafen)', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: erstex
    ('1', r'\b(erste\w*|ernster)\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: zweitex
    ('2', r'\bzweite\w*\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: Suche in Levx
    ('Suche in Leviticus', r'\bSuche in (Lev\w*\b|\w.*kurz\b|.*kuss)', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),




    # EXAMPLE: Vers
    ('Vers 1', r'\b(Vers|fährt) (ein|erwähnt|ab)$', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: fair sein
    ('Vers 1', r'\b(fair sein)$', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: VAR itext x text kapitel 123 Vers text 123
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: VAR itext x text kapitel 123 123 Vers text
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: VAR itext x text 123 kapitel 123 Vers text
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) kapitel (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    # EXAMPLE: VAR itext x text 123 Vers text 123
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Suche Ruth 123 123 Vers
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Suche Ruth 123 123 Vers
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),


    # now experimental more agressiv search (this maybe overwites other plugins) (S.11.11.'25 09:13 Tue)

    # EXAMPLE: Ruth kapitel 123 Vers 123
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Ruth text kapitel 123 123 Vers
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Ruth 123 kapitel 123 Vers
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) kapitel (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),




    # following is in conflict with rules like: was ist 5 plus 3 (s.,11.11.'25 13:35 Tue)
    # Das war ein bisschen schwierig zu finden

    #('bible suche', fr'^(i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
    #    'flags': re.IGNORECASE,
    #    'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    #}),


    # EXAMPLE: Ruth 123 123 Vers
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Was Ruth 1 1 Vers
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),



]















