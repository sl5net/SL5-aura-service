# config/maps/plugins/linux_commands/de-DE/FUZZY_MAP_pre.py
# file config/maps/plugins/it-begriffe/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

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
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: Benachritext stoeren
    (f'{BenachrichtigungenPosition}', r'^Benachri\w+ stoeren$'),
    # EXAMPLE: Benachrichtigtext Position
    (f'{BenachrichtigungenPosition}', r'^Benachrichtig\w+ Position$', 75, {'flags': re.IGNORECASE}),



    # EXAMPLE: AutoKey
    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe symbol|paid symbol|treib symbol|Paypal Symbol|pep|prep simba|treib simba|Paypal Simba)\b', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe|paid|treib|Paypal|pep|prep|treib|Paypal) (symbol|simba|simpel|simbel|schimmer|SIM)\b', 75, {'flags': re.IGNORECASE}),

    # === Linux/Unix Commands ===


    # EXAMPLE: grep recursive
    ('grep -r "aura_engine.py" . --exclude-dir={.git,.venv,__pycache__,data} | wc -l',
     # EXAMPLE: grep recursive
     r'^(grep recursive|kriechen recursiv|grep Durchsuchung)$', 80, {
    'flags': re.IGNORECASE,
    'skip_list': ['LanguageTool']
    }),



    # EXAMPLE: find files
    ('find . -name', r'^(find files|finde Dateien|Suche Dateien)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: pkill process
    ('pkill -f', r'^(kill process|Prozess beenden|pkill)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: sed replace in file
    ('sed -i', r'^(sed replace|ersetze in Datei|sed Ersetzung)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: cat with line numbers
    ('cat -n', r'^(cat numbered|cat mit Zahlen|zeige nummeriert|Zeige numerisch)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),






    # EXAMPLE: download webpage webseite
    ('wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://www. x.de/',
        # EXAMPLE: download webpage
        r'^(download) (webpage|webseite)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: alle Dateitypen
    ('find . -type f -exec file -b --mime-type {} + | sort | uniq -c',
        # EXAMPLE: alle Dateitypen
        r'^(alle) (Dateitypen|Metadaten)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),


    # EXAMPLE: alle Dateitypen Metadaten
    ('find . -type f -exec file -b {} + | sort | uniq -c', r'^(alle) (Dateitypen|Metadaten)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),


    # EXAMPLE: grep with kate output
    ('grep -n "text" file | xclip -selection clipboard', r'^(grep nach Kate|suche und kopiere|grep in Zwischenablage)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),


    # EXAMPLE: restart Watcher
    ('pkill -f type_watcher; sleep 0.1; ./type_watcher_keep_alive.sh &', r'^(Watcher neu starten|restart Watcher)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: show recent logs
    ('tail -20 ~/projects/py/STT/log/type_watcher.log', r'^(zeige letzte logs|show recent logs|letzte Log Einträge)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),






    # EXAMPLE: show last commit
    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^(zeige letzten Commit|show last commit|letzter Commit Diff)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),


    # EXAMPLE: check Watcher processes
    ('ps aux | grep type_watcher', r'^(prüfe Watcher Prozesse|check Watcher processes|zeige Watcher Prozesse)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: aura process timestamps
    ('ps -eo pid,lstart,cmd | grep type_watcher', r'^(zeige Watcher Startzeiten|show Watcher start times|Watcher Prozess Zeiten|aura process timestamps)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: search in aura script
    ('grep -n "check_config_changed" ~/projects/py/STT/type_watcher.sh', r'^(suche Config Check|search config check|finde Config Funktion)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: show Watcher script numbered
    ('cat -n ~/projects/py/STT/type_watcher.sh', r'^(zeige Watcher Script nummeriert|show Watcher script numbered|Watcher Script mit Zeilen)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: count lines in aura script
    ('wc -l ~/projects/py/STT/type_watcher.sh', r'^(zähle Watcher Zeilen|count Watcher lines|wie lang ist Watcher|Wie lange ist Hodscha)$', 80, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    #Wie lange ist Hodscha

    # EXAMPLE: edit aura config
    ('kate ~/projects/py/STT/config/settings_local.py', r'^(editiere lokale Config|edit local config|öffne lokale Einstellungen)$', 85, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),


    # Examples: disk usage
    (f"gdu",
    # EXAMPLE: ordnergröße
    r'^(ordnergröße|speicherfresser|festplatte voll|verzeichnisgröße|gdu|duf|disk usage)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Launch ncdu
    (f"ncdu",
        # EXAMPLE: ordner größe
        r'^(ordner größe|verzeichnis größe|speicherplatz anzeigen|festplatte prüfen|ncdu|Launch ncdu|wie groß sind die ordner)$',
        90,
        {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # Examples: disk usage
    (f"gdu",
    # EXAMPLE: folder size
    r'^(folder size|directory size|disk usage|storage hog|gdu|disk full)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # Examples: disk space
    (f"ncdu",
        # EXAMPLE: check storage
        r'^(check storage|ncdu|launch ncdu|how big are the folders|disk space)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]
