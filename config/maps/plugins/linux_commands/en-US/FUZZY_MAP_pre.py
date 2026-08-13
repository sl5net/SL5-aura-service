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

# file config/maps/plugins/it-terms/FUZZY_MAP_pr.py

# Beispiel: https://www.it-begriffe.de/#L

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

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

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.




    # EXAMPLE: Disturb notification text

    (f'{BenachrichtigungenPosition}', r'^Notification\w+ disturb$'),
    # EXAMPLE: Notification text position

    (f'{BenachrichtigungenPosition}', r'^Notified\w+ position$', 75, {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: AutoKey

    ('AutoKey', r'\bCar k\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: pipe

    ('|', r'\b(pipe|pipe symbol|paid symbol|drive symbol|Paypal symbol|pep|prep Simba|drive Simba|Paypal Simba)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: pipe

    ('|', r'\b(pipe|pipe|paid|drive|Paypal|pep|prep|drive|Paypal) (symbol|Simba|simple|simble|shimmer|SIM)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # === Linux/Unix Commands ===


    # EXAMPLE: grep recursive

    ('grep -r "aura_engine.py" . --exclude-dir={.git,.venv,__pycache__,data} | wc -l',
     # EXAMPLE: grep recursive

     r'^(grep recursive|creep recursive|grep search)$', 80, {
    'command_flags': re.IGNORECASE,
    'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: find files

    ('find . -type f -path "*zip.py"', r'^(find files|find files|Search files)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # find files


    # EXAMPLE: pkill process

    ('pkill -f', r'^(kill process|process finish|pkill)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: sed replace in file

    ('sed -i', r'^(sed replace|replace in file|sed Replacement)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: cat with line numbers

    ('cat -n', r'^(cat numbered|cat with Pay|show numbered|Show numerical)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: download webpage website

    ('wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://www. x.de/',
        # EXAMPLE: download webpage

        r'^(download) (webpage|website)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: all file types

    ('find . -type f -exec file -b --mime-type {} + | sort | uniq -c',
        # EXAMPLE: all file types

        r'^(all) (File types|Metadata)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: all file types metadata

    ('find . -type f -exec file -b {} + | sort | uniq -c', r'^(all) (File types|Metadata)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: grep with kate output

    ('grep -n "text" file | xclip -selection clipboard', r'^(grep after Kate|search and copy|grep in Clipboard)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: restart Watcher

    ('pkill -f type_watcher; sleep 0.1; ./scripts/sh/type_watcher_keep_alive.sh &', r'^(Watchers new start|restart Watchers)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: show recent logs

    ('tail -20 ~/projects/py/STT/log/type_watcher.log', r'^(show last logs|show recent logs|last log Entries)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: show last commit

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^(show last Commit|show load commit|last Commit Diff)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: check Watcher processes

    ('ps aux | grep type_watcher', r'^(prüfe Watcher Prozesse|check Watcher processes|zeige Watcher Prozesse)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: aura process timestamps

    ('ps -eo pid,lstart,cmd | grep type_watcher', r'^(zeige Watcher Startzeiten|show Watcher start times|Watcher Prozess Zeiten|aura process timestamps)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: search in aura script

    ('grep -n "check_config_changed" ~/projects/py/STT/type_watcher.sh', r'^(search Config Check|search config check|find Config function)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: show Watcher script numbered

    ('cat -n ~/projects/py/STT/type_watcher.sh', r'^(show Watchers Script numbered|show Watchers script numbered|Watchers Script with lines)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: count lines in aura script

    ('wc -l ~/projects/py/STT/type_watcher.sh', r'^(count Watchers lines|count Watchers lines|How long is Watchers|How long is Hodja)$', 80, # min_accuracy
     {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # config/maps/plugins/linux_commands/de-DE/FUZZY_MAP_pre.py:205

    # EXAMPLE: git status briefly

    ( 'clear;git diff --shortstat',
        r'^(git\s+(status|diff)?\s*short|git  short|git status short|git statistics|git overview)$',
      {
          'command_flags': re.IGNORECASE,
          'skip_list': ['LanguageTool']
          , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: git diff dirstat

    ( 'clear;git diff --dirstat',
        r'^(git\s+(status|diff)?\s*dirstat|git\s+dirstat|git\s+folder\s+statistics|git\s+directory\s+overview)$',
        {
            'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
            'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console'],
        },
    ),

    # git diff small

    # EXAMPLE: git diff

    ('clear;git diff -U0 > /tmp/aura_small_diff.txt && kate /tmp/aura_small_diff.txt',
     r'^(git diff)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
         , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: sound device to kate editor

    ('./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt',
     r'^(sound Kate)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
     , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # How long is Hodja?


    # EXAMPLE: edit aura config

    ('kate ~/projects/py/STT/config/settings_local.py', r'^(edit local Config|edit local config|open local Settings)$', 85, # min_accuracy
    {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Examples: disk usage

    ("gdu",
    # EXAMPLE: folder size

    r'^(folder size|memory hogs|hard drive full|directory size|gdu|duf|disk usage.usage)$',
    90,
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Launch ncdu

    ("ncdu",
        # EXAMPLE: folder size

        r'^(folder size|directory size|storage space show|hard drive check|ncdu|Launch ncdu|How large are the folder)$',
        90,
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Examples: disk usage

    ("gdu",
    # EXAMPLE: folder size

    r'^(folder size|directory size|disk usage.usage|storage.storage hog|gdu|disk full)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Examples: disk space

    ("ncdu",
        r'^(check storage.storage|ncdu|launch ncdu|how big are the folders|disk space)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Examples: disk space

    ("ncdu",
        r'^(check storage.storage|ncdu|launch ncdu|how big are the folders|disk space)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Examples: rofi window switcher

    ("rofi -show window -window-hide-active-window -window-format '{t}' -window-match-fields title true -sort", r'^(rofi|window.window switcher|switcher)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),





]
