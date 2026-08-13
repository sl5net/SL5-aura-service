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

# config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.

# parada de entrega de idiomas



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

nonsense_start_word = r'(?:(a|a|uno|a|comer)\s*)?'

# EXAMPLE: inglés

Englisch = fr'{nonsense_start_word}(inglés|Inglés\w*|inglés\w*|finalmente|Limpiar|nicho|Cualquier|de alguna manera|habló.*gabe|similar)\b\s*'
# EXAMPLE: Cambiar

toggleCmd=r'\s*(Cambiar|Activar|activar|activado|activo|encender|registrarse|desconectar|abolir|despedida|detener\w*|Detener|desactivar|desactivar|apagar|Estar atento|palanca)\s*'

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


    # EXAMPLE: Activar inglés

    ('en', fr'^{Englisch}{toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Activa el francés

    ('fr', fr'^(französisch) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: interruptor tailandés

    ('th', fr'^(tailandés|tai|Hola|En) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Interruptor japonés

    ('ja', fr'^(japonés) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Cambio árabe

    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Interruptor persa

    ('fa', r'^(persa) (Cambiar|Activar|activar|activado|activo|encender|desactivar|desactivar|apagar|Estar atento|palanca)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Cambio portugués

    ('pt-BR', r'^(Cambiar|Activar|activar|activado|activo|encender|desactivar|desactivar|apagar|Estar atento|palanca) (portugués|portugués|portugués\w*)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Cambio portugués

    ('pt-BR', r'^(portugués) (activar|activado|activo|a|encender|abdominales\w*|desactivar|apagar|Estar atento|palanca|perro danés|doble)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: España Cambiar

    ('es', r'^(España|Español|rígido tú|sparr tú) (activar|activado|activo|a|encender|abdominales\w*|desactivar|apagar|Estar atento|palanca|perro danés|doble)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # palanca afgana

    # EXAMPLE: afgano

    ('Dari', r'^(afgano|Afganistán|Orgánico) (activar|activado|activo|a|encender|abdominales\w*|desactivar|apagar|Estar atento|palanca|perro danés|doble)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # Activar orgánicamente گرمایش را خاموش کنید (original: 'apagar la calefacción').



    # EXAMPLE: traducción: apagar desactivar alternar

    ('de', r'^(\w*traducción|calefacción|estimaciones de ganancias) (desactivar|desactivar|apagar|desconectar|Estar atento|palanca)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # traducción encendido apagado

    # EXAMPLE: desactivar la traducción

    ('de', r'^(\w*traducción|calefacción|para el) (modo )? (Cambiar|Activar|activar|activado|activo|encender|desactivar|desactivar|apagar|desconectar|Estar atento|palanca)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: interruptor de traducción

    ('de', r'^(\w*ocupación\w*) (modo )? (Cambiar|Activar|activar|activado|activo|encender|desactivar|desactivar|apagar|Estar atento|palanca)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: alternar traducción

    ('de', fr'^(\w*habló\w*) (traducción\w*)? {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: alternar traducción

    ('de', r'^(Cambiar|Activar|activar|activado|activo|encender|desactivar|desactivar|apagar|Estar atento|palanca) (\w*traducir\w*)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Buenas noches

    ('', r'\b(bien noche|dormir bien|I ir en el cama)\b', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),


    # config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py

    # ANCLA: La siguiente línea está controlada por el script de alternancia.

    # Es mejor desactivarlo antes de ejecutar reglas de autoevaluación como: hacer coincidir todo con nada. como: .+ -> o .* -> ''

    # REGLA_TRADUCCIÓN

     # ('', r'.+', 5, {'command_flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),


]
