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


## Kann nicht auf Mikrofon zugreifen

App-Berechtigungen prüfen (Windows 10/11):

    Gehen Sie zu Einstellungen > Datenschutz und Sicherheit > Mikrofon.

    Stellen Sie sicher, dass der "Mikrofonzugriff" und "Zulassen, dass Apps auf Ihr Mikrofon zugreifen" EINgeschaltet ist.

    Wichtig: Stellen Sie sicher, dass auch "Zulassen, dass Desktop-Apps(Python) auf Ihr Mikrofon zugreifen" EINgeschaltet ist (da Python in der Regel als Desktop-App läuft).
    
    Vermutlich unterstert Eintrag bei "Datenschutz und Sicherheit"

Geräteneustart: Manchmal hilft einfach ein Neustart des Computers, um blockierte Ressourcen freizugeben.

## Editor für Window?

Notedpadd++ (Tastenkombination 192 und 193 bitte löschen)
Bitte im Menü > Ansicht > Automatischer Zeilenumbuch
einschallten

Für Python wird gerne PyCharm, z.B. Comunity Edition verwendet.

Für vele Sprachen, auch AutoHotkey, Studio Code.

Empfolenen extension: AHK++ (AutoHotkey Plus Plus)

## Empfolenen für Window?

Installation von :

- https://www.autohotkey.com/ -> https://www.autohotkey.com/download/ahk-v2.exe
- Notedpadd++ https://notepad-plus-plus.org/downloads/ (Tastenkombination 192 und 193 bitte löschen)
Bitte im Menü > Ansicht > "Automatischer Zeilenumbuch" einschallten



## Wie sehe ich ob das Mikrofon unter Windows 11 an oder aus ist?

Es ist auch sehr gut an dem Mikrofon Symbol zu sehen, wann das Mikrofon einschaltet, und wann es wieder von alleine ausschaltet



