# LanguageTool

prüfen:

java -jar C:\tmp\STT\LanguageTool-6.6\lingualtool-server.jar --port 8082

#Mein Geschmack für die Aufnahme funktioniert nicht mehr

Haben Sie das Betriebssystem oder den Computer ausgetauscht?

Zum Beispiel:
Der Geschmack für Taschenrechner ist auf Ubuntu anders. Das muss bei der Installation von AutoHotkey zum Beispiel beachtet werden.
Am besten einfach einen neuen Geschmack registrieren.

# Das STT schaltet manchmal ab

Am besten versuchen sie zuerst folgendes (Stand: 7.7.25 13:10 Mo):

## Bei der Verwendung an einem Linux-System
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

Stellen Sie sicher, dass der „Mikrofonzugriff“ und „Zulassen, dass Apps auf Ihr Mikrofon zugreifen“ EINgeschaltet ist.

Wichtig: Stellen Sie sicher, dass auch „Zulassen, dass Desktop-Apps (Python) auf Ihr Mikrofon zugreifen“ EINgeschaltet ist (da Python in der Regel als Desktop-App läuft).
  
Vermutlich unterstert Eintrag bei „Datenschutz und Sicherheit“


## Editor für Windows?

Notedpadd++ (Tastenkombination 192 und 193 bitte löschen)
Bitte im Menü > Ansicht > Automatischer Zeilenumbruch
einschallten

Für Python wird gerne PyCharm verwendet, z.B. Community Edition verwendet.

Für verschiedene Sprachen, auch AutoHotkey, Studio Code.

Empfohlene Erweiterung: AHK++ (AutoHotkey Plus Plus)

## Empfolenen für Fenster?

Installation von:

- https://github.com/sl5net/SL5-aura-service/archive/refs/tags/v0.12.0.1.zip
Installationsanleitung (Kurzfassung)
Öffnen Sie die PowerShell mit Administratorrechten.
Führen Sie das Setup-Skript windows11_setup.bat aus dem Projektordner mit PowerShell und Administratorrechten aus.
Wichtig: NICHT per Rechtsklick auf die Datei windows11_setup.bat im Explorer und Auswahl von „Als Administrator ausführen“.
Weil muss aus dem Projektordner ausgeführt werden.
  
- https://www.autohotkey.com/ -> https://www.autohotkey.com/download/ahk-v2.exe

- Notedpadd++ https://notepad-plus-plus.org/downloads/ (Tastenkombination 192 und 193 bitte löschen)
Bitte im Menü > Ansicht > „Automatischer Zeilenumbruch“ einschalten

Viel Spaß beim Bearbeiten der:
01_koan_erste_schritte 03_koan_schwierige_namen 05_koan_such_beispiel   
02_koan_listen 04_koan_kleine_helfer 06_koan_wikipedia_suche ...  



## Wie sehe ich, ob das Mikrofon unter Windows 11 an oder aus ist?

Es ist auch sehr gut, das Mikrofon-Symbol zu sehen, wann das Mikrofon einschaltet, und wann es wieder von alleine ausschaltet