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

# config/maps/plugins/standard_actions/langage_translator/de-DE/FUZZY_MAP_pre.py

import re
from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.

# arrêt de remise de langue



readme = """
'Translate Shell .. is a versatile and powerful command-line translator that leverages the translation services of major providers like

Google Translate,
DeepL, and
Microsoft Translator.

Its design prioritizes ease of use and extensibility, making it an ideal companion for Linux and other Unix-like operating systems'
(10.11.'25 18:58 Mon, https://itsfoss.gitlab.io/post/how-to-use-google-translate-from-commandline-in-linux/ )

Arch-Users may use:
source .venv/bin/activate
pip install --upgrade pip
yay -S translate-shell


here's a list of common language codes you want use:

    en: English
    de: German
    jp: Japanese
    pr-br: Brazilian Portuguese
    fr: French
    es: Spanish
    it: Italian
    pt: European Portuguese
    ru: Russian
    nl: Dutch
    zh-CN: Chinese (Simplified)
    zh-TW: Chinese (Traditional)
    pl: Polish
    tr: Turkish
    sv: Swedish
    da: Danish
    no: Norwegian
    fi: Finnish
    cs: Czech
    hu: Hungarian
    ro: Romanian
    gr: Greek
    th: Thai
    ko: Korean
    ar: Arabic
    he: Hebrew
    hi: Hindi
    id: Indonesian
    ms: Malay

You can find a comprehensive list of language codes in the
ISO 639-1
ISO 15897
standards.

"""


CONFIG_DIR = Path(__file__).parent

nonsense_start_word = r'(?:(à|un|un|un|manger)\s*)?'

# EXAMPLE: Anglais

Englisch = fr'{nonsense_start_word}(Anglais|Anglais\w*|Anglais\w*|enfin|Essuyer|niche|Nimporte lequel|dune manière ou dune autre|rayon.*Gabe|similaire)\b\s*'
# EXAMPLE: Changer

toggleCmd=r'\s*(Changer|Activer|activer|activé|actif|allumer|enregistrement|éteindre|abolir|adieu|arrêt\w*|Arrêt|désactiver|désactiver|éteindre|attention|basculer)\s*'

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # EXAMPLE: Activer l'anglais

    ('en', fr'^{Englisch}{toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Activez le français

    ('fr', fr'^(französisch) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Commutateur thaïlandais

    ('th', fr'^(thaïlandais|Taï|Salut|À) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Commutateur japonais

    ('ja', fr'^(japonais) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Commutateur arabe

    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Commutateur persan

    ('fa', r'^(persan) (Changer|Activer|activer|activé|actif|allumer|désactiver|désactiver|éteindre|attention|basculer)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Commutateur portugais

    ('pt-BR', r'^(Changer|Activer|activer|activé|actif|allumer|désactiver|désactiver|éteindre|attention|basculer) (portugais|portugais|portugais\w*)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Commutateur portugais

    ('pt-BR', r'^(portugais) (activer|activé|actif|un|allumer|abdos\w*|désactiver|éteindre|attention|basculer|danois|double)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Espagne Changer

    ('es', r'^(Espagne|Espagnol|rigide toi|sparr toi) (activer|activé|actif|un|allumer|abdos\w*|désactiver|éteindre|attention|basculer|danois|double)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # bascule afghane

    # EXAMPLE: afghan

    ('Dari', r'^(afghan|Afghanistan|Organique) (activer|activé|actif|un|allumer|abdos\w*|désactiver|éteindre|attention|basculer|danois|double)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # Activer organiquement گرمایش را خاموش کنید (original : « éteindre le chauffage »).



    # EXAMPLE: traduction : désactiver la bascule de désactivation

    ('de', r'^(\w*traduction|chauffage|estimations des revenus) (désactiver|désactiver|éteindre|éteindre|attention|basculer)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # traduction activée et désactivée

    # EXAMPLE: désactiver la traduction

    ('de', r'^(\w*traduction|chauffage|pour le) (mode )? (Changer|Activer|activer|activé|actif|allumer|désactiver|désactiver|éteindre|éteindre|attention|basculer)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: traduction Switch

    ('de', r'^(\w*profession\w*) (mode )? (Changer|Activer|activer|activé|actif|allumer|désactiver|désactiver|éteindre|attention|basculer)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: bascule de traduction

    ('de', fr'^(\w*rayon\w*) (traduction\w*)? {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: bascule de traduction

    ('de', r'^(Changer|Activer|activer|activé|actif|allumer|désactiver|désactiver|éteindre|attention|basculer) (\w*traduire\w*)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Bonne nuit

    ('', r'\b(bien nuit|dormir bien|je aller dans le lit)\b', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),


    # config/maps/plugins/standard_actions/langage_translator/de-DE/FUZZY_MAP_pre.py

    # ANCHOR : La ligne suivante est contrôlée par le script toggle.

    # Il est préférable de désactiver avant d'exécuter des règles d'auto-test telles que : faire correspondre tout à rien. comme : .+ -> ou .* -> ''

    # TRANSLATION_RULE

     ('', r'.+', 5, {'command_flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),

]
