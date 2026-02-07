# Müll-Abfuhr Erinnerungs-Service (Aura Plugin)

Dieses Tool automatisiert die Erinnerung an Abfalltermine für Wannweil, basierend auf dem offiziellen Abfallkalender-PDF.

## Funktionen
- **PDF-Parsing**: Liest Termine direkt aus der `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Nutzt `notify-send` für visuelle Alarme unter Manjaro.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (ideal, wenn das Handy verlegt ist).
- **Sicherheits-Check**: Warnt aktiv, wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt.

## Installation & Voraussetzungen
1. **System-Pakete** (Manjaro):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten** (im Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## Automatisierung (Systemd)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute nach dem Systemstart, ob am Folgetag Müll abgeholt wird.

**Service-Datei:** 
~/.config/systemd/user/trash_check.service

**Timer-Datei:** `
~/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Empfehlungen für den Jahreswechsel
1. Neues PDF von der Gemeinde Wannweil herunterladen.
2. Die Datei im Ordner `config/maps/plugins/wannweil/de-DE/` ersetzen.
3. Der Service erkennt das neue Jahr automatisch am Dateinamen.
4. Falls das PDF fehlt oder veraltet ist, sendet das System eine tägliche Fehlermeldung.

## Manueller Test
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
```

