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

# config/maps/plugins/git/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: utilice {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


CONFIG_DIR = Path(__file__).parent


# EXAMPLE: git

gitGit = r'(git|Va|Ella va|git|conseguir|red|falla|estado miembro|niños|kate|va[^\s]*|ir|red|gita|kate|kathe|gatito|fíat|con|equipo|durazno|abandonar)'

# un kit con texto en inglés


# EXAMPLE: Comprometerse

commitGit = r'(Comprometerse|cometa|Comedia|historietas|goma|gomas|llega|próximo|con|enganche|venir|cometas|kubiki|divertido|ganar|gromit|venir|kubi|cobit|cúbico|playa|acogedor|abandonar|Google)'

FUZZY_MAP_pre = [



    # EXAMPLE: número de versión

    ('git describe --tags --abbrev=0', r'^(versión número|número de versión)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),

    # EXAMPLE: sin verificar

    ('n --no-verify', r'^(No|solo|no|solo|novela|Números) (gratis|verificar|caso|muy lejos|bien)$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # no-verifyno-verifyl --no-verifyNumeri bien



    # EXAMPLE: punto b chemnitz b

    ('PUNCTUATION_MAP ', r'\b(punto Chemnitz)\b', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: git comprometerse

    ('git commit ', rf'^\s*{gitGit}\s+{commitGit}\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],}),
    # aquí only_in_windows se elimina porque se prueba en esl-test, y tal vez en otras ventanas 17.4.'26 15:08 Vie.



    # sucede muy raramente :D 18/11/25 5:53 p.m. Mar

    # EXAMPLE: El movimiento de cuarzo le da la bienvenida al ser humano.

    ('git commit message ', r'\bMovimiento de cuarzo da venir ser humano\b ', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: casi no da ninguna información

    ('git commit ', r'\bda apenas con\w*', 80,   {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # EXAMPLE: git comprometerse

    ('git commit ', r'\bgit comprometerse\b\s*', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # EXAMPLE: git comprometerse

    ('git commit ', r'\bgrid cometa\b\s*', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: texto de confirmación de git en inglés

    ('bitte Commit-Message for uncommitted changes', rf'\b{gitGit}\b\s*\b{commitGit} text in english\b', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: clon de git

    ('git clone ', rf'^\s*{gitGit}\s+(klar|klon|clone)\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # git@github.com:kiwix/kiwix-tools.git

    #


    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


    # EXAMPLE: solicitudes de extracción

    ('pull requests', r'^\s*(jalar\s*solicitudes.solicitudes?|Suéter\s*Búsqueda)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: solicitudes de extracción

    ('pull requests', r'\b(cero|jalar) solicitudes.solicitudes\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: el rompió

    ('er branch', r'él\b (en bancarrota|Principal)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Príncipe destacado

    ('feature branch ', r'\bCaracterística\s*príncipe\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Príncipe destacado

    ('feature branch ', r'\bCaracterística\s*(príncipe|rancho)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE}),


    # EXAMPLE: git pago

    ('git checkout ', r'^\s*(git|va)\s+(Git Verificar|Controlar-afuera)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git pago

    ('git checkout ', r'^\s*(más cursi|Va Cheka)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: rama git

    ('git branch -d', r'\b(Rama|Príncipe)\s*borrar\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Nombre de la sucursal

    ('Branch Name', r'\rama\s*nombres\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Comprometerse

    (' Commit ', r'\convertirse\s*con\b\s*', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: mensaje de confirmación

    (' Commit Message ', r'\recibir\s*con\s*Mensaje\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: nuevo lanzamiento

    ('neues Release ', r'\nuevo\s*(Liberar|mazmorra)\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- estado de git ---

    # Esta expresión regular reemplaza 5 entradas antiguas.

    # Empecemos el estado.

    # Va al estado git status git status A partir de ahora


    # EXAMPLE: estadogit

    ('git status ', r'^\s*(Va|Ella va|git|conseguir|red|falla|estado miembro|niños|kate)\s+(status|Estado|estado|estático|estado|comenzar|comienza|comenzar|granero|fechas)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: estados miembros

    ('git status ', r'^\s*(estado miembro|estados miembros|Ahora Ciudad|Va Estado es|va status)\s+(es)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: estado miembro

    ('git status ', r'^\s*(estado miembro|Pedal de arranque|Ahora comienza)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: gitschtal

    ('git status', r'^\s*(gitschtal|se deslizó|charlas tenía|chirridos|chirridos convertirse|Disparates tenía|Va hizo a nosotros)\s+$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # es estático



    # --- git agregar . --- git agregar .

    # Gitta tiene

    # EXAMPLE: git agregar.

    ('git add .', r'^\s*(git|va[^\s]*|ir|red|gita|kate|kathe|gatito|fíat|con)\s+(agregar|en|hizo|papá|tiene|dueto|deslizar|él|ahora|aplicación|él tiene)\s*(\.|\punto b\b)?\s*$', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Cuna

    ('git add .', r'^\s*(Cuna|Va él allá|crédito|membrillo tiene)\s*$', 78, # min_accuracy
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # va el tiene




    ############################################
    # una característica demasiado poderosa me gustaría desactivarla temporalmente (original: 'una característica demasiado poderosa me gustaría desactivarla temporalmente', SL5.de/Aura).


    # Si no ha habilitado "git wip" o desea utilizar:

    # diga: git add rápido

    # vaTiene rápidoVa rápido

    # git agregar. && git commit -m "WIP" && git push; && git


    # EXAMPLE: git WIP empujar

    ('!git add . && git commit -m "WIP" && git push', r'^\s*(git|va[^\s]*|ir|red|gita|kate|kathe|gatito|fíat|con)\s+(agregar|en|hizo|papá|tiene|dueto|deslizar|él|ahora|aplicación)\s*(rápido|rápido|sucio|limpiar)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: git WIP empujar

    ('!git add . && git commit -m "WIP" && git push; && git ', r'^\s*(git|va[^\s]*|ir|red|gita|kate|kathe|gatito|fíat|con)\s*(rápido|rápido|sucio|limpiar)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    ############################################

    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|now|app)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['consola', 'consola', 'Terminal', 'Consola']}),


    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|with)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'Konsole', 'Terminal', 'Console']}),


    # --- git confirmar ---

    # EXAMPLE: Klitschko con

    ('git commit ', r'^\s*Klitschko con\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: kate comprometerse

    ('git commit ', r'^\s*kate Comprometerse\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: un cometa

    ('git commit ', r'^\s*A cometas\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: ir a comprometerse

    ('git commit ', r'^\s*(Va Comprometerse|Va con qué|petkovic)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: ve, ven a comprometerte

    ('git commit ', r'^\s*Va venir Comprometerse\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: tu vas conmigo

    ('git commit ', r'^\s*(ir tú con)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: con qué

    ('git commit ', r'^\s*con qué\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: va cobit uno

    ('git commit ', r'^va cobit a$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git empujar

    ('git push ', r'^\s*(git|grande|va|red)\s*(arbusto|empujar|empujar|controlar|desaparecido)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Kate Bush

    ('git push ', r'^\s*kate\s+arbusto\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: pitbull

    ('git push ', r'^\s*pitbull\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git pull ---

    # EXAMPLE: git tirar

    ('git pull ', r'^\s*(git|va|tranquilo|red)\s*(jalar|pohl|piscina)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: s git tirar s

    ('git pull ', r'^\s*git\s*jalar\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git diferencia ---

    # EXAMPLE: diferencia git

    ('git diff ', r'^\s*(equipo|git|va|durazno)\s*(diff|profundo|pelea|tuv|jugo|consejos|va\'s|kittys|dies|die)\s*$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Comparación con el penúltimo compromiso

    ('git diff HEAD~1', r'^Comparación con penúltimo Comprometerse\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Última confirmación con diff s

    ('git log -p -1', r'^Último Comprometerse con Diff\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Muestra cambios preparados pero no comprometidos.

    ('git diff --cached', r'^Espectáculos escenificado (pero no comprometido) cambios\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: interruptor de git

    ('git switch ', r'^\s*(git|va|durazno)\s*(cambiar|Schmidt)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git tirar

    ('git fetch; git pull"', r'^\s*(git|Aplica|va) (jalar|gordo)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

##################################################################

    # EXAMPLE: solicitudes de extracción

    ('pull requests', r'^\s*(jalar\s*solicitudes.solicitudes?|Suéter\s*Búsqueda)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: solicitudes de extracción

    ('pull requests', r'\b(cero|jalar) solicitudes.solicitudes\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

# por favor escríbeme porque vendrá con texto'

    # EXAMPLE: viene con texto

    ('git commit text', r'\b(va venir con texto)\b', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Príncipe destacado

    ('feature branch', r'\bCaracterística\s*príncipe\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Eliminar rama

    ('git branch -d', r'\b(Rama|Príncipe)\s*borrar\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Nombres de ranchos

    ('Branch Name', r'\rama\s*nombres\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: mensaje de confirmación

    (' Commit', r'\convertirse\s*con\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: ven con mensaje

    (' Commit Message', r'\recibir\s*con\s*Mensaje\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: nuevo lanzamiento

    ('neues Release', r'\nuevo\s*(mazmorra|Liberar)\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Sección de código

    ('Code Abschnitt', r'\bkot\s*secciones\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: botón de parada

    ('StopButton', r'\bstob\s*botón\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: alaba el caso

    ('lowerCase', r'\manchas\s*Caso\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- estado de git ---

    # Esta expresión regular reemplaza 5 entradas antiguas.

    # EXAMPLE: estadogit

    ('git status', r'^\s*(git|va|red|niños)\s+(status|estado|fechas)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git agregar . ---

    # EXAMPLE: agregar git

    ('git add .', r'^\s*(git|va|ir|red|kate|fíat|con)\s+(agregar|lejos|en|conducir|hizo|papá|tiene|dueto|él)\s*(\.|\punto b\b)?\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git confirmar ---

    # Kate comete un compromiso de git


    # EXAMPLE: Klitschko con s

    ('git commit ', r'^\s*Klitschko con\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Kate se compromete

    ('git commit ', r'^\s*kate Comprometerse\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: ir cometa

    ('git commit ', r'^\s*Va (cometa|próximo|Comprometerse)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: un cometa

    ('git commit ', r'^\s*A cometas\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Ir a comprometerse

    ('git commit ', r'^\s*Va Comprometerse\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Ve, ven a comprometerte.

    ('git commit ', r'^\s*Va venir Comprometerse\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Va

    ('git commit ', r'^\s*(Va|git|con) (venir|cometas|Comprometerse)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: cometa

    ('commit ', r'\s+cometa\s+', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git

    ('git commit ', r'^\s*(git|con) venir\s*con\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: con que

    ('git commit ', r'^\s*con qué\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|va) venir?\s*con\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Aplica|va) (cometa|venir)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git push ---

    # EXAMPLE: git

    ('git push', r'^\s*(git|va|red)\s*(arbusto|empujar)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git pull ---

    # EXAMPLE: git

    ('git pull', r'^\s*(git|va|red)\s*(pohl|piscina)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: s git tirar s

    ('git pull', r'^\s*git\s*jalar\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git diferencia ---

    # EXAMPLE: git

    ('git diff', r'^\s*(git|va|durazno)\s*(diff|profundo|jugo)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Mostrar lo que se cambió en las últimas confirmaciones

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^\s*Espectáculo Qué en el último Comprometerse cambió convertirse\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Crítica de gruñidos

    ('.gitignore', r'^\s*(crítica gruñido|crítica Noé|Reseñas|gatito knorr|crítica knorr)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: da knorr

    ('.gitignore', r'\b(da knorr)\b$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: nuevo lanzamiento

    ("alias release_protokoll='gh release list --limit 100 | awk \"{print $1}\" | while read tag; do if [ -n \"$tag\" ]; then echo -e \"\n\n--- RELEASE: $tag ---\n\"; gh release view \"$tag\"; fi; done > all_releases.txt && kate all_releases.txt'", r'\b(lanzamientos\w* protocolo\w*|relé\w* Protocolos|todo lanzamientos|lanzamientos\w* exportar\w*|papas fritas Protocolos)\b$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


]





"""
gh release list --limit 100 | awk '{print $1}' | while read tag; do
    if [ -n "$tag" ]; then
        echo -e "\n\n--- RELEASE: $tag ---"
        gh release view "$tag" --json body -q '.body'
    fi
done > all_releases.txt && kate all_releases.txt
"""

