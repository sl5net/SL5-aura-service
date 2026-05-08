# config/maps/plugins/standard_actions/bookmark_link_url_navigator/de-DE/Copy-Shop/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}) # noqa: E702



FUZZY_MAP_pre = [


    # Copy-Shop


    # bitsundso website bus982
    # EXAMPLE: Copy-Shop
    ('Ferdinand-Lassalle-Straße 17-19, 72770 Reutlingen', r'^(Copy-Shop|Copyshop).*Betzingen\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPEL: Copyshop Betzingen Industriegebiet
    # EXAMPLE: Betzingen Copy-Shop
    ('Ferdinand-Lassalle-Straße 17-19, 72770 Reutlingen', r'^(Betzingen).*(Copy-Shop|Copyshop)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPEL: Copyshop Betzingen Industriegebiet
    # EXAMPLE: Betzingen Copy-Shop
    ('https://www.openstreetmap.org/#map=18/48.491606/9.156450', r'^(Betzingen).*(Copy-Shop|Copyshop)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),


]

readme = """

https://www.schreibwaren-ehinger.de/
Steinachstraße 3-5, 72770 Reutlingen-Betzingen
Montag - Freitag07:00 - 12:30 Uhr14:00 - 18:30 UhrSamstag06:30 - 13:00 Uhr
https://www.schreibwaren-ehinger.de/index.php?id=4
Schreibgerätereparatur,Laminier-Service,Fotokopien
pdf auf usb stick geht.

Copy-Shop (Karl-Henschel-Str. 5) Teil eines Fachmarktzentrums ist, teilt er sich den Parkplatz mit:

dm-drogerie markt (großer Drogeriemarkt)

Deichmann (Schuhgeschäft)

Takko Fashion (Bekleidung)

Tedi (Schreibwaren, Deko, Haushaltsartikel)

Fressnapf (Tierbedarf, direkt daneben in der Nr. 1)


















Copy-Shop in Reutlingen von WiesingerMedia GmbH. Wir drucken Ihnen alles was Sie benötigen: Kopien, Ausdrucke, Abschlussarbeiten, Visitenkarten, Poster.

dm-drogerie markt, Ferdinand-Lassalle-Straße 17-19, 72770 Reutlingen
dm-drogerie markt, Ferdinand-Lassalle-Straße 17-19, 72770 Reutlingen - Öffnungszeiten, Zusatzsortimente, Services in der dm Filiale & mehr. Hier finden Sie alle Infos!
Ferdinand-Lassalle-Straße 17-19, Reutlingen, 7277007121 506427

"""
