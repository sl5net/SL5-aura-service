# projects/py/STT/config/maps/plugins/1_collect_unmatched_training/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
import platform
CONFIG_DIR = Path(__file__).parent
# too<-from

starten = r'starten|stab|start|staat|starb|straffen|spart|stab|starb|stadt|starb'
Lernmodus= r'(Lernmodus|Training)'

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
FUZZY_MAP_pre = [


    # 1. Notiere deine Optimierungs-Regel hier zuerst! (Ergebnis zuerst!)


    (f'kate {str(__file__)}', rf'^(lernmodus|Lernmodus\s*{starten}|led modus\s*{starten}|led modus\s*{starten}|Training {starten}|Erkennungstraining|lärm wurdest stab|ihren modus {starten}|der modus|der modus {starten}|Grip Modus {starten}|trainingsstart|reading {starten}|heiligen staat|erkundungstour reading|bildungsprämie|sag rettungs training|quidditch training|führungstraining|gründungstreffen erkältungstee training|gründungs|bildungsträger|jörg velux training|der grillo training|gründungs training|erkältungstee ideen|der glättung streaming|erkältung training|erkältungstee ding|erkennung training|erkältungstee training|erkennung nicht|lab modus {starten}|leere modus {starten}|lernmodus starb|der modus stunden|für genuss training|lernmodus stab|der modus spart|home modus stab|renault modus {starten}|hallo xd reinigen|verkehr lostreten|danke lux training|lernmodul {starten}|werden modus {starten}|für quintus training|genuss trinken verkehr lostreten lernmodus starb|erkennung strähnig|leeren modus {starten}|lärm wurdest stab|er wurde {starten}|werden würdest|der bundesstaat|\w+\s*wurde {starten}|lernmodell {starten})$'),


    #################################################
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    #('Aura einschalten',r'^(Aura einschalten|oh ein einschalten|hurra einschalten|aura einschwenken|rohre eins 12|rohre einschalten|hurra einschl|uva einschalten|hurra ein schmied|hurra entscheiden|eure einschalten|horror in schweden|zora einschalten|aura entfalten|einschalten|aber einschalten|hurra einschränken|aura einschmelzen|cobra einschalten horror eintreffen hurra einschalten aura einschalten|hurra ritschel)$', 100,{'flags': re.IGNORECASE,}),




    #('Teleskop',r'^(Teleskop|tritt|tedesco|cellist|tennis|tourist|kredit|Program loaded|wurde es still|der modeste|der bundesstaaten werden würde stören|lernen modisch|ir modus starten|brutto|hilfe virus)$', 100,{'flags': re.IGNORECASE}),



    #('Torpedo',r'^(Torpedo|trapez|schritt edel|präzise|trotz siedeln|druck peru|shop credo|trotzdem|krepieren)$', 100,{'flags': re.IGNORECASE}),

    # ('Nexus',r'^(Nexus|wirkt|dick)$', 100,{'flags': re.IGNORECASE}),


    # ('Kosmonaut',r'^(Kosmonaut|kurs wurden|großmutter|cosmo deutsch|busbud|kosmologie|gruss pilot|was wohl world|gus gus benutzen groß wurde|kosmodrom|brust nur laut|chris bedroht|grüßle|chris müller|fristlose mut|grüßt mir lot|grußwort hut|grußwort an|gruß pilot|es wurden)$', 100,{'flags': re.IGNORECASE}),

    # ('Roboter',r'^(Roboter|wo bitte|oh britta|oh bitte)$', 100,{'flags': re.IGNORECASE}),


    #('Oktopus',r'^(Oktopus|du)$', 100,{'flags': re.IGNORECASE}),

    # ('teleskop',r'^(teleskop|gott|script ist|kryptos|durch|einen kaputten teleskop|chris|mein gott|crypto|grip|skripte|es|script)$', 100,{'flags': re.IGNORECASE,}),



]


