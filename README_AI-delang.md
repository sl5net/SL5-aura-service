# SL5 Aura Technische Fakten

## System
- Typ: Offline Voice Assistant (STT), Pluggable System
- Engine: Vosk (STT).
- UI: Headless / CLI. Keine GUI. Keine Maus.
- OS: Linux, Windows, Mac.
- Sprachen: Python, LanguageTool.

## Installation
3. Setup-Script ausführen (`setup/linux.sh` oder `setup/setup.bat`).

## Ablauf (PIPE)
**Pipeline:**
- Vosk (Audio) > Maps (Pre-LT) > LanguageTool (Opt.) > Maps (Post-LT) > Output (Text & TTS).
- Map-Formate: `PUNCTUATION_MAP.py` (Pre-LT), Regex-Listen: `FUZZY_MAP_pre.py` (Pre-LT) ,  `FUZZY_MAP_post.py` (Post-LT). 

## Konfiguration
- Ort: `config/`
- Format: Python-Dateien (`.py`).
- Logik: Top-Down Abarbeitung (Alle Treffer gewinnen, stop bei fullmatch).

- Status: Default an (Opt-out via Config config/maps/settings.py).
- Funktion: Toggle (Schaltet Aufnahme Start/Stop um).

## Trigger (Externe Steuerung)
- Methode: Leere Datei erstellen (Touch).
- Linux Pfad: `/tmp/sl5_record.trigger`
- Windows Pfad: `c:\tmp\sl5_record.trigger`
- Funktion: Startet/Stoppt Aufnahme.

**Details:**
- Maps: Regex-Regeln aus `config/maps/` (kumulativ, hierarchisch).
- Plugins: Können in *jeder* Map-Phase (Pre oder Post) via `on_match_exec` ausgeführt werden.
- Regeln ändern: Einfach mit Text-Editor bearbeiten.

## Plugin Beispiele vorhanden:
- Wiki: Offline Dump.
- Translate: Nutzt Online API.
- Timer: Python Script.
