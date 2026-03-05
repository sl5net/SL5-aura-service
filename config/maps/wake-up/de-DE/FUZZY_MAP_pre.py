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

# aura = r'\s*\b(busch|computer|aura|auri|voss|voß|vosk|volk|vor sk|first|frost|froscon|free esc|frist|feuer)\b\s*'
#praktisch einschlafenWie ist das bitte
# einenhaben gratis einschlafennun

nonsense_start_word = r'(?:(ein|eine|einen)\s*)?'

kaktus = r'{nonsense_word}(kaktus|kaktos|kackt|kraft|kürzlich|taktus|captain|voss|frost|klapptisch|praktisch|korb|wie törn).*'

#STT Active. Mute flag removed.Was hat, spuckt

#

FUZZY_MAP_pre = [

    # guten tag das aufwachenkaktus einschalten 🌵
    # bin bi kaktus aufwachen 🌵

    ('voss_start', fr'^({kaktus} höre nicht mit|{kaktus}wach auf|{kaktus}auf|{kaktus}aufwachen|{kaktus}wache|{kaktus}einschätzen|{kaktus}einschalten|{kaktus}aktiv|frost brach kracher|Vor krach auf|free square auf|frost quatsch auf|guten tag das aufwachen|{nonsense_start_word}kaktus woche aus|b\s*\w*\s*\bkaktus aufwachen)$', 89,
     {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # 1 köpfe einschlagen 2 Es richten 2 praktisch
    # kürzlich einschlafen
    # sehen könntest einschlafen
    #

    # EXAMPLE: einschalfen phonetic misinterpretations 🌵
    ('voss_stop', fr'^(?:{kaktus}|gratis|köpfe|hörtest)\s*(?:einschlagen|einschlafen|einschleppen|einsch\w*en|geschlossen|stop|schlafe|ciao).*$', 89,
     {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # einen 🌵
    ('voss_stop', fr'^(?:{kaktus}stop\w*|{nonsense_start_word}{kaktus}{nonsense_start_word}schlafe\w*|{kaktus}geh schlafe\w*|gute nacht|{kaktus}ciao|{kaktus}nen)$', 89,
     {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # einen hörtest einschlafen
    #e
    ('voss_stop', fr'^{nonsense_start_word}\s*(hörtest einschlafen|sehen könntest einschlafen)$', 89,
     {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),
    # 18:40:16,502 - INFO     - 📢📢📢 ######################### gratis einstellen ##########################################
    # stramg i said kakrus and it unsestands gratis ...
    ('voss_stop', r'^(gratis) (geschlossen|einstellen)$', 89,
    {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),



]
#
#Jury war Jury wacheJury wacheinen
#Jury wach aufohComputerwocheJury wache
# FäusteFrost wachSTT Active. Mute flag removed.

