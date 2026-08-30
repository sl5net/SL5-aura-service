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

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


"""
Workshop Nr.4.: Übernahme menschlicher Tätigkeit im Sozialunternehmen durch Technik, Robotik, IT.
"""

FUZZY_MAP_pre = [

    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.

    # avoir une éthique


    # EXAMPLE: éthique tiago

    ('Ethiktagung, Freitag den 10 Oktober 2025', r'^(éthique Tiago|éthique\s*jour\w*|Conférence déthique|éthique réunion|éthique\s*avoir|éthique\s*réunion|Conseil déthique|éthique\s*Aller|Complété avoir|décret avoir)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Centre de psychiatrie

    ('ZfP = Zentrum für Psychiatrie', r'^(centre.*psychiatrie|Z\s*f\s*P|z est|ZDF [pt])$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Dieter

    ('Dieter Haug Stellvertretender Geschäftsführer, ZfP Südwürttemberg', r'^(Dieter|Le) (Haug|avoir|comment|Principal|Aie)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Bernhard Schölkopf

    ('Prof. Dr. Bernhard Schölkopf, Direktor MPI für Intelligente Systeme Tübingen', r'^Bernard\s+(Schölkopf|bon\w*\s*Tête|bon Panier|rapide cuisiner|shaw\sw*\w*|Transducteur|Schalk\w*|écrit|merde\w+ Tête|droite Tête)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x bex tus Friedx riche

    ('Dr. Hubertus Friederich, Ärztlicher Direktor, Klinik für Psychiatrie und Psychosomatik, Alb-Neckar, ZfP Südwürttemberg, Vorsitzender Ärztlicher Verband Krankenhauspsychiatrie', r'^(\w*être\w*tu)\s+(Frit\w*riche|Paix|cavalier|paix)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x alf Assfalx

    ('Ralf Aßfalg, Pflegedirektor, Klinik für Psychiatrie und Psychosomatik Alb-Neckar, ZfP Südwürttemberg', r'^(\w*alf)\s+(Assfal\w*|asphalte|alpha à cas)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

     # EXAMPLE: Frank Schwärx

     ('Dr. Frank Schwärzler, Ärztlicher Direktor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^Franc\s+(Noir\w*|difficile\w*|douleur\w*|difficile\w*|suppurer\w*|noir\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Uwe

    ('Uwe Armbruster, Pflegedirektor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^(Uwe|Oh Oui|Nouveau)\s+(arbalète\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Angélique

    ('Angelika Gasser, Leitung IT-Abteilung, ZfP Südwürttemberg', r'^(Angélique|Angèle)\s+(ruelle\w*|Gaffer\w*|Gaza|Invité|le était|m gaz)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Matthias Kohlerx

    ('Dr. Matthias Köhler, Chefarzt Alterspsychiatrie, ZfP Südwürttemberg', r'^Mathias\s+(Brûleur à charbon\w*|cool\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Julie

    ('Julia Kämmer, Wissenschaftliche Mitarbeiterin im Projekt „SMiLE2getherGaPa“ M.A. Angewandte, Gesundheitswissenschaft, Kath. Stiftungshochschule München', r'^(Julie|Juliers)\s+(\w+mmm\w*|Cameron|vient\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Léonix Baux

    ('Leonie Bauer, Psychotherapeutin PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^\s*Léoni\w?\s+(Bâtiment\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: bois mat

    ('Martin Holzke, Zentralbereichsleitung Pflege und Medizin, Regionaldirektor Ravensburg-Bodensee, ZfP Südwürttemberg', r'^(givré|Martine)\s+(Bois\s*\w*|hé|obtenir\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Christian Freisem

    ('Christian Freisem, Leitung Geschäftsbereich Dienstleistungen, Abteilungsleitung Wirtschaftsabteilung, ZfP Südwürttemberg', r'^chrétien\s+(Freisem|gratuit\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

]

