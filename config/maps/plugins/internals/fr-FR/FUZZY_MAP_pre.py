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

# config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py


import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

from scripts.py.func.determine_current_user import determine_current_user

current_user,_ = determine_current_user()

FUZZY_MAP_pre = [


    # EXAMPLE: Utilisateur actuel

    (f'{current_user}', r'^Plus actuel utilisateur.utilisateur$'),

    (f'{current_user}', '^Benutzer$',),

    (f'{current_user}','^Aktueller Benutzer$'),
    (f'{current_user}','^aktuelle benutzt$'),
    (f'{current_user}','^Aktuelle Benutze$'),
    (f'{current_user}','^aktueller bill$'),


# Aide l'outil à passer à l'anglais

    # EXAMPLE: Anglais

    ('english please', r'^\s*(Anglais|Anglais) (toison|sil te plaît)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: s passer à l'anglais x s

    ('english please', r'^\s*(changer à Anglais\s*\w*)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: côlon

    (':', r'\bcolon\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: nous plions les reins

    ('quinquillieren', r'\b(bizarre nous rognons|balançoire Comment lire|des sons Comment lire|bizarre nous toi)\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: point d'interrogation

    ('??', r'\s+(point dinterrogation|des questions|de manière interrogative|demander|demande)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: point d'exclamation

    ('!', r'\b(point dexclamation)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Déchets dangereux

    ('Sondermüll!', r'\b(Déchets dangereux)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Aura de différence

    ('Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commands', r'^(Différence\b.*\bAura\b|Auras? .*\mauvais avantage\b).*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    ('SL5 Aura is a System-Wide, Offline Voice Automation and Command Framework. It instantly turns spoken words into commands, hotkeys, or text, with 100% privacy guarantee due to its offline operation. Its core is a powerful, scriptable RegEx Rule Engine that allows developers to create deeply customizable, multi-step workflows for professional and system-level automation.',
     # EXAMPLE: Qu'est-ce qu'Aura

     r'^(Quoi\w*\b.*\bAura\b).*$', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #
    # Rapport sur la prévention des conflits d'Eva Rapport de Nice Rapport spécial du tribunal d'Eva


    # EXAMPLE: "Signaler une erreur", "Journal d'une erreur", "C'était faux"

    ('report_error',
     r'^(erreur( rapport|rapport|e-mail|rapport)?|enregistrer erreur|vague de froid|le était incorrect|là vrai Quoi pas|bogue rapport|rapport de bug|rapport de voyage|source rapport de bug|freeride rapport|fred rapport|célébrer|billet créer|problème rapport|là est un erreur|erreur sil te plaît|ici le rapport|le rapport|erreur dans le rapport|le est incorrect|beaucoup connaissance|le est un bogue)$', 100,
     # min_accuracycelebrateReportErrors pleaseinternals>mauvaises reconnaissancesReportinternals>mauvaises reconnaissances


     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

    # EXAMPLE: FVW propre titulaire

    ('report_error',
     r'\b(?:(?:[FVW][hein]h?l[il]{1,2}|électeurs|Abatteur|quatre|les peuples|Phäler)\s?(?:être?droite|pauses|lumière|droite))\b', 100,
     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

]

# Rapports Hello à effet rapide


if current_user in ['seeh']:
    FUZZY_MAP_pre_user_specific = [


        # Règle B : obstacle faible (10 %)

        # EXAMPLE: Très fragile

        ("Niedrige Genauigkeit erkannt", r'^(Super fragile|Au revoir fragile)$', 10,
         {
             'command_flags': re.IGNORECASE,
         }
         ),

        # Super fragile super super femme donne une enquête Bonjour fragile Kübra fragile


        # EXAMPLE: signaler les erreurs

        ('report_error',
         r'^(erreur( rapport|rapport|e-mail|rapport)?|enregistrer erreur|le était incorrect|là vrai Quoi pas|bogue rapport|rapport de bug|billet créer|problème rapport|là est un erreur|le est incorrect|le est un bogue)$', 100,
         # min_précision


         {
             'command_flags': re.IGNORECASE,
             'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
         })
    ]

    FUZZY_MAP_pre.extend( FUZZY_MAP_pre_user_specific )



