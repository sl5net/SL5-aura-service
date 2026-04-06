# Erste Schritte unter Windows

## Schritt 1: Führen Sie das Setup aus
Doppelklicken Sie auf „setup/windows11_setup_with_ahk_copyq.bat“.
- Klicken Sie mit der rechten Maustaste → „Als Administrator ausführen“, wenn Sie dazu aufgefordert werden.
– Das Skript installiert Python, AutoHotkey v2, CopyQ und lädt die Sprachmodelle herunter (~4 GB).
- Dies dauert etwa 8-10 Minuten.

## Schritt 2: Aura starten
Doppelklicken Sie im Projektordner auf „start_aura.bat“.
Sie sollten einen Startton hören – Aura ist bereit.

**Es ist nichts passiert?** Überprüfen Sie das Protokoll:
log\aura_engine.log

## Schritt 3: Konfigurieren Sie Ihren Hotkey
Das Setup installiert CopyQ automatisch. So lösen Sie das Diktat aus:
1. Öffnen Sie CopyQ → Befehle → Befehl hinzufügen
2. Stellen Sie den Befehl ein auf:
cmd /c echo. > C:\tmp\sl5_record.trigger
3. Weisen Sie eine globale Tastenkombination zu (z. B. „F9“)

## Schritt 4: Erstes Diktat
1. Klicken Sie in ein beliebiges Textfeld
2. Drücken Sie Ihren Hotkey – warten Sie auf die Benachrichtigung „Listening…“.
3. Sagen Sie „Hallo Welt“
4. Drücken Sie den Hotkey erneut – der Text erscheint

## Schritt 5: Sprachbefehle finden
Sagen Sie: **„Aura-Suche“** – ein Fenster mit allen verfügbaren Regeln wird geöffnet.

## Fehlerbehebung
| Symptom | Fix |
|---|---|
| Kein Startton | Überprüfen Sie „log\aura_engine.log“ |
| Hotkey macht nichts | Überprüfen Sie, ob „C:\tmp\sl5_record.trigger“ erstellt wurde |
| Text nicht eingegeben | Überprüfen Sie, ob „type_watcher.ahk“ im Task-Manager | ausgeführt wird
| Absturz beim Start | Führen Sie das Setup erneut als Administrator | aus

> Vollständige Fehlerbehebung: [TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-delang.md)