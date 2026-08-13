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

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702





# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


"""
Workshop Nr.4.: Übernahme menschlicher Tätigkeit im Sozialunternehmen durch Technik, Robotik, IT.
"""

FUZZY_MAP_pre = [

    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.

    # tener ética


    # EXAMPLE: ética tiago

    ('Ethiktagung, Freitag den 10 Oktober 2025', r'^(ética tiago|ética\s*día\w*|conferencia de ética|ética reunión|ética\s*tener|ética\s*reunión|Consejo de Ética|ética\s*Ir|Terminado tener|edicto tener)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Centro de Psiquiatría

    ('ZfP = Zentrum für Psychiatrie', r'^(centro.*psiquiatría|Z\s*f\s*P|z es|ZDF [pt])$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Dieter

    ('Dieter Haug Stellvertretender Geschäftsführer, ZfP Südwürttemberg', r'^(Dieter|El) (haug|tener|cómo|Principal|Ay)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Bernhard Schölkopf

    ('Prof. Dr. Bernhard Schölkopf, Direktor MPI für Intelligente Systeme Tübingen', r'^Bernardo\s+(Schölkopf|lindo\w*\s*Cabeza|lindo Cesta|rápido cocinar|shaw\sudoeste*\w*|transductor|Chalco\w*|escribe|sh\w+ Cabeza|bien Cabeza)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x bex tus Friedx rico

    ('Dr. Hubertus Friederich, Ärztlicher Direktor, Klinik für Psychiatrie und Psychosomatik, Alb-Neckar, ZfP Südwürttemberg, Vorsitzender Ärztlicher Verband Krankenhauspsychiatrie', r'^(\w*ser\w*tus)\s+(Frito\w*rico|Paz|jinete|paz)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: x alf Aßfalx

    ('Ralf Aßfalg, Pflegedirektor, Klinik für Psychiatrie und Psychosomatik Alb-Neckar, ZfP Südwürttemberg', r'^(\w*alfo)\s+(Asfalto\w*|asfalto|alfa a caso)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

     # EXAMPLE: Frank Schwärx

     ('Dr. Frank Schwärzler, Ärztlicher Direktor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^Franco\s+(Negro\w*|difícil\w*|dolor\w*|difícil\w*|enconarse\w*|negro\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: uwe

    ('Uwe Armbruster, Pflegedirektor, PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^(uwe|Oh Sí|Nuevo)\s+(ballesta\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Angélica

    ('Angelika Gasser, Leitung IT-Abteilung, ZfP Südwürttemberg', r'^(Angélica|Ángela)\s+(callejón\w*|Capataz\w*|Gaza|Invitado|el era|m gas)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Matthias Kohlerx

    ('Dr. Matthias Köhler, Chefarzt Alterspsychiatrie, ZfP Südwürttemberg', r'^Matías\s+(Quemador de carbón\w*|Frío\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Julia

    ('Julia Kämmer, Wissenschaftliche Mitarbeiterin im Projekt „SMiLE2getherGaPa“ M.A. Angewandte, Gesundheitswissenschaft, Kath. Stiftungshochschule München', r'^(Julia|Jülich)\s+(\w+mmm\w*|Cameron|llega\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Leonix Baux s

    ('Leonie Bauer, Psychotherapeutin PP.rt Klinik für Psychiatrie und Psychosomatik, Reutlingen', r'^\s*Leoni\w?\s+(Edificio\w*)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: madera mate

    ('Martin Holzke, Zentralbereichsleitung Pflege und Medizin, Regionaldirektor Ravensburg-Bodensee, ZfP Südwürttemberg', r'^(escarchado|Martín)\s+(Madera\s*\w*|ke|conseguir\w+)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Christian Freisem

    ('Christian Freisem, Leitung Geschäftsbereich Dienstleistungen, Abteilungsleitung Wirtschaftsabteilung, ZfP Südwürttemberg', r'^cristiano\s+(Freisem|gratis\w*)$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

]

