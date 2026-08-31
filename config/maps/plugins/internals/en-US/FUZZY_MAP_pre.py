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


    # EXAMPLE: Current user

    (f'{current_user}', r'^More current user.user$'),

    (f'{current_user}', '^Benutzer$',),

    (f'{current_user}','^Aktueller Benutzer$'),
    (f'{current_user}','^aktuelle benutzt$'),
    (f'{current_user}','^Aktuelle Benutze$'),
    (f'{current_user}','^aktueller bill$'),


# Helps the Tool to switch to English

    # EXAMPLE: English

    ('english please', r'^\s*(English|english) (fleece|please)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: s switch to english x s

    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: colon

    (':', r'\bcolon\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: we kink kidneys

    ('quinquillieren', r'\b(kwink we kidneys|swing How lire|sounds How lire|kwink we you)\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: question mark

    ('??', r'\s+(question mark|questions|questioningly|ask|asks)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: exclamation mark

    ('!', r'\b(exclamation mark)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Hazardous waste

    ('Sondermüll!', r'\b(Hazardous waste)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Difference aura

    ('Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commands', r'^(Difference\b.*\baura\b|Auras? .*\badvantage\b).*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    ('SL5 Aura is a System-Wide, Offline Voice Automation and Command Framework. It instantly turns spoken words into commands, hotkeys, or text, with 100% privacy guarantee due to its offline operation. Its core is a powerful, scriptable RegEx Rule Engine that allows developers to create deeply customizable, multi-step workflows for professional and system-level automation.',
     # EXAMPLE: Whatx Aura

     r'^(What\w*\b.*\baura\b).*$', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #
    # Eva conflict prevention report Nice report Eva court special report


    # EXAMPLE: "Report Error", "Log Error", "That was wrong"

    ('report_error',
     r'^(mistake( report|report|email|report)?|log mistake|cold wave|the was incorrect|there true What not|bug report|bug report|travel report|source bug report|freeride report|fred report|celebrate|ticket create|problem report|there is a mistake|mistake please|here the report|the report|mistake in the report|the is incorrect|many knowledge|the is a bug)$', 100,
     # min_accuracycelebrateReportErrors pleaseinternals>misrecognitionsReportinternals>misrecognitionss


     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

    # EXAMPLE: FVW own holder

    ('report_error',
     r'\b(?:(?:[FVW][eh]h?l[he]{1,2}|voters|Feller|four|peoples|Phäler)\s?(?:be?right|breaks|light|right))\b', 100,
     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

]

# Quick effect Hello reports


if current_user in ['seeh']:
    FUZZY_MAP_pre_user_specific = [


        # Rule B: Low hurdle (10%)

        # EXAMPLE: Super fragile

        ("Niedrige Genauigkeit erkannt", r'^(Super fragile|Good bye fragile)$', 10,
         {
             'command_flags': re.IGNORECASE,
         }
         ),

        # Super fragile super super woman give Hello fragile survey Kübra fragile


        # EXAMPLE: report errors

        ('report_error',
         r'^(mistake( report|report|email|report)?|log mistake|the was incorrect|there true What not|bug report|bug report|ticket create|problem report|there is a mistake|the is incorrect|the is a bug)$', 100,
         # min_accuracy


         {
             'command_flags': re.IGNORECASE,
             'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
         })
    ]

    FUZZY_MAP_pre.extend( FUZZY_MAP_pre_user_specific )



