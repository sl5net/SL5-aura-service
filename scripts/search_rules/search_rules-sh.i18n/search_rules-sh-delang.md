Zusätzlich zu den vielen Suchmöglichkeiten gibt es in Ihrer Entwicklungsumgebung wahrscheinlich eine Volltextsuche. Sie können außerdem Folgendes verwenden:

scripts/search_rules/search_rules.sh

Dies ermöglicht Ihnen die Suche in den vorhandenen Karten oder im Quellcode oder in der Dokumentation. und dann kannst du den Frieden, den du gefunden hast, in deinem Lieblingseditor öffnen oder auf Github öffnen oder … bitte konfiguriere das Skript so, wie du es brauchst.

MAPS_DIR ist über Positionsargumente oder Umgebungsvariablen konfigurierbar

Das Skript behält seine fest codierte Standardeinstellung bei, lässt jedoch Überschreibungen zu:

- Priorität: 1) erster Positionsparameter ($1), 2) vorhandene MAPS_DIR-Umgebungsvariable,
3) hartcodierter Standardwert „$SL5NET_AURA_PROJECT_ROOT/config/maps“.
– Verbessert die Flexibilität für CI, lokale Überschreibungen und Tests, ohne das Skript bearbeiten zu müssen.
– Fügt Anführungszeichen und eine Überprüfung der Verzeichnisexistenz hinzu, um frühzeitig fehlzuschlagen, wenn der Pfad ungültig ist.

Beispielverwendung:
- ./search_rules.sh verwendet die Standardeinstellung
- ./search_rules.sh ./docs verwendet den angegebenen Pfad
- MAPS_DIR=/env/maps ./search_rules.sh

Dadurch wird die Abwärtskompatibilität gewahrt und gleichzeitig die Konfiguration explizit gemacht.

Es gibt auch eine Version für Windows-PC (in diesem Ordner), die etwas weniger kann: search_rules.ps1


(s, 28.3.'26 23:07 Sa)