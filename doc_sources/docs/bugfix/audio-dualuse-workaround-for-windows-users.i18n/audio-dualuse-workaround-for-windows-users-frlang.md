# Unified_Sink
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### La stratégie pour Windows (solution de contournement)
Sous Windows, utilisez **Câbles audio virtuels** en combinaison avec **OBS-Monitoring**.

**La configuration :**
1. **Installation de câbles virtuels :** (par exemple *VB-Cable*). Il est utilisé comme « Unified_Sink » sur Windows.
2. **Surveillance OBS :** Dans l'installation OBS sous *Audio -> Erweitert -> Monitoring-Gerät*, vous trouverez le « câble virtuel » au-dessus.
3. **Mix ersstellen:** Pour chaque source dans OBS (Mic, Desktop), vous trouverez dans les *Erweiterten Audioeigenschaften* « Monitoring et Ausgabe » un.
4. **Python :** Dans les paramètres, définissez `AUDIO_INPUT_DEVICE = "CABLE Output"`.

### Analyser
* **Vorteil:** OBS übernimmt das komplette Mixing. Il existe de nombreuses applications Python complexes pour Windows.
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Pour les utilisateurs Windows, le chemin de stabilité est disponible.

**Recommandation pour Windows (PowerShell) pour les noms de câbles :**
`Get-AudioDevice -Liste`
*(En anglais : utilisé souvent le module AudioDeviceCmdlets).*