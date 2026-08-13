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

# config/maps/wake-up/de-DE/FUZZY_MAP_pre.py

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


#

CONFIG_DIR = Path(__file__).parent

# aura = r'\s*\b(busch|computer|aura|auri|voss|voß|vosk|volk|vor sk|first|frost|froscon|free esc| Frist|feuer)\b\s*'

# practically falling asleepHow is that?

# have one fall asleep for free now



# wakeword = r'{nonsense_word}(kaktus|kaktos|pooped|kraft|recently|taktus|captain|voss|frost|folding table|practical|basket|like trip).*'


# config/maps/wake-up/de-DE/FUZZY_MAP_pre.py:24

nonsense_start_word = r'(?:(a|one|a)\s*)?'
wakeword = r'{nonsense_word}(telescope|occurs|tedesco|cellist|tennis|tourist|credit).*'


# STT Active. Mute flag removed.What has, spits


#

FUZZY_MAP_pre = [

    # good day, turn on the waking cactus 🌵

    # I wake up with a telescope 🌵


    # EXAMPLE: wakeword don't listen

    ('voss_start', fr'^({wakeword} listen not with|{wakeword}awake on|{wakeword}on|{wakeword}wake up|{wakeword}guard|{wakeword}assess|{wakeword}turn on|{wakeword}active|frost broke cracker|Before crash on|free square on|frost nonsense on|good day the wake up|{nonsense_start_word}telescope week out of|b\s*\w*\s*\bcactus wake up)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # 1 knock heads 2 straighten it 2 practical

    # recently fell asleep

    # you could see yourself falling asleep

    #

    # EXAMPLE: fall asleep phonetic misinterpretations 🌵

    ('voss_stop', fr'^(?:{wakeword}|free|heads|heard)\s*(?:hit|fall asleep|drag in|including\w*en|closed|Stop|temple|ciao).*$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # one 🌵

    # EXAMPLE: wakeword stop

    ('voss_stop', fr'^(?:{wakeword}Stop\w*|{nonsense_start_word}{wakeword}{nonsense_start_word}temple\w*|{wakeword}go temple\w*|good night|{wakeword}ciao|{wakeword}nen)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # you heard one fall asleep

    # e

    # EXAMPLE: nonsense_start_word heard you fall asleep

    ('voss_stop', fr'^{nonsense_start_word}\s*(heard fall asleep|see could fall asleep)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),
    # 18:40:16,502 - INFO - 📢📢📢 ######################### set for free ##########################################

    # stramg i said kakrus and it unsestands gratis...

    # EXAMPLE: closed for free

    ('voss_stop', r'^(free) (closed|set)$', 89,
    {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),



]
#
# Jury was jury awakejury awake

# Jury wake upohComputerwocheJury wake up

# FistsFrost awakeSTT Active. Mute flag removed.


