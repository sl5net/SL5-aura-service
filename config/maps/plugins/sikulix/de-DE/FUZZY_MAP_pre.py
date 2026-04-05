# config/maps/plugins/sikulix/de-DE/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent

sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli']

FUZZY_MAP_pre = [
    # EXAMPLE: wait vanish waitVanish("image.png", 10)

    #################################################
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    # EXAMPLE: doppelklick
    ('doubleClick("image.png")', r'^\s*(doppelklick|doch wirklich|du wirst lebt|du bist|doppelt|top wirklich|doppel|doppel quick|du klickst|drucken klickt|doppelspitze|wirklich|doppelklick|doubleclick|du bist vip|top gepflegt|du bequem|top ist witz|doppel klick|du bist witz|du bist blitz|so gezwickt|du|dort wird fit|so wirklich|top klick|ob wirklich|doppel trick|job wirklich|doppel\w*klick|double\s*click)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),


    # EXAMPLE: rechtsklick
    ('rightClick("image.png")', r'^\s*(rechts\w*klick|right\s*click)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: klick
    ('click("image.png")', r'^(klick|quitt|klicken|quiz|clip|klickt|klick klick|quick|klicken)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: warte
    ('wait("image.png", 10)', r'^(arte|warte|wort|was|oh|mord|morte|morgen wollte|wollte|bartöl|wow schön|worthülsen wozu|wow schiff|wow show|können worte|warten|wasserrutsche|warm|warm trinken|worte|boris|wartet|waren|warnt|warten warten warte|wahre|ward|überhaupt|Warte auf Bild|Such Bereich|Icon-Wache|Erwarte Muster|Screen Check|Bild Suche|Treffer Abfrage|Scan Region|Muster Wartezeit|Grafik Suche|Bereichs Überwachung|Bild Erwartung|Fokus Scan|Element Warten|Visueller Check|Such Modus|Pixel Wache|Erkenne Icon|Region Scan)$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: waitVanish bis weg
    ('waitVanish("image.png", 10)', r'^(Warte bis weg|Element Verschwinden|Pixel Leerung|Wenn weg weiter|Muster Ende|Bild Vanish|Abwesenheits Check|Icon Abgang|Bereich frei Scan|Verschwinde Wache|Grafik Aus|Muster Exitus|Such Ende|Scan Leere|Lösch Check|Verschwinde Timer|Weg Abfrage|Element Ausblenden|Icon Verlust|Leer Scan)$', 85, {
        'flags': re.IGNORECASE,
    }),



    # EXAMPLE: find all
    ('for m in findAll("image.png"):', r'^\s*(find\s*all|alle\s*find\w*|alle\s*such\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: find
    ('find("image.png")', r'^\s*(find|finde?|such\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: exists
    ('if exists("image.png"):', r'^\s*(exists?|existiert|vorhanden|gibt\s*es)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: type
    ('type("text")', r'^\s*(type|tipp\w*|schreib\w*|eingabe)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: paste
    ('paste("text")', r'^\s*(paste|einfüg\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: hover
    ('hover("image.png")', r'^\s*(hover|beweg\w*\s*maus)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: drag drop
    ('dragDrop("source.png", "target.png")', r'^\s*(drag\s*(and)?\s*drop|zieh\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: scroll
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(scroll\w*|rolle\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: sleep
    ('sleep(1)', r'^\s*(sleep|pause)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: popup
    ('popup("message")', r'^\s*(popup|meldung|hinweis|alert)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: highlight
    ('find("image.png").highlight(2)', r'^\s*(highlight|hervorheb\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: capture
    ('capture(SCREEN)', r'^\s*(capture|screenshot|aufnahme)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: switch app
    ('switchApp("App Name")', r'^\s*(switch\s*app|wechsel\w*\s*app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: open app
    ('openApp("app")', r'^\s*(open\s*app|öffne?\s*app|starte?\s*app)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
    # EXAMPLE: run
    ('run("script.sikuli")', r'^\s*(run|ausführ\w*|starte?\s*script)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': sikulix_windows,
    }),
]
