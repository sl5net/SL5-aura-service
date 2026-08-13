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
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

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
# EXAMPLE: search itext x text chapter 123 vfdph text 123

('bible suche', r'^search (i\w+ )?(?P<book>\w*[ ]?\w+) chapter (?P<chapter>\d+) [vfdph]\w+ (?P<verses>\d+)$', 90, { ...

Suche in Ruth Kapitel 1 1 Vers
# EXAMPLE: search itext x text chapter 123 123 vfdph text

('bible suche', r'^search (i\w+ )?(?P<book>\w*\s*\w+) chapter (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {...

Suche in Ruth 1 Kapitel 1 Vers
# EXAMPLE: search itext x text 123 chapter 123 vfdph text

('bible suche', r'^search (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) chapter (?P<verses>\d+) [vfdph]\w+$', 90, {...

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


# EXAMPLE: search ãJ bible

searchCmd=r'(search \w+ Bible|search|Bible)'

# EXAMPLE: the via

Thessalonians = r"(dem via|t[\w ']*chal[\w ]*w[\w ]*o[\w ]*a[\w ]*s|t\w*\s*\w*s|k\w*e\w*alonia\w*\s*\w*)\b"



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.



    # The book 'Leviticus' does not exist in the translation 'GerElb1905'.

    # EXAMPLE: Leviticus

    ('Leviticus', r'\blevitikus\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: cx read

    ('Chronicles', r'\b(c\w*\s*read|Codex\s*read|bro\w*\s*lets)\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),





    # ('Timothy', rf"(timotheus|tee[ \w]*io[ \w\-]*tee|t[ \w]+tes)\b", 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['LanguageTool'],

    # }),



    # TODO: search in II Timothy is buggy 9.11.'25

    # ('search in II Timothy', rf"(search in second) ([\w ]+ee|[\w ]+sy)\b", 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['LanguageTool'],

    # }),








    # EXAMPLE: search in 1

    ('suche in I Thessalonians', rf"suche in (1|erster) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: search in 2

    ('suche in II Thessalonians', rf"suche in (2|zweiter) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: Search in

    ('suche in II', r'^Search (into the|in) \wcontin\w*', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: search in second stext

    ('suche in II Samuel', r'search in second (s\w+|met)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: firstex

    # ('1', r'\b(first\w*|more serious)\b', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['LanguageTool'],

    # }),

    # EXAMPLE: secondx

    ('2', r'\respectively\w*\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: Search in Levx

    ('Suche in Leviticus', r'\bSearch in (Lev\w*\b|\w.*short\b|.*kiss)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),




    # EXAMPLE: verse

    ('Vers 1', r'\b(verse|drives) (a|mentioned|away)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: be fair

    ('Vers 1', r'\b(fair be)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: VAR itext x text chapter 123 verse text 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) chapter (?P<chapter>\d+) [vfdph]\w+ (?P<verses>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: VAR itext x text chapter 123 123 verse text

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) chapter (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: VAR itext x text 123 chapter 123 verse text

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) chapter (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    # EXAMPLE: VAR itext x text 123 Verse text 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verses>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Search Ruth 123 123 verse

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Search Ruth 123 123 verse

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),


    # now experimental more aggressive search (this maybe overwrites other plugins) (S.11.11.'25 09:13 Tue)


    # EXAMPLE: Ruth chapter 123 verse 123

    ('bible suche', r'^(i\w+ )?(?P<book>\w*[ ]?\w+) chapter (?P<chapter>\d+) [vfdph]\w+ (?P<verses>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Ruth text chapter 123 123 verse

    ('bible suche', r'^(i\w+ )?(?P<book>\w*\s*\w+) chapter (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Ruth 123 chapter 123 verse

    ('bible suche', r'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) chapter (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),




    # following is in conflict with rules like: what is 5 plus 3 (see,11.11.'25 13:35 Tue)

    # This was a bit difficult to find


    # ('bible search', fr'^(i\w+ )?(?P<book>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'on_match_exec': [CONFIG_DIR / 'bible_search.py']

    # }),



    # EXAMPLE: Ruth 123 123 verse

    ('bible suche', r'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: What Ruth 1 1 verse

    ('bible suche', r'^(i\w+ )?(?P<book>\w*\s*\w+) (?P<chapter>\d+) (?P<verses>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),



]















