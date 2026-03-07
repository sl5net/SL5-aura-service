## Ziel: Das Modell „Diktiersitzung“.

### Unser Ziel(deutsch): Die "Diktier-Sitzung"

Ein einziger Trigger startet eine **"Diktier-Sitzung"**, die aus drei Phasen besteht:

1. **Startphase (Warten auf Sprache):**
* Nach dem Trigger startet das System.
* Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (z.B. 12s).

2. **Aktivphase (Kontinuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktiven Modus.
* Immer wenn VOSK eine Sprechpause erkennt und einen Textblock liefert (z.B. einen Satz), wird dieser Block **sofort** zur Verarbeitung (LanguageTool, etc.) weitergegeben und als Text ausgegeben.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3. **Endphase (Ende der Sitzung):**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) komplett still.
* Der Nutzer stoppt die Sitzung manuell per Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Nutzer eine längere Pause macht oder sie manuell beendet.


### **Ziel: Das Modell „Diktiersitzung“**

Ein einzelner Auslöser initiiert eine **„Diktiersitzung“**, die aus drei Phasen besteht:
1. **Startphase (Warten auf Rede):**
* Nach dem Auslösen beginnt das System mit dem Abhören.
* Wenn **keine Sprache** erkannt wird, wird die gesamte Sitzung nach dem „PRE_RECORDING_TIMEOUT“ (z. B. 12 Sekunden) beendet.
2. **Aktive Phase (kontinuierliches Diktat):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktiven Modus.
* Immer wenn VOSK eine Pause erkennt und einen Textblock (z. B. einen Satz) liefert, wird dieser Block **sofort** an die Verarbeitungspipeline (LanguageTool usw.) übergeben und als Text ausgegeben.
* Die Aufnahme läuft **nahtlos** im Hintergrund weiter und wartet auf die nächste Äußerung.
3. **Beendigungsphase (Beenden der Sitzung):**
* Die gesamte Sitzung wird nur beendet, wenn eine von zwei Bedingungen erfüllt ist:
* Der Benutzer bleibt für die Dauer des „SPEECH_PAUSE_TIMEOUT“ (z. B. 1-2 Sekunden) völlig stumm.
* Der Benutzer stoppt die Sitzung manuell über den Auslöser.
**Kurz gesagt:** Eine Sitzung, mehrere sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Benutzer eine längere Pause einlegt oder sie manuell beendet.