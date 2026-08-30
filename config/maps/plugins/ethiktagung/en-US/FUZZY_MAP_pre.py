# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/ethiktagung/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


"""
Workshop Nr.4.: Übernahme menschlicher Tätigkeit im Sozialunternehmen durch Technik, Robotik, IT.
"""

FUZZY_MAP_pre = [

    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.

    # have ethics


    # EXAMPLE: ethics tiago

    ('Ethiktagung, Freitag den 10 Oktober 2025', r'^(ethics tiago|ethics\s*day\w*|Ethics conference|ethics meeting|ethics\s*have|ethics\s*meeting|Ethics Council|ethics\s*Togo|Completed have|edict have)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Psychiatry Center

    ('ZfP = Zentrum für Psychiatrie', r'^(center.*psychiatry|Z\s*f\s*P|z is|ZDF [pt])$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Dieter

    ('Dieter Haug Stellvertretender Geschäftsführer, ZfP Südwürttemberg', r'^(Dieter|The) (Haug|have|how|Main|ouch)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Bernhard Schölkopf

    ('Prof. Dr. Bernhard Schölkopf, Direktor MPI für Intelligente Systeme Tübingen', r'^Bernard\s+(Schölkopf|nice\w*\s*Head|nice Basket|fast cook|shaw\sw*\w*|Transducer|Schalk\w*|writes|sh\w+ Head|right Head)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x bex tus Friedx rich

    ('Dr. Hubertus Friederich, Ärztlicher Direktor, Klinik für Psychiatrie und Psychosomatik, Alb-Neckar, ZfP Südwürttemberg, Vorsitzender Ärztlicher Verband Krankenhauspsychiatrie', r'^(\w*be\w*tus)\s+(Fried\w*rich|Peace|rider|peace)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x alf Aßfalx

    ('Ralf Aßfalg, Pflegedirektor, Klinik für Psychiatrie und Psychosomatik Alb-Neckar, ZfP Südwürttemberg', r'^(\w*alf)\s+(Assfal\w*|asphalt|alpha to case)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

     # EXAMPLE: Frank Schwärx

     ('Dr. Frank Schwärzler, Ärztlicher Direktor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^Frank\s+(Black\w*|difficult\w*|pain\w*|difficult\w*|fester\w*|black\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Uwe

    ('Uwe Armbruster, Pflegedirektor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^(Uwe|Oh Yes|New)\s+(crossbow\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Angelica

    ('Angelika Gasser, Leitung IT-Abteilung, ZfP Südwürttemberg', r'^(Angelica|Angela)\s+(alley\w*|Gaffer\w*|Gaza|Guest|the was|m gas)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Matthias Kohlerx

    ('Dr. Matthias Köhler, Chefarzt Alterspsychiatrie, ZfP Südwürttemberg', r'^Matthias\s+(Charcoal burner\w*|cool\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Julia

    ('Julia Kämmer, Wissenschaftliche Mitarbeiterin im Projekt „SMiLE2getherGaPa“ M.A. Angewandte, Gesundheitswissenschaft, Kath. Stiftungshochschule München', r'^(Julia|Jülich)\s+(\w+mmm\w*|Cameron|comes\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Leonix Baux s

    ('Leonie Bauer, Psychotherapeutin PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^\s*Leoni\w?\s+(Building\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: matt wood

    ('Martin Holzke, Zentralbereichsleitung Pflege und Medizin, Regionaldirektor Ravensburg-Bodensee, ZfP Südwürttemberg', r'^(frosted|Martin)\s+(Wood\s*\w*|ke|get\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Christian Freisem

    ('Christian Freisem, Leitung Geschäftsbereich Dienstleistungen, Abteilungsleitung Wirtschaftsabteilung, ZfP Südwürttemberg', r'^Christian\s+(Freisem|free\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

]

