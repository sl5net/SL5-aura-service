#  Unified_Sink 
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Die Strategie für Windows (Workaround)
Unter Windows nutzt **Virtual Audio Cables** in Kombination mit dem **OBS-Monitoring**.

**Das Setup:**
1.  **Virtual Cable installieren:** (z. B. *VB-Cable*). Es fungiert als dein „Unified_Sink“ auf Windows.
2.  **OBS Monitoring:** In den OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* wählst du das „Virtual Cable“ aus.
3.  **Mix erstellen:** Für jede Quelle in OBS (Mic, Desktop) stellst du in den *Erweiterten Audioeigenschaften* „Monitoring und Ausgabe“ ein.
4.  **Python:** In den Settings setzt du `AUDIO_INPUT_DEVICE = "CABLE Output"`.

### Analyse
*   **Vorteil:** OBS übernimmt das komplette Mixing. Keine komplexen Python-Änderungen für Windows nötig.
*   **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Für Windows-User wäre das der stabilste Weg. 

**Befehl für Windows (PowerShell) zum Suchen des Cable-Namens:**
`Get-AudioDevice -List`
*(Hinweis: Erfordert oft das AudioDeviceCmdlets-Modul).*

