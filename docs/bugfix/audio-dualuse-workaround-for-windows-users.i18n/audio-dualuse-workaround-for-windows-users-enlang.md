> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../audio-dualuse-workaround-for-windows-users.md).*

#  Unified_Sink
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP'
The strategy for Windows (Workaround)
On Windows, **Virtual uses Audio Cables** in combination with **OBS monitoring**.

**The setup:**
1.  **Install Virtual Cable:** (e.g. *VB-Cable*). It acts as your “Unified Sink” on Windows.
2.  **OBS Monitoring:** In the OBS settings under *Audio -> Advanced -> Monitoring device* select the "Virtual Cable".
3.  **Create a mix:* For each source in OBS (Mic, Desktop), set to "Monitoring and Output" in the *Advanced Audio Properties*.
4.  **Python:** In the settings you set `AUDIO_INPUT_DEVICE = "CABLE Output"`.

### Analysis
*   **Advantage:** OBS handles the complete mixing. No complex Python changes required for Windows.
*   **Disadvantage:** The user must keep OBS running in the background.

For Windows users, that would be the most stable way.

**Command for Windows (PowerShell) to search for the cable name:**
`Get-AudioDevice -List`
*(Note: Often requires the AudioDeviceCmdlets module).*

