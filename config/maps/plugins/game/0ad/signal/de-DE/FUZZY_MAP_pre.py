# config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py:1
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702
# https://regex101.com/
zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']
_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
}
FUZZY_MAP_pre = [
    # config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py:19
    # EXAMPLE: alarm
    ('ö', r'^(alarm|anhand|na|an|anlass|alle|anna|la|hallo|alarm senden|alarm auslöst|alarm auslösen|alarm senden alarm auslösen alarm auslösen anhang|alarmglocke läuten|alarmglocken|druck lloyd|arme glocke läuten alarmglocken glockenläuten|glockenläuten|glocke läuten|glocken läuten die glocke läuten alle ins|ali|alarm vorbei|anhaben verbreiten|bedrohung beendet)$',
     85,_common_meta),
]
