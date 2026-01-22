# config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'flags': re.IGNORECASE}),
]


"""
Bitte schreiben Sie ein Wort in die erste Zeile vor den Anführungstrichen.

Lernziel:

Automatische Fehlerbehebung in Map-Plugins (z.B. NameError für nicht definierte Variablen)
Umwandlung von "bare words" in gültige Tuples
Header-Cleanup (Dubletten entfernen, Pfade aktualisieren)



Beispiel für einen anderen Helfen der beim Schreiben hilft.

LanguageTool ( https://languagetool.org/ )

Bitte öffnen Sie das Fenster und diktieren Text in der Formular-Feld.


Hier sind die Methoden, um auf Windows 11 zu prüfen, ob der LanguageTool im Hintegrund läuft:

http://localhost:8082/v2/languages


Erfolg: Du siehst eine JSON-Liste mit unterstützten Sprachen.

netstat -ano | findstr 8082

Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%languagetool%'" | Select-Object ProcessId, CommandLine

Per Browser (Funktionstest)
Öffne diese URL im Browser:

http://localhost:8082/v2/languages

Erfolg: Du siehst eine JSON-Liste mit unterstützten Sprachen.


"""
