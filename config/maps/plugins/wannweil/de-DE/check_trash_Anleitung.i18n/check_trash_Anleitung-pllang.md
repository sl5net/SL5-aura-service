# Müll-Abfuhr Erinnerungs-Service (wtyczka Aura)

Dieses Tool automatisiert die Erinnerung and Abfalltermine für Wannweil, podstawowa wersja auf dem offiziellen Abfallkalender-PDF.

## Funkcje
- **PDF-Parsing**: Liest Termine direkt aus der `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Powiadomienie-wysłanie dla wizualnego alarmu dla Manjaro.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (idealny, wenn das Handy verlegt ist).
- **Sicherheits-Check**: Warnt aktiv, wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt.

## Instalacja i sprawdzanie
1. **Pakete systemowe** (Manjaro):
__KOD_BLOKU_0__
2. **Python-Abhängigkeiten** (w Aura-Venv):
__KOD_BLOKU_1__

## Automatyzacja (systemowa)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute nach dem Systemstart, ob am Folgetag Müll abgeholt wird.

**Data serwisu:**
~/.config/systemd/user/trash_check.service

**Data timera:** `
~/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren:
__KOD_BLOKU_2__

## Empfehlungen für den Jahreswechsel
1. Neues PDF von der Gemeinde Wannweil herunterladen.
2. Die Datei im Ordner `config/maps/plugins/wannweil/de-DE/` ersetzen.
3. Der Service erkennt das neue Jahr automatisch am Dateinamen.
4. Falls das PDF fehlt lub veraltet ist, sendet das System eine tägliche Fehlermeldung.

## Test Manuellera
__KOD_BLOKU_3__
__KOD_BLOKU_4__