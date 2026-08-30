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

import re

# depuis pathlib import Path as p;import os as o
# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


CONFIG_DIR = Path(__file__).parent


# EXAMPLE: git

gitGit = r'(git|Va|Elle va|git|obtenir|grille|problème|État membre|enfants|Kate|va[^\s]*|aller|grille|Gitta|Kate|Kathé|chaton|décret|avec|trousse|pêche|quitter)'

# un kit avec texte en anglais


# EXAMPLE: Commettre

commitGit = r'(Commettre|comète|Comédie|bandes dessinées|caoutchouc|caoutchoucs|vient|à venir|avec|attelage|viens|Comètes|Kubicki|drôle|gagner|gromit|viens|Kubis|cobit|cubique|plage|confortable|quitter|Google)'

FUZZY_MAP_pre = [



    # EXAMPLE: numéro de version

    ('git describe --tags --abbrev=0', r'^(version nombre|numéro de version)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),

    # EXAMPLE: pas de vérification

    ('n --no-verify', r'^(Non|seulement|non|seulement|roman|Nombres) (gratuit|vérifier|cas|très loin|bien)$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # no-verifyno-verifyl --no-verifyNumeri bien



    # EXAMPLE: b point chemnitz b

    ('PUNCTUATION_MAP ', r'\b(indiquer Chemnitz)\b', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: git commit

    ('git commit ', rf'^\s*{gitGit}\s+{commitGit}\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],}),
    # ici, only_in_windows est supprimé car il est testé dans le test esl, et nous pouvons peut-être dans d'autres fenêtres 17.4.'26 15:08 Fri



    # arrive très rarement :D 18/11/25 17h53 Mar

    # EXAMPLE: Le mouvement à quartz donne vie à l'être humain

    ('git commit message ', r'\bMouvement à quartz donne viens être humain\b ', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: ne donne pratiquement aucune contribution

    ('git commit ', r'\bdonne à peine avec\w*', 80,   {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # EXAMPLE: git commit

    ('git commit ', r'\bgit commettre\b\s*', 80, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),

    # EXAMPLE: git commit

    ('git commit ', r'\bgrille comète\b\s*', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: texte de commit git en anglais

    ('bitte Commit-Message for uncommitted changes', rf'\b{gitGit}\b\s*\b{commitGit} text in english\b', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: clone git

    ('git clone ', rf'^\s*{gitGit}\s+(klar|klon|clone)\s*$', 80,    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    }),


    # git@github.com:kiwix/kiwix-tools.git



    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # EXAMPLE: demandes de tirage

    ('pull requests', r'^\s*(tirer\s*demandes.demandes?|Pull-over\s*Quête)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: demandes de tirage

    ('pull requests', r'\b(zéro|tirer) demandes.demandes\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: il s'est cassé

    ('er branch', r'il\b (cassé|Prime)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Prince vedette

    ('feature branch ', r'\bFonctionnalité\s*prince\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Prince vedette

    ('feature branch ', r'\bFonctionnalité\s*(prince|ranch)\b', 82, # min_accuracy
   {'command_flags': re.IGNORECASE}),


    # EXAMPLE: git paiement

    ('git checkout ', r'^\s*(git|va)\s+(Git Vérifier|Vérifier-dehors)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git paiement

    ('git checkout ', r'^\s*(plus ringard|Va Tchéka)\s*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: branche git

    ('git branch -d', r'\b(Bifurquer|Prince)\s*supprimer\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Nom de la succursale

    ('Branch Name', r'\bifurquer\s*noms\b', 82, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Commettre

    (' Commit ', r'\devenir\s*avec\b\s*', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Message de validation

    (' Commit Message ', r'\recevoir\s*avec\s*Message\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: nouvelle version

    ('neues Release ', r'\nouveau\s*(Libérer|cachot)\b', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # === Git Commands (Consolidated & Case-Insensitive) ===

    # --- statut git ---

    # Cette expression régulière remplace 5 anciennes entrées.

    # Commençons l'état

    # Passe à l'état git status git status À partir de maintenant


    # EXAMPLE: statut git

    ('git status ', r'^\s*(Va|Elle va|git|obtenir|grille|problème|État membre|enfants|Kate)\s+(status|État|État|statique|État|commencer|commence|commencer|grange|rendez-vous)\s*$', 82, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: États membres

    ('git status ', r'^\s*(État membre|États membres|Maintenant Ville|Va État est|va status)\s+(est)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: État membre

    ('git status ', r'^\s*(État membre|Kickstarter|Maintenant commence)\s*$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: gitschtal

    ('git status', r'^\s*(gitschtal|glissé|discussions avait|couine|couine devenir|Absurdité avait|Va a fait nous)\s+$', 80, # min_accuracy
   {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # est statique



    # --- git ajouter . --- git ajouter .

    # Gitta a

    # EXAMPLE: git ajouter .

    ('git add .', r'^\s*(git|va[^\s]*|aller|grille|Gitta|Kate|Kathé|chaton|décret|avec)\s+(ajouter|à|a fait|papa|a|duo|glisser|il|maintenant|application|il a)\s*(\.|\point b\b)?\s*$', 82, # min_accuracy
           {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Lit bébé

    ('git add .', r'^\s*(Lit bébé|Va il là|crédit|coing a)\s*$', 78, # min_accuracy
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # Va il a




    ############################################
    # une fonctionnalité trop puissante, je souhaite la désactiver temporairement (original : « une fonctionnalité trop puissante, je souhaite la désactiver temporairement », SL5.de/Aura ).


    # si vous n'avez pas activé "git wip" ou si vous souhaitez peut-être utiliser :

    # dis : git add quick

    # vaA viteVa vite

    # git ajouter . && git commit -m "WIP" && git push; && git


    # EXAMPLE: git WIP pousser

    ('!git add . && git commit -m "WIP" && git push', r'^\s*(git|va[^\s]*|aller|grille|Gitta|Kate|Kathé|chaton|décret|avec)\s+(ajouter|à|a fait|papa|a|duo|glisser|il|maintenant|application)\s*(rapide|rapide|sale|essuyer)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: git WIP pousser

    ('!git add . && git commit -m "WIP" && git push; && git ', r'^\s*(git|va[^\s]*|aller|grille|Gitta|Kate|Kathé|chaton|décret|avec)\s*(rapide|rapide|sale|essuyer)?\s*$', 82,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    ############################################

    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|mit)\s+(add|at|tat|dad|hat|duett|rutsch|es|now|app)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows' : ['console', 'console', 'Terminal', 'Console']}),


    # (f'cd {CONFIG_DIR}/../../../../../; !git add . && git commit -m "WIP" && git push', r'^\s*(git|go[^\s]*|go|gitter|Gitta|kate|käthe|kitte|fiat|with)\s*(quick|fast|dirty|wip)?\s*$', 82, {'command_flags' : re.IGNORECASE, 'only_in_windows' : ['Konsole', 'Konsole', 'Terminal', 'Console']}),


    # --- git commit ---

    # EXAMPLE: Klitschko avec

    ('git commit ', r'^\s*Klitschko avec\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Kate s'engage

    ('git commit ', r'^\s*Kate Commettre\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Une comète

    ('git commit ', r'^\s*UN Comètes\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Allez vous engager

    ('git commit ', r'^\s*(Va Commettre|Va avec quoi|petković)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Allez, venez vous engager

    ('git commit ', r'^\s*Va viens Commettre\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: tu viens avec moi

    ('git commit ', r'^\s*(aller toi avec)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: avec quoi

    ('git commit ', r'^\s*avec quoi\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: va en cobit un

    ('git commit ', r'^va cobit un$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git pousser

    ('git push ', r'^\s*(git|grand|va|grille)\s*(buisson|pousser|pousser|vérifier|disparu)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Kate Bush

    ('git push ', r'^\s*Kate\s+buisson\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: pitbull

    ('git push ', r'^\s*pitbull\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git pull ---

    # EXAMPLE: git pull

    ('git pull ', r'^\s*(git|va|calme|grille)\s*(tirer|pohl|piscine)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: c'est git pull c

    ('git pull ', r'^\s*git\s*tirer\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git diff ---

    # EXAMPLE: git diff

    ('git diff ', r'^\s*(trousse|git|va|pêche)\s*(diff|profond|tiff|tuv|jus|conseils|va\'s|kittys|dies|die)\s*$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Comparaison avec l'avant-dernier commit

    ('git diff HEAD~1', r'^Comparaison avec pénultième Commettre\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Dernier commit avec diff s

    ('git log -p -1', r'^Dernier Commettre avec Diff\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Spectacles mis en scène mais non engagés dans les modifications

    ('git diff --cached', r'^Spectacles mis en scène (mais pas engagé) changements\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),



    # EXAMPLE: commutateur git

    ('git switch ', r'^\s*(git|va|pêche)\s*(changer|Schmidt)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git pull

    ('git fetch; git pull"', r'^\s*(git|Sapplique|va) (tirer|graisse)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

##################################################################

    # EXAMPLE: demandes de tirage

    ('pull requests', r'^\s*(tirer\s*demandes.demandes?|Pull-over\s*Quête)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: demandes de tirage

    ('pull requests', r'\b(zéro|tirer) demandes.demandes\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

# s'il te plaît, écris-moi car il sera accompagné d'un texte'

    # EXAMPLE: est livré avec du texte

    ('git commit text', r'\b(va viens avec texte)\b', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Prince vedette

    ('feature branch', r'\bFonctionnalité\s*prince\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Supprimer la branche

    ('git branch -d', r'\b(Bifurquer|Prince)\s*supprimer\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Noms des ranchs

    ('Branch Name', r'\bifurquer\s*noms\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Message de validation

    (' Commit', r'\devenir\s*avec\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: venir avec un message

    (' Commit Message', r'\recevoir\s*avec\s*Message\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: nouvelle version

    ('neues Release', r'\nouveau\s*(cachot|Libérer)\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Section des codes

    ('Code Abschnitt', r'\bKot\s*rubriques\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: bouton d'arrêt

    ('StopButton', r'\bstob\s*bouton\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: fait l'éloge du cas

    ('lowerCase', r'\blobs\s*Cas\b', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- statut git ---

    # Cette expression régulière remplace 5 anciennes entrées.

    # EXAMPLE: statut git

    ('git status', r'^\s*(git|va|grille|enfants)\s+(status|État|rendez-vous)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git ajouter . ---

    # EXAMPLE: git ajouter

    ('git add .', r'^\s*(git|va|aller|grille|Kate|décret|avec)\s+(ajouter|loin|à|monter|a fait|papa|a|duo|il)\s*(\.|\point b\b)?\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git commit ---

    # Kate commet un git commit


    # EXAMPLE: Klitschko avec s

    ('git commit ', r'^\s*Klitschko avec\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: Kate s'engage

    ('git commit ', r'^\s*Kate Commettre\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Allez comète

    ('git commit ', r'^\s*Va (comète|à venir|Commettre)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Une comète s

    ('git commit ', r'^\s*UN Comètes\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Allez vous engager

    ('git commit ', r'^\s*Va Commettre\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Allez viens commettre des s

    ('git commit ', r'^\s*Va viens Commettre\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: Va

    ('git commit ', r'^\s*(Va|git|avec) (viens|Comètes|Commettre)\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: comète

    ('commit ', r'\s+comète\s+', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: git

    ('git commit ', r'^\s*(git|avec) viens\s*avec\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: avec quoi s

    ('git commit ', r'^\s*avec quoi\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|va) viens?\s*avec\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Sapplique|va) (comète|viens)\s*$"', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git push ---

    # EXAMPLE: git

    ('git push', r'^\s*(git|va|grille)\s*(buisson|pousser)\s*$', 85, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git pull ---

    # EXAMPLE: git

    ('git pull', r'^\s*(git|va|grille)\s*(pohl|piscine)\s*$', 82, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),
    # EXAMPLE: c'est git pull c

    ('git pull', r'^\s*git\s*tirer\s*$', 80, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # --- git diff ---

    # EXAMPLE: git

    ('git diff', r'^\s*(git|va|pêche)\s*(diff|profond|jus)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Afficher ce qui a été modifié lors des derniers commits

    ('git show HEAD > gitDiff.txt; kate gitDiff.txt', r'^\s*Montrer Quoi dans le dernier Commettre modifié devenu\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


    # EXAMPLE: Critique grogneuse

    ('.gitignore', r'^\s*(critique grognement|critique Noé|Avis|chaton Knorr|critique Knorr)\s*$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: donne à Knorr

    ('.gitignore', r'\b(donne Knorr)\b$', 75, # min_accuracy
      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),

    # EXAMPLE: nouvelle version

    ("alias release_protokoll='gh release list --limit 100 | awk \"{print $1}\" | while read tag; do if [ -n \"$tag\" ]; then echo -e \"\n\n--- RELEASE: $tag ---\n\"; gh release view \"$tag\"; fi; done > all_releases.txt && kate all_releases.txt'", r'\b(sorties\w* protocole\w*|relais\w* Protocoles|tous sorties|sorties\w* exporter\w*|frites Protocoles)\b$', 75,      {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']}),


]





"""
gh release list --limit 100 | awk '{print $1}' | while read tag; do
    if [ -n "$tag" ]; then
        echo -e "\n\n--- RELEASE: $tag ---"
        gh release view "$tag" --json body -q '.body'
    fi
done > all_releases.txt && kate all_releases.txt
"""

