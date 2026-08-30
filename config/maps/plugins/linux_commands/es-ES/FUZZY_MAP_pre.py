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

# config/maps/plugins/linux_commands/de-DE/FUZZY_MAP_pre.py

# archivo de configuración/maps/plugins/it-terms/FUZZY_MAP_pr.py

# Beispiel: https://www.it-begriffe.de/#L

import re

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


BenachrichtigungenPosition = """
    KDE
    Systemeinstellungen > Benachrichtigungen > Position wählen

    XFCE
    Einstellungen > Benachrichtigungen > Standardposition

    GNOME
    Erweiterung "Just Perfection" installieren > Benachrichtigungsposition

    Ganz ausschalten (alle)
    Klick auf Uhrzeit/Glocke > Nicht stören
    
"""



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.




    # EXAMPLE: Texto de notificación de molestias

    (f'{BenachrichtigungenPosition}', r'^Notificación\w+ molestar$'),
    # EXAMPLE: Posición del texto de notificación

    (f'{BenachrichtigungenPosition}', r'^notificado\w+ posición$', 75, {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: Clave automática

    ('AutoKey', r'\bCoche k\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: tubo

    ('|', r'\b(tubo|tubo símbolo|pagado símbolo|conducir símbolo|PayPal símbolo|energía|deberes Simba|conducir Simba|PayPal Simba)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: tubo

    ('|', r'\b(tubo|tubo|pagado|conducir|PayPal|energía|deberes|conducir|PayPal) (símbolo|Simba|simple|sencillo|brillar|SIM)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # === Linux/Unix Commands ===


    # EXAMPLE: grep recursivo

    ('grep -r "aura_engine.py" . --exclude-dir={.git,.venv,__pycache__,data} | wc -l',
     # EXAMPLE: grep recursivo

     r'^(grep recursivo|arrastrarse recursivo|grep buscar)$', 80, {
    'command_flags': re.IGNORECASE,
    'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: encontrar archivos

    ('find . -type f -path "*zip.py"', r'^(encontrar archivos|encontrar archivos|Buscar archivos)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # encontrar archivos


    # EXAMPLE: proceso de eliminación

    ('pkill -f', r'^(matar proceso|proceso finalizar|matar)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: sed reemplazar en el archivo

    ('sed -i', r'^(sed reemplazar|reemplazar en archivo|sed Reemplazo)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: gato con números de línea

    ('cat -n', r'^(gato numerado|gato con Pagar|espectáculo numerado|Espectáculo numérico)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: descargar pagina web sitio web

    ('wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://www. x.de/',
        # EXAMPLE: descargar pagina web

        r'^(descargar) (Página web|sitio web)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: todos los tipos de archivos

    ('find . -type f -exec file -b --mime-type {} + | sort | uniq -c',
        # EXAMPLE: todos los tipos de archivos

        r'^(todo) (Tipos de archivos|Metadatos)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: todos los tipos de archivos metadatos

    ('find . -type f -exec file -b {} + | sort | uniq -c', r'^(todo) (Tipos de archivos|Metadatos)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: grep con salida kate

    ('grep -n "text" file | xclip -selection clipboard', r'^(grep después kate|buscar y Copiar|grep en Portapapeles)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: reiniciar Vigilante

    ('pkill -f type_watcher; sleep 0.1; ./scripts/sh/type_watcher_keep_alive.sh &', r'^(Vigilantes nuevo comenzar|Reanudar Vigilantes)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: mostrar registros recientes

    ('tail -20 ~/projects/py/STT/log/type_watcher.log', r'^(espectáculo último registros|espectáculo reciente registros|último registro Entradas)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: mostrar el último compromiso

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^(espectáculo último Comprometerse|espectáculo carga comprometerse|último Comprometerse Diff)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: comprobar los procesos de Watcher

    ('ps aux | grep type_watcher', r'^(prüfe Watcher Prozesse|check Watcher processes|zeige Watcher Prozesse)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: marcas de tiempo del proceso del aura

    ('ps -eo pid,lstart,cmd | grep type_watcher', r'^(zeige Watcher Startzeiten|show Watcher start times|Watcher Prozess Zeiten|aura process timestamps)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: buscar en el guión del aura

    ('grep -n "check_config_changed" ~/projects/py/STT/type_watcher.sh', r'^(buscar configuración Controlar|buscar configuración controlar|encontrar configuración función)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: mostrar guión de Watcher numerado

    ('cat -n ~/projects/py/STT/type_watcher.sh', r'^(espectáculo Vigilantes Guion numerado|espectáculo Vigilantes guion numerado|Vigilantes Guion con pauta)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: contar líneas en la escritura del aura

    ('wc -l ~/projects/py/STT/type_watcher.sh', r'^(contar Vigilantes pauta|contar Vigilantes pauta|Cómo largo es Vigilantes|Cómo largo es hodja)$', 80, # min_accuracy
     {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # config/maps/plugins/linux_commands/de-DE/FUZZY_MAP_pre.py:205

    # EXAMPLE: estado de git brevemente

    ( 'clear;git diff --shortstat',
        r'^(git\s+(status|diff)?\s*corto|git  corto|git status corto|git estadística|git descripción general)$',
      {
          'command_flags': re.IGNORECASE,
          'skip_list': ['LanguageTool']
          , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: git diff dirstat

    ( 'clear;git diff --dirstat',
        r'^(git\s+(status|diff)?\s*estado sucio|git\s+estado sucio|git\s+carpeta\s+estadística|git\s+directorio\s+descripción general)$',
        {
            'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
            'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console'],
        },
    ),

    # git diferencia pequeña

    # EXAMPLE: diferencia git

    ('clear;git diff -U0 > /tmp/aura_small_diff.txt && kate /tmp/aura_small_diff.txt',
     r'^(git diff)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
         , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: dispositivo de sonido al editor kate

    ('./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt',
     r'^(sonido kate)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
     , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # ¿Cuánto dura Hodja?


    # EXAMPLE: editar configuración de aura

    ('kate ~/projects/py/STT/config/settings_local.py', r'^(editar local configuración|editar local configuración|abierto local Ajustes)$', 85, # min_accuracy
    {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Ejemplos: uso del disco

    ("gdu",
    # EXAMPLE: tamaño de carpeta

    r'^(tamaño de carpeta|cerdos de memoria|disco duro lleno|tamaño del directorio|gdu|duf|disco uso.uso)$',
    90,
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Lanzar ncdu

    ("ncdu",
        # EXAMPLE: tamaño de carpeta

        r'^(carpeta tamaño|directorio tamaño|espacio de almacenamiento espectáculo|disco duro controlar|ncdu|Lanzamiento ncdu|Cómo grande son el carpeta)$',
        90,
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Ejemplos: uso del disco

    ("gdu",
    # EXAMPLE: tamaño de carpeta

    r'^(carpeta tamaño|directorio tamaño|disco uso.uso|almacenamiento.almacenamiento cerdo|gdu|disco lleno)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Ejemplos: espacio en disco

    ("ncdu",
        r'^(controlar almacenamiento.almacenamiento|ncdu|lanzamiento ncdu|cómo grande son el carpetas|disco espacio)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Ejemplos: espacio en disco

    ("ncdu",
        r'^(controlar almacenamiento.almacenamiento|ncdu|lanzamiento ncdu|cómo grande son el carpetas|disco espacio)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Ejemplos: conmutador de ventana rofi

    ("rofi -show window -window-hide-active-window -window-format '{t}' -window-match-fields title true -sort", r'^(rofi|ventana.ventana conmutador|conmutador)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),





]
