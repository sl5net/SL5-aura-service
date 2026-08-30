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

import re
import subprocess
import sys

from scripts.py.func.get_project_root import get_aura_project_root


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

    if re.search(r'tabel', text):
        if _check_kde_hotkey_conflict('Ctrl+F12'):
            speak_inclusive_fallback(
                'Konflikt: Strg F12 ist als globaler Hotkey in KDE belegt. '
                'Bitte in den Systemeinstellungen unter Kurzbefehle entfernen.',
                'de-DE'
            )
        else:
            _dotool('key ctrl+f12')
    # formatting

    elif re.search(r'fat', text):               _dotool('key ctrl+b')
    elif re.search(r'italic', text):             _dotool('key ctrl+i')
    elif re.search(r'understated', text):           _dotool('key ctrl+u')

    # Headings

    elif re.search(r'headline.?1|heading.?1|title.?1', text): _dotool('key ctrl+1')
    elif re.search(r'headline.?2|heading.?2|title.?2', text): _dotool('key ctrl+2')
    elif re.search(r'headline.?3|heading.?3|title.?3', text): _dotool('key ctrl+3')
    elif re.search(r'standard|more normal?\s*text', text):          _dotool('key ctrl+0')

    # Edit

    elif re.search(r'back|undo', text):          _dotool('key ctrl+z')
    elif re.search(r'copy', text):             _dotool('key ctrl+c')
    elif re.search(r'cut out', text):         _dotool('key ctrl+x')
    elif re.search(r'insert', text):             _dotool('key ctrl+v')
    elif re.search(r'everything\s*(select|mark)', text): _dotool('key ctrl+a')
    elif re.search(r'search.*replaced|replaced', text): _dotool('key ctrl+h')

    # file

    elif re.search(r'memory', text):           _dotool('key ctrl+s')
    elif re.search(r'press', text):            _dotool('key ctrl+p')
    # elif re.search(r'pdf', text): _dotool('key ctrl+shift+e')


    # Insert

    elif re.search(r'paragraph|line|upheaval', text): _dotool('key Return')
    elif re.search(r'pages.*upheaval|new\s*page', text): _dotool('key ctrl+Return')
    elif re.search(r'comment|note', text): _dotool('key ctrl+alt+c')
    elif re.search(r'content.*directory|toc', text): _dotool('key alt+F10')

    # Opinion

    elif re.search(r'navigator', text):          _dotool('key F5')
    elif re.search(r'spelling|spelling', text): _dotool('key F7')
    elif re.search(r'macro|macro', text):        _dotool('key alt+F8')
    elif re.search(r'zoom', text):               _dotool('key ctrl+0')

    # we need stop this thread because we don't want any work on it by aura. at this place all good. np. better use Exception. sys.exit(1) also works but not recommended

    # return '' # if we use return '' it will write the original text

    raise Exception('no text after replacement')

