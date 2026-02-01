# de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

#

CONFIG_DIR = Path(__file__).parent

aura = r'\s*\b(busch|computer|aura|auri|voss|voß|vosk|volk|vor sk|first|frost|froscon|free esc|frist|feuer)\b\s*'

aura = r'.*(kaktus|kaktos|kackt|taktus|voss|frost|wie törn).*'

#STT Active. Mute flag removed.Was hat, spuckt

#

FUZZY_MAP_pre = [

    # guten tag das aufwachenkaktus einschalten
    # bin bi kaktus aufwachen

    ('voss_start', fr'^({aura} höre nicht mit|{aura}wach auf|{aura}auf|{aura}aufwachen|{aura}wache|{aura}einschätzen|{aura}einschalten|{aura}aktiv|frost brach kracher|Vor krach auf|free square auf|frost quatsch auf|guten tag das aufwachen|einen kaktus woche aus|b\s*\w*\s*\bkaktus aufwachen)$', 89,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    #



    ('voss_stop', fr'^({aura}stop\w*|{aura}schlafe\w*|{aura}geh schlafe\w*|gute nacht|{aura}ciao|{aura}nen)$', 89,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    ('voss_stop', fr'^(mithören|mithören stopppen|einschlafen|\w*\s*kannst du einschlafeneinen|guten tag das geh schlafen|bin jetzt dran hab das einschlafe\w*|bin klappt das einschlafen)$', 89,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),



]
#
#Jury war Jury wacheJury wacheinen
#Jury wach aufohComputerwocheJury wache
# FäusteFrost wachSTT Active. Mute flag removed.

