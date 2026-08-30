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


    # EXAMPLE: Usuario actual

    (f'{current_user}', r'^Más actual usuario.usuario$'),

    (f'{current_user}', '^Benutzer$',),

    (f'{current_user}','^Aktueller Benutzer$'),
    (f'{current_user}','^aktuelle benutzt$'),
    (f'{current_user}','^Aktuelle Benutze$'),
    (f'{current_user}','^aktueller bill$'),


# Ayuda a la herramienta a cambiar al inglés.

    # EXAMPLE: Inglés

    ('english please', r'^\s*(Inglés|inglés) (lana|por favor)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: s cambiar al inglés x s

    ('english please', r'^\s*(cambiar a inglés\s*\w*)\s*$', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: colon

    (':', r'\bcolon\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: retorcimos los riñones

    ('quinquillieren', r'\b(kinky nosotros riñones|balancearse Cómo liras|sonidos Cómo liras|kinky nosotros tú)\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: signo de interrogación

    ('??', r'\s+(signo de interrogación|preguntas|interrogativamente|preguntar|pregunta)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: signo de admiración

    ('!', r'\b(signo de admiración)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Desechos peligrosos

    ('Sondermüll!', r'\b(Desechos peligrosos)\b', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Aura de diferencia

    ('Auras key advantage is its Hierarchical and Recursive Rule Engine (RegEx). This architecture allows developers to create live-adaptable, modular, and highly maintainable plugins for complex, professional-grade tasks that go beyond simple commands', r'^(Diferencia\b.*\baura\b|Auras? .*\mala ventaja\b).*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    ('SL5 Aura is a System-Wide, Offline Voice Automation and Command Framework. It instantly turns spoken words into commands, hotkeys, or text, with 100% privacy guarantee due to its offline operation. Its core is a powerful, scriptable RegEx Rule Engine that allows developers to create deeply customizable, multi-step workflows for professional and system-level automation.',
     # EXAMPLE: Qué aura

     r'^(Qué\w*\b.*\baura\b).*$', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #
    # Informe de prevención de conflictos de Eva Bonito informe Informe especial de la corte de Eva


    # EXAMPLE: "Informe de error", "Error de registro", "Eso estuvo mal"

    ('report_error',
     r'^(error( informe|informe|correo electrónico|informe)?|registro error|ola de frio|el era incorrecto|allá verdadero Qué no|bicho informe|informe de error|informe de viaje|fuente informe de error|paseo libre informe|fred informe|celebrar|boleto crear|problema informe|allá es a error|error por favor|aquí el informe|el informe|error en el informe|el es incorrecto|muchos conocimiento|el es a bicho)$', 100,
     # min_accuracycelebrateReportErrors pleaseinternals>misrecognitionsReportinternals>misrecognitionss


     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

    # EXAMPLE: Titular propio de FVW

    ('report_error',
     r'\b(?:(?:[FVW][eh]h?l[él]{1,2}|votantes|talador|cuatro|pueblos|Phäler)\s?(?:ser?bien|se rompe|luz|bien))\b', 100,
     {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
     }),

]

# Efecto rápido Hola informes.


if current_user in ['seeh']:
    FUZZY_MAP_pre_user_specific = [


        # Regla B: Obstáculo bajo (10%)

        # EXAMPLE: Súper frágil

        ("Niedrige Genauigkeit erkannt", r'^(Súper frágil|Adiós frágil)$', 10,
         {
             'command_flags': re.IGNORECASE,
         }
         ),

        # Súper frágil súper súper mujer da Hola frágil encuesta Kübra frágil


        # EXAMPLE: informar errores

        ('report_error',
         r'^(error( informe|informe|correo electrónico|informe)?|registro error|el era incorrecto|allá verdadero Qué no|bicho informe|informe de error|boleto crear|problema informe|allá es a error|el es incorrecto|el es a bicho)$', 100,
         # precisión_min


         {
             'command_flags': re.IGNORECASE,
             'on_match_exec': [CONFIG_DIR / '..' / 'report_error.py']
         })
    ]

    FUZZY_MAP_pre.extend( FUZZY_MAP_pre_user_specific )



