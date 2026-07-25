# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    # EXAMPLE: Zebra
    ('.Zebra.txt',r'^(Zebra|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     ),

    ('/home/seeh/Downloads/tesseract.log',r'^(Blumenkohl|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]
