# LanguageTool

prüfen:

java -jar C:\tmp\STT\LanguageTool-6.6\languagetool-server.jar --port 8082

# Meine Taste für die Aufnahme funktioniert nicht mehr

Haben sie das Betriebssystem oder den Computer gewechselt?

Zum Beispiel:
Die Taste für Taschenrechner ist auf Ubuntu anders. Das muss bei der Installation von AutoHotkey zum Beispiel beachtet werden.
Am besten einfach eine neue Taste registrieren.

# Das STT schaltet manchmal ab

Am besten versuchen sie zuerst folgendes (Stand: 7.7.'25 13:10 Mon):

## Bei der Verwendung an einem Linux System
```sh
cd ~/projects/py/STT

./type_watcher.sh

./scripts/restart_venv_and_run-server.sh

./keep_live.sh
```sh

Dann sollte das STT nicht mehr abstützen
