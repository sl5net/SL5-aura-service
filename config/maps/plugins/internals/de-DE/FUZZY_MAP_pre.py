# config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py

import re
from pathlib import Path


CONFIG_DIR = Path(__file__).parent

from scripts.py.func.determine_current_user import determine_current_user
current_user,_ = determine_current_user()

FUZZY_MAP_pre = [


    (f'{current_user}', r'^Aktueller user$'),

    (f'{current_user}', '^Benutzer$',),

    (f'{current_user}','^Aktueller Benutzer$'),
    (f'{current_user}','^aktuelle benutzt$'),
    (f'{current_user}','^Aktuelle Benutze$'),
    (f'{current_user}','^aktueller bill$'),


#  Helps the Tool to switch to English
    # EXAMPLE: englisch
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: s switch to english x s
    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Doppelpunkt
    (':', r'\bDoppelpunkt\b', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: kwink wir nieren
    ('quinquillieren', r'\b(kwink wir nieren|swing wie lire|klingt wie lire|kwink wir dir)\b', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: fragezeichen
    ('??', r'\s+(fragezeichen|fragen|fragend|frage|fragt)\s*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: ausrufezeichen
    ('!', r'\b(ausrufezeichen)\b', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Sondermüll
    ('Sondermüll!', r'\b(Sondermüll)\b', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Unterschied Aura
    ('Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commands', r'^(Unterschied\b.*\bAura\b|Auras? .*\badvantage\b).*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    ('SL5 Aura is a System-Wide, Offline Voice Automation and Command Framework. It instantly turns spoken words into commands, hotkeys, or text, with 100% privacy guarantee due to its offline operation. Its core is a powerful, scriptable RegEx Rule Engine that allows developers to create deeply customizable, multi-step workflows for professional and system-level automation.',
     # EXAMPLE: Whatx  Aura  
     r'^(What\w*\b.*\bAura\b).*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #

    # EXAMPLE: "Fehler melden", "Logge Fehler", "Das war falsch"
    ('report_error',
     r'^(fehler( melden|bericht|mail|meldung)?|logge fehler|das war falsch|da stimmt was nicht|bug melden|bugreport|ticket erstellen|problem melden|da ist ein fehler|das ist falsch|das ist ein bug)$',
     100,
     {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

]

if current_user in ['seeh']:
    FUZZY_MAP_pre_user_specific = [
        ('report_error',
         r'^(fehler( melden|bericht|mail|meldung)?|logge fehler|das war falsch|da stimmt was nicht|bug melden|bugreport|ticket erstellen|problem melden|da ist ein fehler|das ist falsch|das ist ein bug)$',
         100,
         {
             'flags': re.IGNORECASE,
             'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
         })
    ]

    FUZZY_MAP_pre.extend( FUZZY_MAP_pre_user_specific )



