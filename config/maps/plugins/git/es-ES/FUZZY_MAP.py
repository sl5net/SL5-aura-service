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

# config/maps/plugins/git/de-DE/FUZZY_MAP.py

# config/languagetool_server/maps/de-DE/FUZZY_MAP.py

import re

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - significa que primero es lo más importante, es posible que las reglas inferiores no se lean.

    # EXAMPLE: alaba el caso

    ('lowerCase', r'\manchas\s*Caso\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: algunos pocos

    ('Manjaro', r'\b(Alguno pareja|monjes euro)\b', 75, {'command_flags': re.IGNORECASE}),


# ('.', r'^\s*(punto|pup)\s*$', 82, {'command_flags': re.IGNORECASE}),





    # EXAMPLE: solicitudes de extracción

    ('pull requests', r'^\s*(jalar\s*solicitudes.solicitudes?|Suéter\s*Búsqueda)\s*$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: cero

    ('pull requests', r'\b(cero|jalar) solicitudes.solicitudes\b', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Príncipe destacado

    ('feature branch', r'\bCaracterística\s*príncipe\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Rama

    ('git branch -d', r'\b(Rama|Príncipe)\s*borrar\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Nombres de ranchos

    ('Branch Name', r'\rama\s*nombres\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Venga conmigo

    (' Commit ', r'\convertirse\s*con\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: ven con bitkom

    (' Commit ', r'\convertirse\s*con\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    ('git commit ', r'^bitcom con$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: ven con mensaje

    (' Commit Message', r'\recibir\s*con\s*Mensaje\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: nueva mazmorra

    ('neues Release', r'\nuevo\s*mazmorra\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: heces cortadas

    ('Code Abschnitt', r'\bkot\s*secciones\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: botón de parada

    ('StopButton', r'\bstob\s*botón\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: alaba el caso

    ('lowerCase', r'\manchas\s*Caso\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- estado de git ---

    # Esta expresión regular reemplaza 5 entradas antiguas.


    # EXAMPLE: estadogit

    ('git status', r'^(se deslizó|estados miembros|arranque|chirridos lejos|él Status)$', 82,
     {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: estadogit

    ('git status', r'^\s*(git|va|red|niños)\s+(status|estado|en lugar de|estadio|fechas)\s*$', 82,  {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- git agregar . ---

    # tiene lugar

    # EXAMPLE: agregar git

    ('git add .', r'^\s*(git|va|ir|red|kate|fíat|con)\s+(agregar|en|hizo|papá|tiene|dueto|él)\s*(\.|\punto b\b)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git commit en medio del texto en algún lugar: ---

    # EXAMPLE: git comprometerse

    ('git commit ', r'\b(Va|git|bien|con) (Comprometerse)\b\s*', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git confirmar ---

    # Kate comete un compromiso de git


    # EXAMPLE: Klitschko con

    ('git commit ', r'^\s*Klitschko con\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Kate se compromete

    ('git commit ', r'^\s*kate Comprometerse\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: ir cometa

    ('git commit ', r'^\s*Va (cometa|próximo|correctamente|Comprometerse)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: un cometa

    ('git commit ', r'^\s*A cometas\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: ir a comprometerse

    ('git commit ', r'^\s*Va Comprometerse\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # EXAMPLE: ve, ven a comprometerte

    ('git commit ', r'^\s*Va venir Comprometerse\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Va

    ('git commit ', r'^\s*(Va|git|bien|con) (venir|cometas|Comprometerse|kevin)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),





    # EXAMPLE: cometa

    (' commit ', r'\s+cometa\s+', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: git

    ('git commit ', r'^\s*(git|con) venir\s*con\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: con qué

    ('git commit ', r'^\s*con qué\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|va) venir?\s*con\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Aplica|va) (cometa|venir)\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # Dorado ven ven


    # ahora también en línea reemplazos:

    # EXAMPLE: git comprometerse

    ('git commit "', r'\b(git|Aplica|va) (cometa|venir|kubitz)\b\s*"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),





    # --- git push ---

    # EXAMPLE: git empujar

    ('git push', r'^\s*(git|va|red)\s*(arbusto|fresco|empujar|probablemente)\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git pull ---

    # EXAMPLE: git tirar

    ('git pull', r'^\s*(git|va|red)\s*(pohl|piscina)\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git tirar

    ('git pull', r'^\s*git\s*jalar\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- git diferencia ---

    # EXAMPLE: diferencia git

    ('git diff', r'^\s*(git|va|durazno)\s*(diff|profundo|jugo)\s*$', 75, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

]
