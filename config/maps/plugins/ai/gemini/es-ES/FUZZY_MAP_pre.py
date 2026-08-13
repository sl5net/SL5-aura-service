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
    r'(?:área del ruhr|software colaborativo|udp\s+por favor|listo|bebebay|Picardias|aniversario|privilegio|'
    r'prueba|cada día|dar\s+tres|dar\s+su|gb\s+datos)'
)
_studio_variants = r'(?:estudiar[ao]\w*|seminario\w*|estilo|silla|capital|aviv|capilla|Brema)'
geminiUrl = 'https://aistudio.google.com/prompts/new_chat'

_google_prefix = r'(?:Google|googlealo?|gogol|mirar|mirar[n\s]*|goris|bien|gb|bolas|brooke|coral|Frío|a pesar de)'
_gemini_phonetics = (
    r'(?:Géminis|emily|comités|caminoée|g[\s-]?mío|minutos a pie|ir\s+con|da|juego de azar|criminal\w*|'
    r'cita\w*|Palanqueta\s*(?:No|caballero|poner|nuevo)|Alemania|femenino|ganador\w*|'
    r'ganancia\s+a|ge[mw]\w*|g\s+significar|g\s+Cómo\s+nuevo|seminario\w*)'
)
_common_metaVERBOSE = {
    'command_flags': re.IGNORECASE | re.VERBOSE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Cromo', r'Corajudo', r'DIFUSO_MAPA_pre', r'kate'],
    'exclude_windows': [r'elemento', r'mastodonte', r'GitHub', r'claudio', r'Google AI'],
}
_common_meta = {
    'command_flags': re.IGNORECASE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Cromo', r'Corajudo', r'DIFUSO_MAPA_pre', r'kate'],
    'exclude_windows': [r'elemento', r'mastodonte', r'GitHub', r'claudio', r'Google AI'],
}
FUZZY_MAP_pre = [

    # EXAMPLE: Brazo de portátil con IA

    ('https://notebooklm.google', r'^computadora portátil (yo|ai|brazo)( Google)?$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Búsqueda profunda de IA

    ('https://chat.deepseek.com/', r'^búsqueda profunda?$', 75, {'command_flags': re.IGNORECASE}),



    # kimi Empresa china de inteligencia artificial Particularmente buena en: procesar textos largos




    # EXAMPLE: Chat de AI Kimi

    ('https://www.kimi.com/en/', r'^(ai\s*)?kimi( charlar)?$', 75, {'command_flags': re.IGNORECASE}),



    # EXAMPLE: google geminis

    (f'{geminiUrl}', r'^(Google Géminis|Google va no|Google minutos a pie|Google laminado|Google Alemania|Google Géminis anillo|pastel Géminis|Google camilla|Google móvil|Google b d|Google ganar|Google determinar|mirar por favor|uri Géminis|Google criminal|Google reducido|Google g menos|Google gana|Rülke Biblia|Google bebé|Google pagar por favor|Google gb d|Google hilo|Google Géminis|Google g molinero|Google imagen|Google cada día|Google juego de azar|Google gravedad|Google dar el|Google seminario web|Google g b|Google dar|Google dar d|Google por favor|Google dar él|Google g por favor|Google existiría el|Google da|gary Hewitt|Google área|Google picante|Google va|gucci bebé|Google dominio|en grupo nosotros preguntar|correctamente por favor|Google g b d|corico su bebé|mirar furtivamente cebit|Google vórtice d|koppe gravedad|Google va de nuevo|mirar lejos dar d|mirar Sí por favor|cuco aquí por favor|cosi bebé|mirar a mí por favor|galletas aquí por favor|Google aniversario|Google en realidad|Google dar este|mirar nosotros por favor|mirar dar ella|mirar dar d|galletas Entregar|cuco su bebé|cuco www|gripe aviar|Google g b día|luminaria por favor|Google áreas|mirar nosotros de nuevo|mirar nosotros por favor|cornudo OMS de nuevo|cuco respondió|luminaria bebé|grupo dar|mirar Cómo por favor|cuco amar d|cuco lejos|buscado en google su bebé|curry Géminis|Google su bebé|pepino su bebé|uwe tejido|Google equipo|Google crédito|cuco Evi d|Ulrike b a través de|Google todos por favor|Google se convierte|Google g mío|Google Biblia|mirar tú Cómo nuevo|DE ACUERDO Palanqueta|Oh bien ginny|uwe g d|Google kiwi|va de nuevo|hotel dar|colega de nuevo|Google formado|Google pagar día|gucci ganar|bolas seminario|mirar Géminis|ahora pero|renovar grifo|Google ganancia|gofemenino|googles menú|cubo seminario|Google encariñarse|Google silla|Google estudiar|mirar da|Google perspectivas|altura de crecimiento minutos a pie|mirar dar|por pistola mío|mirar ganar|Google equipo a)$', 70, _common_meta),



    # 2. activa esta regla (después de la primera lluvia que deseas optimizar)


    # EXAMPLE: geminiUrl

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

    # EXAMPLE: Estudio de IA

    (f'{geminiUrl}', rf'''(?ix)
    ^ chat\ mit\s+ (?:
        {_gemini_phonetics} |
        chip | Kevin | Boot\ Gaming\ nein
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

]
