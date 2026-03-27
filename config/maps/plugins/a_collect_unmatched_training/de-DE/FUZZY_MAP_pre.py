# projects/py/STT/config/maps/plugins/a_collect_unmatched_training/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
# too<-from
FUZZY_MAP_pre = [
    # 1. Deine Optimierungs-Regel (Ergebnis zuerst!)
    #
    ('Aura einschalten',
     r'^(Aura einschalten|oh ein einschalten|hurra einschalten|aura einschwenken|rohre eins 12|rohre einschalten|hurra einschl|uva einschalten|hurra ein schmied|hurra entscheiden|eure einschalten|horror in schweden|zora einschalten|aura entfalten|einschalten|aber einschalten|hurra einschränken|aura einschmelzen|cobra einschalten horror eintreffen hurra einschalten aura einschalten|hurra ritschel)$', 100,
     {
         'flags': re.IGNORECASE,
     }
    ),


    ('COLLECT_UNMATCHED',
    r'^OFF5 (.*) 5OFF$', 10,
        {
            'on_match_exec': [CONFIG_DIR / '..' / 'collect_unmatched.py'],
        }
    ),
]
#Blumen orchestrieren
