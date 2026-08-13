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

# config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702





# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: utilice {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


# too<-from

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


    # Acumulación: Reglas (acumular) de modo que quizás solo sea visible la última regla. Ejemplos:


    # La siguiente regla se aplica a todo:

    # ('---', r'^.*$', 5, # min_accuracy {'command_flags': re.IGNORECASE}),


    # La siguiente regla se aplica a todo excepto a la palabra casa:

    # EXAMPLE: Casa

    # ('', r'^(?!Casa).*$', 5, {'command_flags': re.IGNORECASE}),

    # PruebaPruebaPruebaCasaCasaCasaMujer deCasa Árbol debajoBuen díaJaque mateJaque mate

    # Jaque mateJaque mate


    # La siguiente regla se aplica a todo excepto a las palabras jaque, mate:

    # EXAMPLE: Ajedrez

    # ('', r'^(?!check|mate|mala|casa).*$', 5, {'command_flags': re.IGNORECASE}),

    # AjedrezAjedrezCasaAjedrezAjedrezCuarto de baño

    # Mate


    # EXAMPLE: Ajedrez

    # ('Jaque mate', r'^(Jaque mate|malo|Casa).*$', 5, {'command_flags': re.IGNORECASE}),

    # Jaque mateJaque mate




    ('LECKER_EXAKT', 'Marmelade', 100, {'command_flags': re.IGNORECASE}),
    # Mermelada MermeladaLECKER_EXAKT


    # Prueba 2: regla tolerante (se permiten errores tipográficos)

    # También debe reconocerse la 'Marmelada' o 'Marmelad'.

    # ('LECKER_FUZZY', 'JAM', 1, {'command_flags': re.IGNORECASE}),


    # Mermelada Mermelada Mammon Mammon Mama Marion Málaga

    # Mamá MarionA es delgada





]
