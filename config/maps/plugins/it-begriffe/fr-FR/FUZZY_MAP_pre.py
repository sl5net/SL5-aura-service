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

# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py

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


# config/maps/plugins/it-terms/de-DE/FUZZY_MAP_pre.py:17

FUZZY_MAP_pre = [
    # EXAMPLE: déboguerABZ

    ('debugABZxxx', r'déboguerABZ'),  # ← komplett standalone, keine Gruppe

    # Règle de démarrage : Déclenche le groupe 'sandbox_test' au "start sandbox"

    # EXAMPLE: boîte de sta

    ('Sandbox', r'^sta\w* .*boîte.*', 100, {'group_start': 'sandbox_test'}),

    # Règle intérieure 1 : Remplacez « pomme » par « poire » (si disponible)

    # EXAMPLE: pomme

    ('birne', r'pomme'),

    # Règle intérieure 2 : Remplacez « banane » (si présent), sinon « banane » est ajouté !

    # EXAMPLE: banane

    ('banane', r'banane'),

    # Marqueur de fin passif pour 'sandbox_test'

    (None, r'', 100, {'group_end': 'sandbox_test'}),
    (None, r'', 100, {'group_end': 'sandbox_test'}),

    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.



    # EXAMPLE: Fichier JSON


    ('JSON Datei', r'^\b(JSON(\sFichier)?|chasse|Jacen|Jason|errer)\s*(déposer|détail)(\b)$', 80, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Exportation JSON


    ('JSON Export', r'^\b(JSON exporter|Jacen exporter)(\b)$', 80, {'command_flags': re.IGNORECASE}),


    # Essayez-le


    # la chaise liquide

    # EXAMPLE: l'outil linguistique

    # Outil de langue

    # EXAMPLE: selles liquides

    ('das LanguageTool', r'\b(le) (Outil de langue|liquide Chaise)(\b)', 80, {'command_flags': re.IGNORECASE}),
    ('LanguageTool', r'\b(liquide Chaise)(\b)', 80, {'command_flags': re.IGNORECASE}),

    # du lien quels outils

    # EXAMPLE: Outil de langue


    ("des LanguageTool's", r'\b(Outil de langue|des lien w\w+ outils)(\b)', 80, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Manjaro


    ('Manjaro Linux', r'^(Manjaro|quest-ce que je fais|moine|matcha où) (Linux|Caroline\w*)$', 80, {'command_flags': re.IGNORECASE}),

    # Moine CarolinAvec CarolinSi CarolineManjaro Linux

    # EXAMPLE: Linux Manjaro

    ('Linux Manjaro', r'^(Linux) (Manjaro|homme Vérifier|juste jaro|devient jaro|matcha frotter)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Linux Manjaro

    ('Linux Manjaro', r'^(Linux) maman\w*\s*\w*a\s*r[ou]m?$', 80, {'command_flags': re.IGNORECASE}),


    # Moine CarolinAvec CarolinSi CarolineManjaro Linux

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^(Linux|vélux) (Manjaro|matcha|devient jaro|devient jaro|avec jaro)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Linux Manjarovelux

    ('Linux Manjaro', r'^vélux m\w+\s*[ou]$', 80, {'command_flags': re.IGNORECASE}),

    # velux m\w+\s*[ou]


    # Velux Matcha Ru

    # velux avec jaro


    # Match Velux


    # Linux Manjaro Velux fois Karo

    # correspond où Linux




    # EXAMPLE: questions de débat

    ('Debug-Ausgaben', r'^(débat dépense)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: programme chargé

    ('Programm geladen. Viel Spaß', r'^(Programme[m]+ chargé)$', 80, {'command_flags': re.IGNORECASE}),




    # EXAMPLE: Fichier journal

    ('Logdatei', r'^(Fichier journal|dossier de cuisine|enregistrer-déposer)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Fichier journal

    ('Logfile', r'^(\b)(Fichier journal)(\b)$', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: relief

    ('release', r'^(\b)(libérer|relief|libérer|relief|OMS ce)(\b)$', 75, {'command_flags': re.IGNORECASE}),

# Pratiquement chez les femmes

# Rituel à Deibel

# virtuel à Weibel

# Pratiquement à distance

# virtuel en blanc

# Rituel à Weimarvirtuel à Weimar

# Environnement virtuel

# virtuel chez les veuves blanches à WeimarRituel en blanc#Environnement virtuel

# Rituel à DeibelVirtuel à weibelVirtuel à DeibelSera déjà dans le vin

# ce sera déjà dans le vin, ce sera difficile au chaud

# devient difficile dans une économie chaude à Weimar économie à Weimar Environnement virtuel

# veuf en blanc avec

# Les païens connecteront chacun une femme virtuelle. Ce sera à Deibel

# Bachelorette DeibelVirtuel en courVirtuel en tourbillonnant Sangliers dans les pièces Environnement virtuel Titan est utilisé ici dans un environnement rituel

# virtuel en blancvirtuel dans les chambres

#

    # EXAMPLE: Virtuel

    ('Virtual environment', r'\b(Virtuel|virtuel|veuve\w*|veuf|devient déjà|devient difficile|entreprise|sanglier)\w* (dans |blanc |dans le )?(femme|blanc|weima|métal|blanc|chaud|blanc avec|tourbillon|clair|preuves|portefeuille)\w*\b', 75, {'command_flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
    }),


# Le titane est utilisé ici dans un virtuel en blanc

# Environnement virtuel Titan se connectera ici dans un environnement rituel

# Biden est ici confondu avec une femme virtuelle

# Le titane est utilisé chez chaque femme de veuve

# Titan le fera, ici repose une personne non, les deux ici seront l'oint de ta veuve pour devenir tous les deux ici l'onction de ta veuve sera à qui stupide

# Biden est ici confondu avec une femme virtuelle

# Tous deux seront rejoints ici dans une balade pour le corps

# Le titane est utilisé ici chez une femme virtuelle

# Titan sera à Weibel

# Les deux sont utilisés ici dans un cas

# De plus, une entrée virtuelle avec est utilisée ici

# Chaque veuve doit utiliser sa femme

# Le titane est utilisé ici dans un métal blanc virtuel

# Les temps se connecteront ici chez une veuve à Weimar

# les temps se connecteront ici chez une veuve à Weimar

# Échec iciSkaterTitan sera jamais utilisé chez un veuf avec

# Le titane sera jamais utilisé chez un veuf en blanc

# Times est utilisé ici chez un sanglier chez la femelle

# ützensagTitan est utilisé ici dans un environnement rituel


    # EXAMPLE: Brighton

    ('Python', r'^(\b)(B2026-0131-2125à droite|large déjà|Parachute|fouet)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Les deux sont utilisés ici dans un environnement virtuel

    ('Python wird hier in einer Virtual environment verwendet', r'^(les deux devient ici dans un Virtuel environnement également utilisé|Les deux devient ici dans un devient pour le automne utilisé|En outre devient ici dans un virtuel dans à avec utilisé|Prise devient nimporte qui veuve devient femme utiliser|titane devient ici dans un virtuel dans femme utilisé|les deux devient ici dans un virtuel dans blanc également utilisé)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: sdf b octets charme b

    ('PyCharm', r'^sdf(\b)(octets charme)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: d pâle

    ('default', r'^(\b)(d pâle)(\b)$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Pénétrer

    ('String', r'^(\b)(Pénétrer)(\b)$', 75, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Fèces coupées

    ('Code Abschnitt', r'\bKot\s*rubriques\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: fait l'éloge du cas

    ('lowerCase', r'\blobs\s*Cas\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: bouton de commande

    ('StopButton', r'\bstob\s*bouton\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: fait l'éloge du cas

    ('lowerCase', r'\blobs\s*Cas\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Clé automatique

    ('AutoKey', r'\bVoiture\s*k\w+\b', 82, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 0 après JC

    ('0 A.D.', r'\ou zewa d\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: 0 jeu après JC

    ('0 A.D. spiel', r'\ou zewa d jeu\W*\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: 0 jeu après JC

    ('GitHub SL5', r'\github il sont 5\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: guerre x

    ('regex', r'\b(guerre x|rekik|Micro x|meule x|Récapitulatifs)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),

    # EXAMPLE: processus d'image

    ('Build Prozess', r'\image processus\b', 82, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: source ouverte

    ('opensource', r'\boopensource\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: tuyau

    ('|', r'\b(tuyau|tuyau symbole|payé symbole|conduire symbole|Paypal symbole|dynamisme|préparation Simba|conduire Simba|Paypal Simba)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: tuyau

    ('|', r'\b(tuyau|tuyau|payé|conduire|Paypal|dynamisme|préparation|conduire|Paypal) (symbole|Simba|simple|simple|miroiter|Carte SIM)\b', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: à

    ('@', r'\b(à|éd) (symbole|Simba|simple|simple|miroiter|Carte SIM|shampooing|gros mot|Signe)\b', 75, {'command_flags': re.IGNORECASE}),
# Ed Shampoo, ma chérie se plaignait

# HiPaypalSymbole payantPepSymbole fémininSymbole TreibPythonSymbole PaypalFemme rôtie SimbaFemalePaypal Simbafeit SchimpfTribst simpleVeit SchimmelPep shimmer

# Snacks chez SIMPaypal SIMHalf SIMPep simple||Préparer des cookies


 # Logfile-Duden Logfile-Duden Logfile-Logfile atteint vers le nord Logfile-Logfile Logfile-Logfile Modifications Relief Vernissage Crédit Le crédit établit Qui ceci Edit Qui ceci





]



