# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    # ('ert', r'^(ert|wie ist das wetter|git status |stopp|was ist 5 plus 3|Sekunde lauf war|für|überall|5 ,|circa|12|7|22|9|größer|schön|respektive|bitte schön|die antwort ist ein test|bitte reservieren sie einen tisch für 2 personen um 8 uhr|von sebastian laufer|1000 euro. Und euro großgeschrieben.|im sommer ist es warm|lieblingszahlen sind 5 und 3|heute ist montag|danke schön|sebastian mit nachnamen laufer|ich weiß nicht|bis später|entschuldigung|auf wiedersehen|ich verstehe|weiß|alles klar|füße|kein problem|müde|zum beispiel|und so weiter|hände|was machst du heute|zum schluss|was für ein tag|wo finde ich toilette|wie spät ist es|der kleine hund spielt mit seinem neuen spielzeug|die sonne scheint auf die blumen|das ist unglaublich|gehe nach links|öffne die tür|obwohl es regnet ist die stimmung gut|schalte das licht ein|Programm geladen. Viel Spaß|git commit |789|git add .|der hund bellt|mit nachnamen laufer|heute ist ein schöner tag|heute ist ein schöner tag 23|ein haus und ein garten|Sebastian mit nachnamen|über die konsole zu bedienen|straße|doktor|hilfe|wiederhole das bitte|das wetter wird morgen sonnig mit temperaturen um die 20 grad|irgendwasneuesneues4)$'),
    #('jetzt funktioniert hab ich etwas vergessen2', '^(jetzt\\ funktioniert\\ hab\\ ich\\ etwas\\ vergessen|jetzt funktioniert habe ich etwas vergessen)$'),
    # (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
