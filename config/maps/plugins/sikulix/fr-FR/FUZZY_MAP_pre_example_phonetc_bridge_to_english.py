# config/maps/plugins/sikulix/fr-FR/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent
sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli', 'oculixide', 'OculiX']

FUZZY_MAP_pre = [
    #################################################
    # 2. activez cette règle (derrière la première règle que vous souhaitez optimiser)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    # EXAMPLE: double clic
    # Native: double clic | Vosk-EN-Logic: double click, bubble league
    ('doubleClick("image.png")', r'^\s*(double\s*clic\w*|double\s*click|dub\s*clic|doublé\s*clic|double\s*quick)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: clic droit
    # Native: clic droit | Vosk-EN-Logic: clay draw, click draw, clay drought, click dry
    ('rightClick("image.png")', r'^\s*(clic\s*droit|clique\s*droit|clay\s*draw|click\s*draw|cliquez\s*droit|right\s*click)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: clic
    ('click("image.png")', r'^\s*(clic|clique|cliquez|cliquer|click|quick|clerk)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: attente disparition (wait vanish)
    ('waitVanish("image.png", 10)', r'^\s*(attend\s*disparition|attendre\s*disparition|attend\s*qu’il\s*parte|disparaît|vanish)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: attend (wait)
    # Native: attend, attendre | Vosk-EN-Logic: attend, a ton, a tan, wait
    ('wait("image.png", 10)', r'^\s*(attend|attendre|attendez|a\s*ton|a\s*tan|pause|wait|patience)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: trouve tout (find all)
    ('for m in findAll("image.png"):', r'^\s*(trouve\s*tout|trouver\s*tout|cherche\s*tout|find\s*all)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: trouve (find)
    ('find("image.png")', r'^\s*(trouve|trouver|cherche|chercher|trouvez|find|search)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: existe
    ('if exists("image.png"):', r'^\s*(existe|existait|présent|est\s*là|exists?)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: taper (type)
    # Native: tape, taper, écrire | Vosk-EN-Logic: tape, type, tap, write
    ('type("text")', r'^\s*(tape|taper|tapez|écris|écrire|écrivez|saisir|type|write)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: coller (paste)
    ('paste("text")', r'^\s*(colle|coller|collez|paste)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: survoler (hover)
    ('hover("image.png")', r'^\s*(survole|survoler|survolez|hover|move\s*mouse)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: glisser déposer (drag drop)
    ('dragDrop("source.png", "target.png")', r'^\s*(glisse\s*dépose|glisser\s*déposer|drag\s*drop)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: défiler (scroll)
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(défile|défiler|molette|scroll|wheel)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: dormir (sleep)
    ('sleep(1)', r'^\s*(dort|dormir|pause|sommeil|sleep)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: capture
    ('capture(SCREEN)', r'^\s*(capture|écran|photo|screenshot|screen\s*shot)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: basculer app (switch app)
    ('switchApp("App Name")', r'^\s*(bascule\s*app|change\s*app|switch\s*app)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: ouvrir app (open app)
    ('openApp("app")', r'^\s*(ouvre\s*app|ouvrir\s*app|lance\s*app|lancer\s*app|open\s*app)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),
]
