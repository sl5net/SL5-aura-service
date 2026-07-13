# config/maps/plugins/sikulix/en-US/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent
sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli', 'oculixide', 'OculiX']


FUZZY_MAP_pre = [

    # EXAMPLE: double click
    # Native: double click | German-Vosk: dabble, bubble, doppel
    ('doubleClick("image.png")', r'^\s*(double|dub|dabble|bubble|doppel|durable|dublin|dopple)\s*(click|klick|quick)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    #################################################
    # 2. activate this rule (behind the first rule you want to optimize)

    #################################################

    # EXAMPLE: right click
    # Native: right click | German-Vosk: write, white, light, rate, ride
    ('rightClick("image.png")', r'^\s*(right|write|white|light|rate|ride|reit)\s*(click|klick)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: click
    # Native: click | German-Vosk: clark, clerk, clock, cluck, glick
    ('click("image.png")', r'^\s*(click|klick|glick|clark|clerk|clock|cluck|quick|clip|clit|clique|clicked|clicks)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: wait vanish
    ('waitVanish("image.png", 10)', r'^\s*(wait|weight|white|fate)\s*(vanish|till\s*gone|until\s*gone|disappear|for\s*vanish)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: wait
    # Native: wait, waits | German-Vosk: weight, white, fate, eight, wet, wade
    ('wait("image.png", 10)', r'^\s*(wait|weight|white|fate|eight|wet|wade|what|waits|waited|woke|wate|Await Image|Wait Pattern|Watch Screen|Expect Icon|Wait Region|Scan Image|Image Wait|Watch Region|Pixel Watch|Visual Wait|Screen Watch|Icon Await|Pattern Wait|Region Scan|Element Wait)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: find all
    ('for m in findAll("image.png"):', r'^\s*((find|fine|font|fined|locate)\s*(all|every|each))\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: find
    # Native: find, search | German-Vosk: fine, fined, font, found
    ('find("image.png")', r'^\s*(find|finds|fine|fined|font|found|locate|search)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: exists
    # Native: exists | German-Vosk: exist, exit, access
    ('if exists("image.png"):', r'^\s*(exists?|existing|exist\s*check|exit|access|is\s*there|check\s*exists?)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: type
    # Native: type | German-Vosk: tape, tight, tap, tip | Synonym: write, enter
    ('type("text")', r'^\s*(type|types|typing|tight|typed|tape|tap|tip|write|write\s*down|enter)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: paste
    # Native: paste | German-Vosk: past, paced, paid
    ('paste("text")', r'^\s*(paste|past|paced|paid|paste\s*text)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: hover
    # Native: hover | German-Vosk: howver, over, hoover
    ('hover("image.png")', r'^\s*(hover|hoover|hower|howver|move\s*mouse|over)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: drag drop
    ('dragDrop("source.png", "target.png")', r'^\s*(drag\s*(and\s*)?drop|dreg\s*drop|dragged\s*drop)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: scroll
    # Native: scroll | German-Vosk: school, skull, score
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(scroll|scrolling|school|skull|score|roll|wheel|scroll\s*down)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: sleep
    # Native: sleep | German-Vosk: slip, sheep
    ('sleep(1)', r'^\s*(sleep|sleeps|slip|sheep|pause|wait\s*a\s*second)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: popup
    ('popup("message")', r'^\s*(popup|pop\s*up|alert|message\s*box|show\s*message)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: highlight
    ('find("image.png").highlight(2)', r'^\s*(highlight|high\s*light|mark\s*it|show\s*region)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: capture
    # Native: capture | German-Vosk: captain, kept, captured
    ('capture(SCREEN)', r'^\s*(capture|captured|captain|kept|screenshot|screen\s*shot|take\s*screenshot)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: switch app
    ('switchApp("App Name")', r'^\s*(switch\s*app|switsch\s*app|switch\s*application|change\s*app)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: open app
    # Native: open app | German-Vosk: often, oven, urban
    ('openApp("app")', r'^\s*(open|often|oven|urban)\s*(app|application|up|start|launch)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: run
    ('run("script.sikuli")', r'^\s*(run|run\s*script|execute|execute\s*script|start\s*script)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),
]
