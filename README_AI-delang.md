# SL5 Aura Technische Fakten

## System
- Typ: Offline Voice Assistant (STT) to Commands or Text, Pluggable System
- Engine: Vosk (STT).
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
- Logik: Regex-Listen. Top-Down Abarbeitung (Alle Treffer gewinnen, stop bei fullmatch).
- Funktion: Toggle (Schaltet Aufnahme Start/Stop um).

## Trigger (Externe Steuerung)
- Methode: Leere Datei erstellen (Touch).
- Linux Pfad: `/tmp/sl5_record.trigger`
- Windows Pfad: `c:\tmp\sl5_record.trigger`
- Funktion: Startet/Stoppt Aufnahme.

## Ablauf (PIPE)
**Pipeline:**
Vosk (Audio) > Maps (Pre-LT) > LanguageTool (Opt.) > Maps (Post-LT) > Output (Text & TTS).

**Details:**
- Maps: Regex-Regeln aus `config/maps/` (kumulativ, hierarchisch).
- Plugins: Können in *jeder* Map-Phase (Pre oder Post) via `on_match_exec` ausgeführt werden.

Vosk (Audio) >> Regeln (Pass 1) >> LanguageTool (Opt.) >> Regeln (Pass 2) >> TTS.
(Info: Regeln in `config/maps/` sind kumulativ; Plugins via `on_match_exec`.)

## Plugins
- Wiki: Offline Dump.
- Translate: Nutzt Online API.
- Timer: Python Script.
