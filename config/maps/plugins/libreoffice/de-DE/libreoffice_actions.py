# config/maps/plugins/libreoffice/de-DE/libreoffice_actions.py
import subprocess
import sys
import re
import platform
from pathlib import Path


def _dotool(command):
    subprocess.run(['dotool'], input=command, text=True)

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
    TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
    PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))

    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.py.func.audio_manager import speak_inclusive_fallback

    text = match_data.get('original_text', '').strip().lower()

    if re.search(r'tabelle', text):
        if _check_kde_hotkey_conflict('Ctrl+F12'):
            speak_inclusive_fallback(
                'Konflikt: Strg F12 ist als globaler Hotkey in KDE belegt. '
                'Bitte in den Systemeinstellungen unter Kurzbefehle entfernen.',
                'de-DE'
            )
        else:
            _dotool('key ctrl+f12')
    # Formatierung
    elif re.search(r'fett', text):               _dotool('key ctrl+b')
    elif re.search(r'kursiv', text):             _dotool('key ctrl+i')
    elif re.search(r'unterstr', text):           _dotool('key ctrl+u')

    # Überschriften
    elif re.search(r'überschrift.?1|heading.?1|titel.?1', text): _dotool('key ctrl+1')
    elif re.search(r'überschrift.?2|heading.?2|titel.?2', text): _dotool('key ctrl+2')
    elif re.search(r'überschrift.?3|heading.?3|titel.?3', text): _dotool('key ctrl+3')
    elif re.search(r'standard|normaler?\s*text', text):          _dotool('key ctrl+0')

    # Bearbeiten
    elif re.search(r'rück|undo', text):          _dotool('key ctrl+z')
    elif re.search(r'kopier', text):             _dotool('key ctrl+c')
    elif re.search(r'ausschneid', text):         _dotool('key ctrl+x')
    elif re.search(r'einfüg', text):             _dotool('key ctrl+v')
    elif re.search(r'alles\s*(auswähl|markier)', text): _dotool('key ctrl+a')
    elif re.search(r'such.*ersetz|ersetz', text): _dotool('key ctrl+h')

    # Datei
    elif re.search(r'speicher', text):           _dotool('key ctrl+s')
    elif re.search(r'drucken', text):            _dotool('key ctrl+p')
    # elif re.search(r'pdf', text):                _dotool('key ctrl+shift+e')

    # Einfügen
    elif re.search(r'absatz|zeile|umbruch', text): _dotool('key Return')
    elif re.search(r'seiten.*umbruch|neue\s*seite', text): _dotool('key ctrl+Return')
    elif re.search(r'kommentar|anmerkung', text): _dotool('key ctrl+alt+c')
    elif re.search(r'inhalts.*verzeichnis|toc', text): _dotool('key alt+F10')

    # Ansicht
    elif re.search(r'navigator', text):          _dotool('key F5')
    elif re.search(r'rechtschreib|spelling', text): _dotool('key F7')
    elif re.search(r'makro|macro', text):        _dotool('key alt+F8')
    elif re.search(r'zoom', text):               _dotool('key ctrl+0')

    sys.exit(1) # we need stoü this thread becouse we dont want any work on it by aura. at this place all good. np.
    #return '' # if we use return '' it will write the original text
