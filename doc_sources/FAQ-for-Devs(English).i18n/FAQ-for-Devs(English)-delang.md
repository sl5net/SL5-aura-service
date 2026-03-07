# Regeln für reguläre Ausdrücke

Wichtig: Bitte wenden Sie die regulären Ausdrücke in der richtigen Reihenfolge an.

Sie müssen zuerst den zusammengesetzten (allgemeineren) regulären Ausdruck verwenden und dann den speziellen Ausdruck anwenden.

Der Grund dafür ist, dass, wenn die kürzere, spezialisierte Regex zuerst ausgeführt wird, sie möglicherweise mit einem Teil der Zeichenfolge übereinstimmt, der für die größere, zusammengesetzte Regex wesentlich ist. Dies würde es für den zusammengesetzten regulären Ausdruck unmöglich machen, später seine Übereinstimmung zu finden.
(S. 20.10.'25 18:37 Mo)

# Linux/Mac

Wenn Sie den Dienst automatisch starten möchten, können Sie Folgendes hinzufügen:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
zum Autostart.

Starten Sie den Dienst nur, wenn eine Internetverbindung besteht:
dann in Settings_local.py einstellen:
SERVICE_START_OPTION = 1


## hinzufügen eingeben
wenn Sie einstellen
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
zu 1 fügt es enter hinzu.

wenn Sie einstellen
tmp/sl5_auto_enter.flag
zu 1 fügt es enter hinzu.

tmp/sl5_auto_enter.flag wird überschrieben, wenn Sie den Dienst starten.
tmp/sl5_auto_enter.flag lässt sich möglicherweise einfacher mit anderen Skripten analysieren und ist möglicherweise etwas schneller zu lesen.

Verwenden Sie zum Deaktivieren andere Nummern
(S. 13.9.'25 16:12 Sa)