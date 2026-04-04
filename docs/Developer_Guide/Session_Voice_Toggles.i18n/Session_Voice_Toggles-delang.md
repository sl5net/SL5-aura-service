# Sitzungs-Audiobearbeitung und Sprachumschaltung

Aura implementiert eine sitzungsbasierte Audioverarbeitungsschleife. Sprachbefehle zur Statusverwaltung sind nur innerhalb einer bestehenden Aufnahmesitzung aktiv.

## Konfiguration
Das sitzungsinterne Verhalten wird gesteuert durch:
`ENABLE_WAKE_WORD = True/False` (in `config/settings.py`)

## Betriebslogik
Im Gegensatz zu einem permanenten Hintergrund-Listener verarbeitet die STT-Engine (Vosk) von Aura Audio nur, wenn eine Aufnahmesitzung extern (z. B. per Hotkey) ausgelöst wurde.

### Der In-Session-Toggle („Teleskop“)
Wenn „ENABLE_WAKE_WORD“ auf **True** gesetzt ist:
1. **Auslöser:** Der Benutzer startet eine Sitzung manuell.
2. **Umschalten:** Wenn Sie während der Sitzung „Teleskop“ sagen, wird zwischen den Zuständen **AKTIV** und **SUSPENDED** umgeschaltet.
3. **Verhalten:** Dadurch kann der Benutzer die Textverarbeitung mithilfe von Sprachbefehlen „anhalten“ und „fortsetzen“, ohne den Audiostream zu beenden.

### Datenschutz und Effizienz
Wenn „ENABLE_WAKE_WORD“ auf **False** gesetzt ist (Standard):
- **STT-Unterdrückung:** Im angehaltenen Zustand werden Aufrufe von „AcceptWaveform“ und „PartialResult“ vollständig übersprungen.
- **Datenschutz:** Es werden keine Audiodaten analysiert, es sei denn, das System befindet sich in einem explizit aktiven Zustand.
- **Ressourcenverwaltung:** Die CPU-Auslastung wird minimiert, indem die neuronale Netzwerkanalyse während der Unterbrechung umgangen wird.

## Latenz und Leistung
- **Sofortige Wiederaufnahme:** Da der „RawInputStream“ während der gesamten Sitzung geöffnet bleibt, hat der Wechsel von SUSPENDED zurück zu ACTIVE **0 ms zusätzliche Latenz**.
- **Schleifen-Timing:** Die Verarbeitungsschleife arbeitet in einem Intervall von ~100 ms („q.get(timeout=0.1)“) und gewährleistet so nahezu sofortige Reaktionszeiten.