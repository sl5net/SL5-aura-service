# config/maps/plugins/sikulix/es-ES/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent
sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli', 'oculixide', 'OculiX']

FUZZY_MAP_pre = [
    #################################################
    # 2. activa esta regla (detrás de la primera regla que quieras optimizar)

    #################################################

    # EXAMPLE: doubleClick
    # Native: doble clic | Vosk-EN-Logic: double click, bubble click
    ('doubleClick("image.png")', r'^\s*(doubleClick|doble\s*clic|double\s*clic|clic\s*doble|dub\s*clic|double\s*click)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: clic derecho
    # Native: clic derecho | Vosk-EN-Logic: click the reach oh, clay dare a show, right click
    ('rightClick("image.png")', r'^\s*(clic\s*derecho|cliquea\s*derecho|click\s*derecho|right\s*click)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: clic
    # Native: clic, haz clic | Vosk-EN-Logic: as click, es click, click, cleak
    ('click("image.png")', r'^\s*(clic|click|clica|cliquea|haz\s*clic|as\s*click|es\s*click|quick)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: espera a que desaparezca (wait vanish)
    ('waitVanish("image.png", 10)', r'^\s*(espera\s*desaparezca|cuando\s*se\s*vaya|espera\s*vanish|vanish)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: espera (wait)
    # Native: espera, esperar | Vosk-EN-Logic: as pair a, repair, space, wait
    ('wait("image.png", 10)', r'^\s*(espera|esperar|espere|as\s*pair\s*a|repair|wait|pausa)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: busca todos (find all)
    ('for m in findAll("image.png"):', r'^\s*(busca\s*todos|buscar\s*todos|encontrar\s*todos|find\s*all)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: busca (find)
    ('find("image.png")', r'^\s*(busca|buscar|encuentra|encontrar|busque|find|search)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: existe
    ('if exists("image.png"):', r'^\s*(existe|existirá|está\s*ahí|hay|exists?)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: escribe (type)
    # Native: escribe, escribir | Vosk-EN-Logic: as cree bay, ice cree bay, type, tape
    ('type("text")', r'^\s*(escribe|escribir|teclea|teclear|as\s*cree\s*bay|type|write)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: pega (paste)
    ('paste("text")', r'^\s*(pega|pegar|pegue|paste)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: mover ratón encima (hover)
    ('hover("image.png")', r'^\s*(pon\s*encima|sobrevuela|pasa\s*por\s*encima|hover|move\s*mouse)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: arrastra y suelta (drag drop)
    ('dragDrop("source.png", "target.png")', r'^\s*(arrastra\s*y\s*suelta|arrastrar|drag\s*drop)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: desplazar (scroll)
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(desplaza|desplazar|bajar|rueda|scroll|wheel)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: dormir / pausa (sleep)
    ('sleep(1)', r'^\s*(duerme|dormir|espera\s*un\s*segundo|pausa|sleep)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: captura
    ('capture(SCREEN)', r'^\s*(captura|pantallazo|foto|screenshot|screen\s*shot)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: cambiar app (switch app)
    ('switchApp("App Name")', r'^\s*(cambia\s*app|cambiar\s*app|switch\s*app)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: abrir app (open app)
    ('openApp("app")', r'^\s*(abre\s*app|abrir\s*app|lanza\s*app|lanzar\s*app|open\s*app)\s*$', 85, {
        'flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),
]
