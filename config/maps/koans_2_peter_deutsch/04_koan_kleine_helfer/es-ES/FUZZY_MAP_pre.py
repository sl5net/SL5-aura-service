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

# config/maps/koans_2_peter_deutsch/04_koan_kleine_helfer/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# Formato de regla: ('texto de reemplazo', r'patrón', umbral, banderas)

# Lógica: De arriba hacia abajo, el primer golpe gana. Fullmatch (^...$) detiene la canalización.


# PETER TAREA para Koan: 04_koan_kleine_helfer

# Hay 3 reglas comentadas.

# -> Activa la PRIMERA regla (elimina el '#').

# -> Las demás son alternativas para comparar.

FUZZY_MAP_pre = [

    # HACER


    # ¿Quizás así?

    # ('Super :) Felicitaciones', r'^Su Muy Honorable Arch-Amts-Rath-zu-Przewalskyst-Silesien-Westpfalz, diputado comercial real electoral y verdadero representante de la cronología xenocrónica.*$'),


    # o eso?

    # ('Genial :) Felicitaciones', r'^Su Señoría.*$'),


    # ¿Y el título?

    # ¿Quizás así?

    # ('Phryxts-Tschrudel-Wzeschtsch-Chryschth Condesa von und zu Echtschluchtz-Quartzschicht-Prtschnitz-Krüppelschwärz.', r'^.*gräfin.*$'),


    # Los códigos de área son principalmente 0707 (Tübingen) y 0712 (Reutlingen), así como variaciones para las ciudades más pequeñas de los alrededores.


    # Descripción de expresiones regulares del código de área de Tubinga y sus alrededores (0707x)

    # EXAMPLE: Código de área zona principal de Tubinga

    ('07071', r'^Prefijo telefónico Tubinga Zona principal$'),
    # EXAMPLE: Código de área Dußlingen

    ('07073', r'^Prefijo telefónico Dusslingen$'),
    # EXAMPLE: Código de área Rotemburgo del Neckar

    ('07074', r'^Prefijo telefónico Rotemburgo en Neckar$'),
    # EXAMPLE: Código de área Ammerbuch

    ('07075', r'^Prefijo telefónico Ammerbuch$'),
    # EXAMPLE: Código de área de Gomaringen

    ('07076', r'^Prefijo telefónico Gomaringen$'),
    # EXAMPLE: Código de área Mössingen

    ('07078', r'^Prefijo telefónico Mössingen$'),

    # Descripción de la expresión regular del código de área de Reutlingen y alrededores (0712x)

    # EXAMPLE: Código de área de la zona principal de Reutlingen

    ('07121', r'^Prefijo telefónico Reutlingen Zona principal$'),
    # EXAMPLE: Código de área de Metzingen

    ('07122', r'^Prefijo telefónico Metzingen$'),
    # EXAMPLE: Código de área Reutlingen-Degerschlacht

    ('07123', r'^Prefijo telefónico Reutlingen-batalla deger$'),
    # EXAMPLE: Código de área Pliezhausen

    ('07124', r'^Prefijo telefónico Pliezhausen$'),
    # EXAMPLE: Código de área Pfullingen

    ('07125 hi all', r'^Prefijo telefónico Pfullingen$'),
    # EXAMPLE: Código de área Neckartenzlingen

    ('07127', r'^Prefijo telefónico Neckartenzlingen$'),

    # ¿También puedes hacer otras preguntas? ¿Quizás le hayan emitido su propio número completo?

    #

]
