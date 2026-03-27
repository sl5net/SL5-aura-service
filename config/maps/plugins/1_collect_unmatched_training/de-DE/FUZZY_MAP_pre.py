# projects/py/STT/config/maps/plugins/1_collect_unmatched_training/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
# too<-from
FUZZY_MAP_pre = [
    # 1. Notiere deine Optimierungs-Regel hier zuerst! (Ergebnis zuerst!)
    #





    # 2. aktiviere diese Regel
    # ('COLLECT_UNMATCHED', r'^(.*)$', 10,{'on_match_exec':[CONFIG_DIR / '..' / 'collect_unmatched.py'],}),

    #('Aura einschalten',r'^(Aura einschalten|oh ein einschalten|hurra einschalten|aura einschwenken|rohre eins 12|rohre einschalten|hurra einschl|uva einschalten|hurra ein schmied|hurra entscheiden|eure einschalten|horror in schweden|zora einschalten|aura entfalten|einschalten|aber einschalten|hurra einschränken|aura einschmelzen|cobra einschalten horror eintreffen hurra einschalten aura einschalten|hurra ritschel)$', 100,{'flags': re.IGNORECASE,}),


    (f'kate {str(__file__)}', r'^(Lernmodus starten|Training starten|Erkennungstraining|ihren modus starten|der modus starten|trainingsstart|reading starten|heiligen staat|erkundungstour reading|bildungsprämie|sag rettungs training|quidditch training|führungstraining|gründungstreffen erkältungstee training|gründungs|bildungsträger|jörg velux training|der grillo training|gründungs training|erkältungstee ideen|der glättung streaming|erkältung training|erkältungstee ding|erkennung training|erkältungstee training|erkennung nicht|lab modus starten|leere modus starten|lernmodus starb|der modus stunden|für genuss training|lernmodus stab|der modus spart|home modus stab|renault modus starten|hallo xd reinigen|verkehr lostreten|danke lux training|lernmodul starten|werden modus starten|für quintus training|genuss trinken verkehr lostreten lernmodus starb|erkennung strähnig)$'),




]

#Der Modus starten

