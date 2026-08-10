# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401


from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [


    ('',
     # EXAMPLE: Clipboard
     r'^(Clipboard|Zwischenablage|Zeile\w*|Text neu) (nummeriere\w*|suggerieren|dumme geritten|operieren|nummerieren|nummerieren)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),
    ('',
     # EXAMPLE: nummerierex
     r'^(nummeriere\w*|suggerieren|dumme geritten|operieren|nummerieren|nummerieren)\b\s*(?:!die)?(Clipboard|Zwischenablage|Zeile\w*|Text neu)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / '..' /  'renumber_clipboard_text.py']
     }),

    # EXAMPLE: Zeilex nummerierex
    ('', r'^(Zeile\w* nummeriere\w*|Zeilen suggerieren|Zeile dumme geritten|zeile\w* operieren|Text neu nummerieren|Zwischenablage nummerieren|Laufende Zeilennummern einfügen|Zeilennummern aktualisieren|teile reparieren|keine nummerieren|Zeilesuggerieren)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' / 'renumber_clipboard_text.py']
    }),


]

