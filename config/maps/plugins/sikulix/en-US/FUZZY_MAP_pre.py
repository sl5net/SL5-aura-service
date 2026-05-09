# config/maps/plugins/sikulix/en-US/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent

sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli']

FUZZY_MAP_pre = [
    #################################################
    # 2. activate this rule (behind the first rule you want to optimize)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    # EXAMPLE: double click
    ('doubleClick("image.png")', r'^\s*(double\s*click|dub\s*click|dopple\s*click|durable\s*click|double\s*quick|dublin\s*click|doppelklick|doubleclick)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: right click
    ('rightClick("image.png")', r'^\s*(right\s*click|write\s*click|right\s*klick)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: click
    ('click("image.png")', r'^\s*(click|klick|lick|quick|clip|clit|clique|clicked|clicks)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: wait vanish
    ('waitVanish("image.png", 10)', r'^\s*(wait\s*vanish|wait\s*till\s*gone|wait\s*until\s*gone|wait\s*disappear|vanish|wait\s*for\s*vanish)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: wait
    ('wait("image.png", 10)', r'^\s*(wait|wade|weight|white|wheat|waits|waited|what|woke|wate|Await Image|Wait Pattern|Watch Screen|Expect Icon|Wait Region|Scan Image|Image Wait|Watch Region|Pixel Watch|Visual Wait|Screen Watch|Icon Await|Pattern Wait|Region Scan|Element Wait)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: find all
    ('for m in findAll("image.png"):', r'^\s*(find\s*all|find\s*every|find\s*each|locate\s*all)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: find
    ('find("image.png")', r'^\s*(find|finds|fine|found|locate|search)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: exists
    ('if exists("image.png"):', r'^\s*(exists?|existing|exist\s*check|is\s*there|check\s*exists?|presence)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: type
    ('type("text")', r'^\s*(type|write|write\s*down|enter|types|typing|tight|typed)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: paste
    ('paste("text")', r'^\s*(paste|past|paced|paste\s*text)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: hover
    ('hover("image.png")', r'^\s*(hover|hoover|move\s*mouse|over)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: drag drop
    ('dragDrop("source.png", "target.png")', r'^\s*(drag\s*(and\s*)?drop|dragged\s*drop)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: scroll
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(scroll|roll|scroll\s*down|wheel|scrolling)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: sleep
    ('sleep(1)', r'^\s*(sleep|pause|wait\s*a\s*second|sleeps)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: popup
    ('popup("message")', r'^\s*(popup|pop\s*up|alert|message\s*box|show\s*message)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: highlight
    ('find("image.png").highlight(2)', r'^\s*(highlight|high\s*light|mark\s*it|show\s*region)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: capture
    ('capture(SCREEN)', r'^\s*(capture|screenshot|screen\s*shot|take\s*screenshot)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: switch app
    ('switchApp("App Name")', r'^\s*(switch\s*app|switch\s*application|change\s*app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: open app
    ('openApp("app")', r'^\s*(open\s*app|open\s*application|start\s*app|launch\s*app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: run
    ('run("script.sikuli")', r'^\s*(run|run\s*script|execute|execute\s*script)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
]
