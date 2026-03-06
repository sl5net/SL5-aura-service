# Unificado_sumidero
## configuración.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### La estrategia para Windows (solución alternativa)
En Windows, use **Cables de audio virtuales** en combinación con el **Monitoreo OBS**.

**Configuración:**
1. **Instalación de cable virtual:** (por ejemplo, *VB-Cable*). Se activa el "Unified_Sink" en Windows.
2. **Monitoreo OBS:** In den OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* wählst du das „Virtual Cable“ aus.
3. **Mix erstellen:** Para jede Quelle en OBS (Micrófono, Escritorio) stellst du in den *Erweiterten Audioeigenschaften* „Monitoring und Ausgabe“ ein.
4. **Python:** En la configuración, establezca `AUDIO_INPUT_DEVICE = "CABLE Output"`.

### Analizar
* **Vorteil:** OBS übernimmt das komplette Mixing. No hay complejos completos de Python para Windows únicamente.
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Para los usuarios de Windows, el camino es estable.

**Atención para Windows (PowerShell) según los nombres de cables:**
`Get-AudioDevice-List`
*(Hinweis: Erfordert oft das AudioDeviceCmdlets-Modul).*