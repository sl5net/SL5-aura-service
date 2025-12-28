# config/maps/plugins/internals/en-US/FUZZY_MAP_pre.py
# config/languagetool_server/maps/de-DE/FUZZY_MAP.py
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
    # - it stops with first full-match (^ ... $)!
    # - means first is most importend, lower rules maybe not get read.

    # Deutsche p Nun sprechen wir durch

    #  Helps the Tool to switch to German
    # {'flags': {'flags': re.IGNORECASE}, 'skip_list': ['filter1', 'filter4']}
    # EXAMPLE: s deutsche pizza
    ('Deutsch bitte', r'^\s*(deutsche) (pizza|pigeons|putin|bit|p)\s*$', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: lobtCase
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),


    # EXAMPLE: lobtCase
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),


    # EXAMPLE: Manjaro
    ('Manjaro', r'\b(Manjaro|much whole|munchau|mon travel|Manchu|Much\s*whole)\b', 82, {'flags': re.IGNORECASE}),
# Much whole Mon travel
# One troll Michelle


#    ('.', r'^\s*(punkt|pup)\s*$', 82, {'flags': re.IGNORECASE}),


#    ('zwei', r'ein|eins', 60, {'flags': re.IGNORECASE}),
#    ('drei', r'zwei', 60, {'flags': re.IGNORECASE}),


    # EXAMPLE: Unterschied Aura
    ('Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commands', r'^(Unterschied\b.*\bAura\b|Auras? .*\badvantage\b).*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    ('SL5 Aura is a System-Wide, Offline Voice Automation and Command Framework. It instantly turns spoken words into commands, hotkeys, or text, with 100% privacy guarantee due to its offline operation. Its core is a powerful, scriptable RegEx Rule Engine that allows developers to create deeply customizable, multi-step workflows for professional and system-level automation.',
     # EXAMPLE: Whats Aura
     r'^(What\w*\b.*\bAura\b).*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #What is aura What is aura


    # EXAMPLE:  Aura Strength  
    ('SL5 Aura (Strength): Recursive, Hierarchical Rule Engine with Live Parsing and RegEx. Inheritance and Sub-folders (e.g., game/0ad, it-begriffe/php/codeigniter) enable modular, maintainable plugins.100% GDPR-Compliance and Developer-Friendly Design for complex, long-term projects. Conclusion: Aura is the Architect Solution for privacy-compliant, specialized, and scalable voice control.', r'^(.*\bAura.*\bStrength\b).*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #




]
