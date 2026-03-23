import subprocess
import sys
import time
import re


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


def _tabelle_via_menu():
    _dotool('ctrl+F12')
    # time.sleep(0.3)
    # _dotool('key Return')


def execute(match_data):
    text = match_data.get('original_text', '').strip().lower()

    if re.search(r'tabelle', text):               _dotool('key ctrl+f12')

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
