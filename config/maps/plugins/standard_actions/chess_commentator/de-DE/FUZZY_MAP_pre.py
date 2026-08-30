# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py
import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [

    # --- Rule for the Chess Commentator ---
    # This rule listens for various forms of negative self-talk during a game.
    # EXAMPLE: fehler
    ( 'schach_kommentator_negativ', r'^\b(fehler|mist|So ein Mist|verdammt|scheiße|blöd|dumm|idiot|nicht aufgepasst|ärgerlich|ach komm|das wars|verloren|ich geb\w? auf)\b$', 90, { 'flags': re.IGNORECASE, 'on_match_exec': [CONFIG_DIR / '..' / 'chess_commentator.py'] }),

]

