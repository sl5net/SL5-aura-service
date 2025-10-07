# config/maps/plugins/ethiktagung/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401


# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use re.IGNORECASE for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

"""
Workshop Nr.4.: Übernahme menschlicher Tätigkeit im Sozialunternehmen durch Technik, Robotik, IT.
"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    ('Ethiktagung, Freitag den 10 Oktober 2025', r'^(ethik tiago|Ethik\s*Tag\w*|Ethiktagung|ethik tagung|Ethik\s*Tagung|Ethikrat|Ethik\s*Togo|Erledigt haben|Edikt haben)$', 80, re.IGNORECASE),

    ('ZfP = Zentrum für Psychiatrie', r'^(Zentrum.*Psychiatrie|Z\s*f\s*P|z ist|ZDF [pt])$', 80, re.IGNORECASE),

    ('Dieter Haug Stellvertretender Geschäftsführer, ZfP Südwürttemberg', r'^(Dieter|Die) (Haug|haben|how|Haupt|au)$', 80, re.IGNORECASE),

    ('Prof. Dr. Bernhard Schölkopf, Direktor MPI für Intelligente Systeme Tübingen', r'^Bernhard\s+(Schölkopf|schön\w*\s*Kopf|schön Korb|schnell koch|shaw\sw*\w*|Schallkopf|Schalk\w*|schreibt|sch\w+ Kopf|gell Kopf)$', 80, re.IGNORECASE),

    ('Dr. Hubertus Friederich, Ärztlicher Direktor, Klinik für Psychiatrie und Psychosomatik, Alb-Neckar, ZfP Südwürttemberg, Vorsitzender Ärztlicher Verband Krankenhauspsychiatrie', r'^(\w*be\w*tus)\s+(Fried\w*rich|Frieden|rider|friede)$', 80, re.IGNORECASE),

    ('Ralf Aßfalg, Pflegedirektor, Klinik für Psychiatrie und Psychosomatik Alb-Neckar, ZfP Südwürttemberg', r'^(\w*alf)\s+(Aßfal\w*|Asphalt|alpha zu fall)$', 80, re.IGNORECASE),

     ('Dr. Frank Schwärzler, Ärztlicher Direktor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^Frank\s+(Schwär\w*|schwer\w*|schmerz\w*|schwers\w*|schwär\w*|schwar\w*)\s*$', 80, re.IGNORECASE),

    ('Uwe Armbruster, Pflegedirektor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^(Uwe|oh ja|Neue)\s+(Armbrust\w*)$', 80, re.IGNORECASE),

    ('Angelika Gasser, Leitung IT-Abteilung, ZfP Südwürttemberg', r'^(Angelika|Angela)\s+(Gasse\w*|Gaffer\w*|Gaza|Gast|das war|m Gas)$', 80, re.IGNORECASE),

    ('Dr. Matthias Köhler, Chefarzt Alterspsychiatrie, ZfP Südwürttemberg', r'^Matthias\s+(Köhler\w*|küh\w*)$', 80, re.IGNORECASE),

    ('Julia Kämmer, Wissenschaftliche Mitarbeiterin im Projekt „SMiLE2getherGaPa“ M.A. Angewandte, Gesundheitswissenschaft, Kath. Stiftungshochschule München', r'^(Julia|Jülicher)\s+(\w+mme\w*|Cameron|käm\w+)$', 80, re.IGNORECASE),

    ('Leonie Bauer, Psychotherapeutin PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^\s*Leoni\w?\s+(Bau\w*)\s*$', 80, re.IGNORECASE),

    ('Martin Holzke, Zentralbereichsleitung Pflege und Medizin, Regionaldirektor Ravensburg-Bodensee, ZfP Südwürttemberg', r'^(matt|Martin)\s+(Holz\s*\w*|ke|hol\w+)$', 80, re.IGNORECASE),

    ('Christian Freisem, Leitung Geschäftsbereich Dienstleistungen, Abteilungsleitung Wirtschaftsabteilung, ZfP Südwürttemberg', r'^Christian\s+(Freisem|frei\w*)$', 80, re.IGNORECASE),

]

