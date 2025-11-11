# /home/seeh/projects/py/STT/config/maps/plugins/bible_search/FUZZY_MAP_pr.py
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
('bible suche', r'^suche (i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, { ...

Suche in Ruth Kapitel 1 1 Vers
('bible suche', r'^suche (i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {...

Suche in Ruth 1 Kapitel 1 Vers
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

searchCmd=r'(suche|bibel|suche \w+ bibel)'

Thessalonians = r"(dem via|t[\w ']*chal[\w ]*w[\w ]*o[\w ]*a[\w ]*s|t\w*\s*\w*s|k\w*e\w*alonia\w*\s*\w*)\b"



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    # Das Buch 'levitikus' existiert nicht in der Übersetzung 'GerElb1905'.
    ('Leviticus', r'\blevitikus\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

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







    ('suche in I Thessalonians', rf"suche in (1|erster) {Thessalonians}\b", 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    ('suche in II Thessalonians', rf"suche in (2|zweiter) {Thessalonians}\b", 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    ('suche in II', r'^Suche (ins|in) \wweiter\w*', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    ('suche in II Samuel', r'suche in zweiter (s\w+|trafen)', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    ('1', r'\b(erste\w*|ernster)\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    ('2', r'\bzweite\w*\b', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    ('Suche in Leviticus', r'\bSuche in (Lev\w*\b|\w.*kurz\b|.*kuss)', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),




    ('Vers 1', r'\b(Vers|fährt) (ein|erwähnt|ab)$', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    ('Vers 1', r'\b(fair sein)$', 90, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) kapitel (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),


    # now experimental more agressiv search (this maybe overwites other plugins) (S.11.11.'25 09:13 Tue)

    ('bible suche', fr'^(i\w+ )?(?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) kapitel (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) kapitel (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    ('bible suche', fr'^(i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    ('bible suche', fr'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verse>\d+) [vfdph]\w+$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),



]















