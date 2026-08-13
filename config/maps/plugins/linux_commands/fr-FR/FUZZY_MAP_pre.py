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

# fichier config/maps/plugins/it-terms/FUZZY_MAP_pr.py

# Beispiel: https://www.it-begriffe.de/#L

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


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
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.




    # EXAMPLE: Texte de notification de perturbation

    (f'{BenachrichtigungenPosition}', r'^Notification\w+ déranger$'),
    # EXAMPLE: Position du texte de notification

    (f'{BenachrichtigungenPosition}', r'^Notifié\w+ position$', 75, {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: Clé automatique

    ('AutoKey', r'\bVoiture k\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: tuyau

    ('|', r'\b(tuyau|tuyau symbole|payé symbole|conduire symbole|Paypal symbole|dynamisme|préparation Simba|conduire Simba|Paypal Simba)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: tuyau

    ('|', r'\b(tuyau|tuyau|payé|conduire|Paypal|dynamisme|préparation|conduire|Paypal) (symbole|Simba|simple|simple|miroiter|Carte SIM)\b', 75, # min_accuracy
 {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # === Linux/Unix Commands ===


    # EXAMPLE: grep récursif

    ('grep -r "aura_engine.py" . --exclude-dir={.git,.venv,__pycache__,data} | wc -l',
     # EXAMPLE: grep récursif

     r'^(grep récursif|ramper récursif|grep recherche)$', 80, {
    'command_flags': re.IGNORECASE,
    'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: trouver des fichiers

    ('find . -type f -path "*zip.py"', r'^(trouver fichiers|trouver fichiers|Recherche fichiers)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # trouver des fichiers


    # EXAMPLE: processus pkill

    ('pkill -f', r'^(tuer processus|processus finition|pkill)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: sed remplacer dans le fichier

    ('sed -i', r'^(sed remplacer|remplacer dans déposer|sed Remplacement)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: chat avec numéros de ligne

    ('cat -n', r'^(chat numéroté|chat avec Payer|montrer numéroté|Montrer numérique)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: télécharger la page Web du site Web

    ('wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://www. x.de/',
        # EXAMPLE: télécharger la page Web

        r'^(télécharger) (page web|site web)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: tous les types de fichiers

    ('find . -type f -exec file -b --mime-type {} + | sort | uniq -c',
        # EXAMPLE: tous les types de fichiers

        r'^(tous) (Types de fichiers|Métadonnées)$', 80, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: métadonnées de tous les types de fichiers

    ('find . -type f -exec file -b {} + | sort | uniq -c', r'^(tous) (Types de fichiers|Métadonnées)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: grep avec la sortie de Kate

    ('grep -n "text" file | xclip -selection clipboard', r'^(grep après Kate|recherche et copie|grep dans Presse-papiers)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: redémarrer l'observateur

    ('pkill -f type_watcher; sleep 0.1; ./scripts/sh/type_watcher_keep_alive.sh &', r'^(Observateurs nouveau commencer|redémarrage Observateurs)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: afficher les journaux récents

    ('tail -20 ~/projects/py/STT/log/type_watcher.log', r'^(montrer dernier journaux|montrer récent journaux|dernier enregistrer Entrées)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),






    # EXAMPLE: afficher le dernier commit

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^(montrer dernier Commettre|montrer charger commettre|dernier Commettre Diff)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: vérifier les processus Watcher

    ('ps aux | grep type_watcher', r'^(prüfe Watcher Prozesse|check Watcher processes|zeige Watcher Prozesse)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: horodatages du processus d'aura

    ('ps -eo pid,lstart,cmd | grep type_watcher', r'^(zeige Watcher Startzeiten|show Watcher start times|Watcher Prozess Zeiten|aura process timestamps)$', 85, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: rechercher dans le script aura

    ('grep -n "check_config_changed" ~/projects/py/STT/type_watcher.sh', r'^(recherche Configuration Vérifier|recherche configuration vérifier|trouver Configuration fonction)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: afficher le script Watcher numéroté

    ('cat -n ~/projects/py/STT/type_watcher.sh', r'^(montrer Observateurs Scénario numéroté|montrer Observateurs scénario numéroté|Observateurs Scénario avec lignes)$', 80, # min_accuracy
 {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: compter les lignes dans le script aura

    ('wc -l ~/projects/py/STT/type_watcher.sh', r'^(compter Observateurs lignes|compter Observateurs lignes|Comment long est Observateurs|Comment long est Hodja)$', 80, # min_accuracy
     {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # config/maps/plugins/linux_commands/de-DE/FUZZY_MAP_pre.py:205

    # EXAMPLE: statut git brièvement

    ( 'clear;git diff --shortstat',
        r'^(git\s+(status|diff)?\s*court|git  court|git status court|git statistiques|git aperçu)$',
      {
          'command_flags': re.IGNORECASE,
          'skip_list': ['LanguageTool']
          , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: répertoire de diff git

    ( 'clear;git diff --dirstat',
        r'^(git\s+(status|diff)?\s*dirstat|git\s+dirstat|git\s+dossier\s+statistiques|git\s+annuaire\s+aperçu)$',
        {
            'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
            'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console'],
        },
    ),

    # git diff petit

    # EXAMPLE: git diff

    ('clear;git diff -U0 > /tmp/aura_small_diff.txt && kate /tmp/aura_small_diff.txt',
     r'^(git diff)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
         , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: périphérique audio pour l'éditeur Kate

    ('./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt',
     r'^(son Kate)$', 85, # min_accuracy
    {
         'command_flags': re.IGNORECASE,
         'skip_list': ['LanguageTool']
     , 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Quelle est la durée de Hodja ?


    # EXAMPLE: modifier la configuration de l'aura

    ('kate ~/projects/py/STT/config/settings_local.py', r'^(modifier locale Configuration|modifier locale configuration|ouvrir locale Paramètres)$', 85, # min_accuracy
    {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    ,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Exemples : utilisation du disque

    ("gdu",
    # EXAMPLE: taille du dossier

    r'^(taille du dossier|porcs de mémoire|disque dur complet|taille du répertoire|gdu|ouf|disque utilisation.usage)$',
    90,
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Lancer ncdu

    ("ncdu",
        # EXAMPLE: taille du dossier

        r'^(dossier taille|annuaire taille|espace de stockage montrer|disque dur vérifier|ncdu|Lancement ncdu|Comment grand sont le dossier)$',
        90,
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Exemples : utilisation du disque

    ("gdu",
    # EXAMPLE: taille du dossier

    r'^(dossier taille|annuaire taille|disque utilisation.usage|stockage.stockage porc|gdu|disque complet)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Exemples : espace disque

    ("ncdu",
        r'^(vérifier stockage.stockage|ncdu|lancement ncdu|comment grand sont le dossiers|disque espace)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # Exemples : espace disque

    ("ncdu",
        r'^(vérifier stockage.stockage|ncdu|lancement ncdu|comment grand sont le dossiers|disque espace)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Exemples: rofi window switcher

    ("rofi -show window -window-hide-active-window -window-format '{t}' -window-match-fields title true -sort", r'^(rofi|fenêtre.fenêtre commutateur|commutateur)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),





]
