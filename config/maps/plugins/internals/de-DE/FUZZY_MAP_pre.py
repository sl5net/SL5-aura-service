# config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py

import re
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - means first is most important, lower rules maybe not get read.

    # Kannst du nicht ein

    # TEST: Vertauschte Regel (Regex vorn, ID hinten)
    (r'test_id', '^(test fehler|chaos monkey)$', 100, {}),
    ('test_id','^(test fehler|chaos monkey)$',  100, {}),

    # TEST 1: Vertauschte einfache Regel
    (r'toggle_light', '^(taschenlampe an|licht an)$', 95, {}),

    # TEST 2: Vertauschter Mehrzeiler (wie dein report_error)
    (r'check_system_health',
     '^(system status|wie geht es dir|alles okay)$',
     100,
     {
         'flags': re.IGNORECASE
     }),



    # EXAMPLE: "Fehler melden", "Logge Fehler", "Das war falsch"
    ('report_error',r'^(fehler melden|logge fehler|das war falsch|fehler mail|fehlermeldung)$', 100,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
    }),

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
]
#!Sünde muss Santa bSondermüll!Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commandshörig antwortetSowas Advantage


