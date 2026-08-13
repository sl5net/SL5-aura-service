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

# config/maps/plugins/ai/gemini/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702
CONFIG_DIR = p(__file__).parent

_misc_errors = (
    r'(?:région de la Ruhr|logiciel de groupe|UDP\s+sil te plaît|prêt|bébébaye|poupée|jubilé|privilège|'
    r'test|tous les jours|donner\s+trois|donner\s+ton|go\s+données)'
)
_studio_variants = r'(?:étude[ao]\w*|séminaire\w*|style|chaise|capital|aviv|chapiteau|Brême)'
geminiUrl = 'https://aistudio.google.com/prompts/new_chat'

_google_prefix = r'(?:Google|google?|gogol|regarder|regarder[n\s]*|goris|bien|go|balles|Brooke|corail|cool|bien que)'
_gemini_phonetics = (
    r'(?:Gémeaux|Émilie|comités|cheminée|g[\s-]?le mien|minutes à pied|aller\s+avec|donne|jeu|criminel\w*|'
    r'rendez-vous\w*|Jimmy\s*(?:Non|chevalier|poser|nouveau)|Allemagne|féminin|gagnant\w*|'
    r'profit\s+un|ge[mw]\w*|g\s+signifier|g\s+Comment\s+nouveau|séminaire\w*)'
)
_common_metaVERBOSE = {
    'command_flags': re.IGNORECASE | re.VERBOSE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Chrome', r'Courageux', r'FLOU_CARTE_pré', r'Kate'],
    'exclude_windows': [r'élément', r'mastodonte', r'GitHub', r'Claude', r'Google IA'],
}
_common_meta = {
    'command_flags': re.IGNORECASE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Chrome', r'Courageux', r'FLOU_CARTE_pré', r'Kate'],
    'exclude_windows': [r'élément', r'mastodonte', r'GitHub', r'Claude', r'Google IA'],
}
FUZZY_MAP_pre = [

    # EXAMPLE: Bras pour ordinateur portable AI

    ('https://notebooklm.google', r'^carnet de notes (lm|ai|bras)( Google)?$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Recherche profonde par l'IA

    ('https://chat.deepseek.com/', r'^recherche profonde?$', 75, {'command_flags': re.IGNORECASE}),



    # kimi Société chinoise d'IA Particulièrement douée pour : traiter des textes longs




    # EXAMPLE: Chat Kimi avec l'IA

    ('https://www.kimi.com/en/', r'^(ai\s*)?Kimi( chat)?$', 75, {'command_flags': re.IGNORECASE}),



    # EXAMPLE: Google Gémeaux

    (f'{geminiUrl}', r'^(Google Gémeaux|Google va pas|Google minutes à pied|Google stratifié|Google Allemagne|Google Gémeaux anneau|gâteau Gémeaux|Google camille|Google mobile|Google b d|Google gagner|Google déterminer|regarder sil te plaît|uri Gémeaux|Google criminel|Google réduit|Google g moins|Google gagne|Rülke Bible|Google bébé|Google payer sil te plaît|Google go d|Google fil|Google Gémeaux|Google g meunier|Google image|Google tous les jours|Google jeu|Google pesanteur|Google donner le|Google webinaire|Google g b|Google donner|Google donner d|Google sil te plaît|Google donner il|Google g sil te plaît|Google existerait le|Google donne|Gary Hewitt|Google zone|Google piquant|Google va|Gucci bébé|Google commande|par groupe nous demander|correctement sil te plaît|Google g b d|corique son bébé|piaulement cebit|Google vortex d|koppe pesanteur|Google va encore|regarder loin donner d|regarder Oui sil te plaît|coucou ici sil te plaît|cosi bébé|regarder moi sil te plaît|cookies ici sil te plaît|Google jubilé|Google vraiment|Google donner ce|regarder nous sil te plaît|regarder donner elle|regarder donner d|cookies remettre|coucou son bébé|coucou www|grippe aviaire|Google g b jour|astre sil te plaît|Google domaines|regarder nous encore|regarder nous sil te plaît|cocu OMS encore|coucou a répondu|astre bébé|groupe donner|regarder Comment sil te plaît|coucou amour d|coucou loin|googlé son bébé|curry Gémeaux|Google son bébé|concombre son bébé|uwe tissu|Google rendez-vous|Google crédit|coucou Évi d|Ulrike b à travers|Google tout le monde sil te plaît|Google devient|Google g le mien|Google Bible|regarder toi Comment nouveau|DACCORD Jimmy|Oh bien Ginny|uwe g d|Google kiwi|va encore|hôtel donner|collègue encore|Google formé|Google payer jour|Gucci gagner|balles séminaire|regarder Gémeaux|maintenant mais|réno robinet|Google profit|goféminin|Google menu|cube séminaire|Google se prendre daffection pour|Google chaise|Google étude|regarder donne|Google connaissances|hauteur de croissance minutes à pied|regarder donner|par pistolet le mien|regarder gagner|Google rendez-vous un)$', 70, _common_meta),



    # 2. activez cette règle (derrière la première pluie que vous souhaitez optimiser)


    # EXAMPLE: URL des Gémeaux

    (f'{geminiUrl}', rf'''(?ix)
    ^ (?:
        {_gemini_phonetics} |                     # Gemini direkt
        {_misc_errors} |                         # Sonderfehler
        {_google_prefix} \s+ (?:                 # Google + Anhang
            {_gemini_phonetics} |
            {_studio_variants} |
            {_misc_errors} |
            geben\ ihnen\ ein | recht | \w*minarett | dir\ bitte | b[\s-]?day
        )
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

    # EXAMPLE: Studio d'IA

    (f'{geminiUrl}', rf'''(?ix)
    ^ chat\ mit\s+ (?:
        {_gemini_phonetics} |
        chip | Kevin | Boot\ Gaming\ nein
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

]
