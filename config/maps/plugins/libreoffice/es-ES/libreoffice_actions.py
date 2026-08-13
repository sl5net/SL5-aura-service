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

# config/maps/plugins/libreoffice/de-DE/libreoffice_actions.py

from scripts.py.func.get_project_root import get_aura_project_root
import subprocess
import sys
import re


def _dotool(command):
    subprocess.run(['dotool'], input=command, text=True, check=True)

def _via_uno_socket(zeilen=3, spalten=3):
    import importlib.util
    if importlib.util.find_spec('uno') is None:
        raise ImportError("uno nicht gefunden")
    import uno
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.getCurrentComponent()
    text = doc.getText()
    cursor = text.createTextCursor()
    table = doc.createInstance("com.sun.star.text.TextTable")
    table.initialize(zeilen, spalten)
    text.insertTextContent(cursor, table, False)

def _check_kde_hotkey_conflict(shortcut: str) -> bool:
    """Returns True if shortcut is globally bound in KDE."""
    try:
        result = subprocess.run(
            ['qdbus6', 'org.kde.kglobalaccel', '/component/kwin', 'shortcutKeys', shortcut],
            capture_output=True, text=True, timeout=2
        )
        return bool(result.stdout.strip())
    except Exception:
        return False
def execute(match_data):
    SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

    if str(SL5NET_AURA_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(SL5NET_AURA_PROJECT_ROOT))

    from scripts.py.func.audio_manager import speak_inclusive_fallback

    text = match_data.get('original_text', '').strip().lower()

    if re.search(r'tabla', text):
        if _check_kde_hotkey_conflict('Ctrl+F12'):
            speak_inclusive_fallback(
                'Konflikt: Strg F12 ist als globaler Hotkey in KDE belegt. '
                'Bitte in den Systemeinstellungen unter Kurzbefehle entfernen.',
                'de-DE'
            )
        else:
            _dotool('key ctrl+f12')
    # formateo

    elif re.search(r'gordo', text):               _dotool('key ctrl+b')
    elif re.search(r'itálico', text):             _dotool('key ctrl+i')
    elif re.search(r'subestimado', text):           _dotool('key ctrl+u')

    # Encabezamientos

    elif re.search(r'titular.?1|título.?1|título.?1', text): _dotool('key ctrl+1')
    elif re.search(r'titular.?2|título.?2|título.?2', text): _dotool('key ctrl+2')
    elif re.search(r'titular.?3|título.?3|título.?3', text): _dotool('key ctrl+3')
    elif re.search(r'estándar|mas normal?\s*texto', text):          _dotool('key ctrl+0')

    # Editar

    elif re.search(r'atrás|deshacer', text):          _dotool('key ctrl+z')
    elif re.search(r'Copiar', text):             _dotool('key ctrl+c')
    elif re.search(r'separar', text):         _dotool('key ctrl+x')
    elif re.search(r'insertar', text):             _dotool('key ctrl+v')
    elif re.search(r'todo\s*(seleccionar|marca)', text): _dotool('key ctrl+a')
    elif re.search(r'buscar.*reemplazado|reemplazado', text): _dotool('key ctrl+h')

    # archivo

    elif re.search(r'memoria', text):           _dotool('key ctrl+s')
    elif re.search(r'prensa', text):            _dotool('key ctrl+p')
    # elif re.search(r'pdf', texto): _dotool('tecla ctrl+shift+e')


    # Insertar

    elif re.search(r'párrafo|línea|convulsión', text): _dotool('key Return')
    elif re.search(r'paginas.*convulsión|nuevo\s*página', text): _dotool('key ctrl+Return')
    elif re.search(r'comentario|nota', text): _dotool('key ctrl+alt+c')
    elif re.search(r'contenido.*directorio|toc', text): _dotool('key alt+F10')

    # Opinión

    elif re.search(r'navegador', text):          _dotool('key F5')
    elif re.search(r'ortografía|ortografía', text): _dotool('key F7')
    elif re.search(r'macro|macro', text):        _dotool('key alt+F8')
    elif re.search(r'zoom', text):               _dotool('key ctrl+0')

    # Necesitamos detener este hilo porque no queremos que aura trabaje en él. En este lugar todo bien. notario público. mejor uso de excepción. sys.exit(1) también funciona pero no se recomienda

    # return ''# si usamos return '' escribirá el texto original

    raise Exception('no text after replacement')

