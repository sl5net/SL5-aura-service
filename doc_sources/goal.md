## Goal: The "Dictation Session" Model

### Unser Ziel(german): Die "Diktier-Sitzung"

Ein einziger Trigger startet eine **"Diktier-Sitzung"**, die aus drei Phasen besteht:

1.  **Startphase (Warten auf Sprache):**
    *   Nach dem Trigger lauscht das System.
    *   Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (z.B. 12s).

2.  **Aktivphase (Kontinuierliches Diktieren):**
    *   Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktiven Modus.
    *   Immer wenn VOSK eine Sprechpause erkennt und einen Textblock liefert (z.B. einen Satz), wird dieser Block **sofort** zur Verarbeitung (LanguageTool, etc.) weitergegeben und als Text ausgegeben.
    *   Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3.  **Endphase (Ende der Sitzung):**
    *   Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
        *   Der Nutzer bleibt für die Dauer des `SILENCE_TIMEOUT` (z.B. 1-2s) komplett still.
        *   Der Nutzer stoppt die Sitzung manuell per Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Nutzer eine längere Pause macht oder sie manuell beendet.


### **Goal: The "Dictation Session" Model**

A single trigger initiates a **"Dictation Session"**, which consists of three phases:
1.  **Startup Phase (Waiting for Speech):**
    *   After the trigger, the system starts listening.
    *   If **no speech** is detected, the entire session terminates after the `PRE_RECORDING_TIMEOUT` (e.g., 12s).
2.  **Active Phase (Continuous Dictation):**
    *   As soon as the first speech input is detected, the session switches to active mode.
    *   Whenever VOSK detects a pause and delivers a text chunk (e.g., a sentence), this chunk is **immediately** passed to the processing pipeline (LanguageTool, etc.) and output as text.
    *   The recording continues **seamlessly** in the background, waiting for the next utterance.
3.  **Termination Phase (Ending the Session):**
    *   The entire session terminates only when one of two conditions is met:
        *   The user remains completely silent for the duration of the `SILENCE_TIMEOUT` (e.g., 1-2s).
        *   The user manually stops the session via the trigger.
**In short:** One session, multiple immediate text outputs. The session remains active until the user takes a long pause or manually terminates it.
