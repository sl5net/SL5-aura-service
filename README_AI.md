# SL5 Aura Technische Fakten

## System
- Typ: Offline Voice Assistant (STT) to Commands or Text, Pluggable System
- UI: Headless / CLI. Keine GUI. Keine Maus.
- OS: Linux (Arch/Manjaro), Windows, Mac.
- Sprachen: Python (Hauptlogik), Bash.

## Installation
1. Download ZIP von GitHub https://github.com/sl5net/Vosk-System-Listener/archive/master.zip 
2. Entpacken.
3. Setup-Script ausführen (`setup/manjaro_arch_setup.sh` oder `setup/setup.bat`).
4. Dauer: ~15 Min (Download 4GB Modelle).

## Konfiguration
- Ort: `config/maps/plugins/`
- Format: Python-Dateien (`FUZZY_MAP_pre.py`).
- Logik: Regex-Listen. Top-Down Abarbeitung.
- Reload: Automatisch bei Dateiänderung.

## Trigger (Externe Steuerung)
- Methode: Leere Datei erstellen (Touch).
- Linux Pfad: `/tmp/sl5_record.trigger`
- Windows Pfad: `c:\tmp\sl5_record.trigger`
- Funktion: Startet/Stoppt Aufnahme.

## Plugins
- Wiki: Offline Dump.
- Translate: Nutzt Online API.
- Timer: Python Script.
