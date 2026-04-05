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
    ('doubleClick("image.png")', r'^\s*(double\s*click|dub click|durable click|double quick|dublin click|doppelklick|doubleclick)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: right click
    ('rightClick("image.png")', r'^\s*(right\s*click|right click|write click|right klick)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: click
    ('click("image.png")', r'^\s*(click|klick|quick|clip|clit|clique|clicked|clicks)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: wait vanish
    ('waitVanish("image.png", 10)', r'^\s*(wait\s*vanish|wait till gone|wait until gone|wait disappear|vanish|wait for vanish)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: wait
    ('wait("image.png", 10)', r'^\s*(wait|wade|weight|waits|waited|what|woke|wate|Await Image|Wait Pattern|Watch Screen|Expect Icon|Wait Region|Scan Image|Image Wait|Watch Region|Pixel Watch|Visual Wait|Screen Watch|Icon Await|Pattern Wait|Region Scan|Element Wait)\s*$', 85, {
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
    ('if exists("image.png"):', r'^\s*(exists?|existing|exist check|is there|check exists?)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: type
    ('type("text")', r'^\s*(type|types|typing|tight|typed)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: paste
    ('paste("text")', r'^\s*(paste|past|paced|paste text)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: hover
    ('hover("image.png")', r'^\s*(hover|hoover|move mouse|over)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: drag drop
    ('dragDrop("source.png", "target.png")', r'^\s*(drag\s*(and)?\s*drop|drag drop|dragged drop)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: scroll
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(scroll|scroll down|wheel|scrolling)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: sleep
    ('sleep(1)', r'^\s*(sleep|pause|wait a second|sleeps)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: popup
    ('popup("message")', r'^\s*(popup|pop up|alert|message box|show message)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: highlight
    ('find("image.png").highlight(2)', r'^\s*(highlight|high light|mark it|show region)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: capture
    ('capture(SCREEN)', r'^\s*(capture|screenshot|screen shot|take screenshot)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: switch app
    ('switchApp("App Name")', r'^\s*(switch\s*app|switch application|change app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: open app
    ('openApp("app")', r'^\s*(open\s*app|open application|start app|launch app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: run
    ('run("script.sikuli")', r'^\s*(run|run script|execute|execute script)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
]
