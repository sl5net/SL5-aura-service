> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../goal.md).*

## Goal: The "Dictation Session" Model

### Our goal(german): The "dictation session"

A single trigger starts a **"dictation session"** consisting of three phases:

1.  **Start phase (waiting for speech):**
    *   After the trigger, the system listens.
    *   If there is no voice input, the entire session ends after `PRE_RECORDING_TIMEOUT` (e.g. 12s).

2.  **Active phase (continuous dictation):**
    *   Once the first voice input is recognized, the session switches to active mode.
    *   Whenever VOSK detects a speech pause and delivers a text block (e.g. a sentence), this block is passed on **immediately** for processing (LanguageTool, etc.) and output as text.
    *   Meanwhile, the recording continues **seamlessly**. The sitting is waiting for the next sentence.

3.  **End phase (end of session):**
    *   The entire session ends only if one of these two conditions is met:
        *   The user remains completely silent for the duration of the `SPEECH_PAUSE_TIMEOUT` (e.g. 1-2s).
        *   The user stops the session manually by trigger.

**In summary:** One session, many instant text issues. The session remains active until the user takes a longer break or ends it manually.


### **Goal: The "Dictation Session" Model * *

A single trigger initiates a **"Dictation Session"**, which consists of three phases:
1.  **Startup Phase (Waiting for Speech):**
    *   After the trigger, the system starts listening.
    *   If **no speech** is detected, the entire session terminates after the `PRE_RECORDING_TIMEOUT` (e.g., 12s).
2.  Active Phase (Continuous Dictation):
    *   As soon as the first speech input is detected, the session switches to active mode.
    *   Whenever VOSK detects a pause and delivers a text chunk (e.g., a sentence), this chunk is **immediately** passed to the processing pipeline (LanguageTool, etc.) and output as text.
    *   The recording continues **seamlessly** in the background, waiting for the next utterance.
3.  Ending phase (Ending the session):
    *   The entire session terminates only when one of two conditions is met:
        *   The user remains completely silent for the duration of the `SPEECH_PAUSE_TIMEOUT` (e.g., 1-2s).
        *   The user manually stops the session via the trigger.
**In short:** One session, multiple immediate text outputs. The session remains active until the user takes a long pause or manually terminates it.
