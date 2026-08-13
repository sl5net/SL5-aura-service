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

# config/maps/wake-up/es-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


#

CONFIG_DIR = Path(__file__).parent

# aura = r'\s*\b(busch|computadora|aura|auri|voss|voß|vosk|volk|vor sk|first|frost|froscon|free esc| Frist|feuer)\b\s*'

# prácticamente quedarse dormido ¿Cómo es eso?

# haz que uno se duerma gratis ahora



# wakeword = r'{nonsense_word}(kaktus|kaktos|caca|kraft|recientemente|taktus|capitán|voss|frost|mesa plegable|práctico|canasta|como viaje).*'


# config/maps/wake-up/de-DE/FUZZY_MAP_pre.py:24

nonsense_start_word = r'(?:(a|uno|a)\s*)?'
wakeword = r'{nonsense_word}(telescopio|ocurre|tedesco|violoncelista|tenis|turístico|crédito).*'


# STT activo. Se eliminó la bandera de silencio. Lo que tiene, escupe


#

FUZZY_MAP_pre = [

    # buen día, enciende el cactus que despierta 🌵

    # Me despierto con un telescopio 🌵


    # EXAMPLE: palabra de despertar no escuches

    ('voss_start', fr'^({wakeword} escuchar no con|{wakeword}despierto en|{wakeword}en|{wakeword}despertar|{wakeword}guardia|{wakeword}evaluar|{wakeword}encender|{wakeword}activo|helada en bancarrota galleta|Antes chocar en|gratis cuadrado en|helada disparates en|bien día el despertar|{nonsense_start_word}telescopio semana fuera de|b\s*\w*\s*\cactus despertar)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # 1 golpear cabezales 2 enderezarlo 2 práctico

    # recientemente me quedé dormido

    # podías verte quedándote dormido

    #

    # EXAMPLE: quedarse dormido malas interpretaciones fonéticas 🌵

    ('voss_stop', fr'^(?:{wakeword}|gratis|cabezas|escuchó)\s*(?:golpear|dormirse|arrastrar hacia dentro|incluido\w*es|cerrado|Detener|templo|chao).*$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # uno 🌵

    # EXAMPLE: parada de palabra de activación

    ('voss_stop', fr'^(?:{wakeword}Detener\w*|{nonsense_start_word}{wakeword}{nonsense_start_word}templo\w*|{wakeword}ir templo\w*|bien noche|{wakeword}chao|{wakeword}nen)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # escuchaste a uno quedarse dormido

    # mi

    # EXAMPLE: nonsense_start_word te escuché quedarte dormido

    ('voss_stop', fr'^{nonsense_start_word}\s*(escuchó dormirse|ver podría dormirse)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),
    # 18:40:16,502 - INFORMACIÓN - 📢📢📢 ######################### set gratis ##########################################

    # stramg dije kakrus y se desentiende gratis...

    # EXAMPLE: cerrado gratis

    ('voss_stop', r'^(gratis) (cerrado|colocar)$', 89,
    {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),



]
#
# El jurado estaba despierto. El jurado estaba despierto.

# Despertar del juradoohComputerwocheDespertar del jurado

# PuñosFrost despiertoSTT Activo. Se eliminó la bandera de silencio.


