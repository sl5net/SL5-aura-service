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

# config/langagetool_server/maps/de-DE/FUZZY_MAP.py

import re

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - signifie que le premier est le plus important, les règles inférieures peuvent ne pas être lues.

    # EXAMPLE: fait l'éloge du cas

    ('lowerCase', r'\blobs\s*Cas\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Quelques quelques

    ('Manjaro', r'\b(Quelques couple|Moines euro)\b', 75, {'command_flags': re.IGNORECASE}),


# ('.', r'^\s*(dot|pup)\s*$', 82, {'command_flags' : re.IGNORECASE}),





    # EXAMPLE: demandes de tirage

    ('pull requests', r'^\s*(tirer\s*demandes.demandes?|Pull-over\s*Quête)\s*$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: zéro

    ('pull requests', r'\b(zéro|tirer) demandes.demandes\b', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Prince vedette

    ('feature branch', r'\bFonctionnalité\s*prince\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Bifurquer

    ('git branch -d', r'\b(Bifurquer|Prince)\s*supprimer\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Noms des ranchs

    ('Branch Name', r'\bifurquer\s*noms\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: viens avec moi

    (' Commit ', r'\devenir\s*avec\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: viens avec bitkom

    (' Commit ', r'\devenir\s*avec\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    ('git commit ', r'^bitkom avec$', 82,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: venir avec un message

    (' Commit Message', r'\recevoir\s*avec\s*Message\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: nouveau donjon

    ('neues Release', r'\nouveau\s*cachot\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Fèces coupées

    ('Code Abschnitt', r'\bKot\s*rubriques\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: bouton de commande

    ('StopButton', r'\bstob\s*bouton\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: fait l'éloge du cas

    ('lowerCase', r'\blobs\s*Cas\b', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- statut git ---

    # Cette expression régulière remplace 5 anciennes entrées.


    # EXAMPLE: statut git

    ('git status', r'^(glissé|États membres|coup de pied|couine loin|il Status)$', 82,
     {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: statut git

    ('git status', r'^\s*(git|va|grille|enfants)\s+(status|État|au lieu de|stade|rendez-vous)\s*$', 82,  {'command_flags': re.IGNORECASE,'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- git ajouter . ---

    # a lieu

    # EXAMPLE: git ajouter

    ('git add .', r'^\s*(git|va|aller|grille|Kate|décret|avec)\s+(ajouter|à|a fait|papa|a|duo|il)\s*(\.|\point b\b)?\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git commit quelque part au milieu du texte : ---

    # EXAMPLE: git commit

    ('git commit ', r'\b(Va|git|bien|avec) (Commettre)\b\s*', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git commit ---

    # Kate commet un git commit


    # EXAMPLE: Klitschko avec

    ('git commit ', r'^\s*Klitschko avec\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: Kate s'engage

    ('git commit ', r'^\s*Kate Commettre\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Allez comète

    ('git commit ', r'^\s*Va (comète|à venir|correctement|Commettre)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Une comète s

    ('git commit ', r'^\s*UN Comètes\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Allez vous engager

    ('git commit ', r'^\s*Va Commettre\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # EXAMPLE: Allez, venez vous engager

    ('git commit ', r'^\s*Va viens Commettre\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: Va

    ('git commit ', r'^\s*(Va|git|bien|avec) (viens|Comètes|Commettre|Kévin)\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),





    # EXAMPLE: comète

    (' commit ', r'\s+comète\s+', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # EXAMPLE: git

    ('git commit ', r'^\s*(git|avec) viens\s*avec\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: avec quoi

    ('git commit ', r'^\s*avec quoi\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|va) viens?\s*avec\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git

    ('git commit -m "', r'^\s*(git|Sapplique|va) (comète|viens)\s*$"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # Doré viens viens


    # maintenant également en remplacement de ligne :

    # EXAMPLE: git commit

    ('git commit "', r'\b(git|Sapplique|va) (comète|viens|Kubitz)\b\s*"', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),





    # --- git push ---

    # EXAMPLE: git pousser

    ('git push', r'^\s*(git|va|grille)\s*(buisson|frais|pousser|probablement)\s*$', 85, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),



    # --- git pull ---

    # EXAMPLE: git pull

    ('git pull', r'^\s*(git|va|grille)\s*(pohl|piscine)\s*$', 82, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

    # EXAMPLE: git pull

    ('git pull', r'^\s*git\s*tirer\s*$', 80, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),


    # --- git diff ---

    # EXAMPLE: git diff

    ('git diff', r'^\s*(git|va|pêche)\s*(diff|profond|jus)\s*$', 75, {'command_flags': re.IGNORECASE, 'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'gnome-terminal', 'xterm', 'tilix', 'terminator']}),

]
