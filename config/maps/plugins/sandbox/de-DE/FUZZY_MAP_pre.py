# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
# too<-from
FUZZY_MAP_pre = [
    # EXAMPLE: Blumenkohl
    ('.test.txt',r'^(Blumenkohl|5)$', 85,
     {'command_flags': re.IGNORECASE, }
     )
]
