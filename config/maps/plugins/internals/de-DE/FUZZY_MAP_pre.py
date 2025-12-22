# config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py
# config/languagetool_server/maps/de-DE/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.


    #  Helps the Tool to switch to English
    # EXAMPLE: s englisch
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: s switch to english s x s
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


