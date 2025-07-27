# File: scripts/py/func/handle_trigger.py
"""
**Unser Ziel(german): Die "Diktier-Sitzung"**

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
"""

import threading, time, vosk

from .guess_lt_language_from_model import guess_lt_language_from_model
from .notify import notify
from .process_text_in_background import process_text_in_background
from .transcribe_audio_with_feedback import transcribe_audio_with_feedback

from .prioritize_model import prioritize_model


from config.settings import SAMPLE_RATE, SUSPICIOUS_TIME_WINDOW, SUSPICIOUS_THRESHOLD, \
    PRE_RECORDING_TIMEOUT, SILENCE_TIMEOUT


def handle_trigger(
        logger,
        loaded_models,
        active_threads,
        suspicious_events,
        project_root,
        TMP_DIR,
        recording_time,
        active_lt_url
):

    if not loaded_models:
        logger.error("Trigger ignored: No models are loaded, likely due to low memory.")
        notify("STT-error", "no models loaded (less memory). recording ignored.")
        return
    logger.info(f"TRIGGER DETECTED! Active threads: {len(active_threads)}")
    model_name_file = project_root / "config/model_name.txt"
    last_used_file = project_root / "config/model_name_lastused.txt"
    found_key = None  # Initialize found_key

    try:
        target_model_name = model_name_file.read_text().strip()
        if not target_model_name: raise FileNotFoundError("model_name.txt is empty")
        # last_used_file.write_text(target_model_name)
    except FileNotFoundError as e:
        logger.warning(f"Could not read target model ('{e}'). Using first available as fallback.")
        found_key = list(loaded_models.keys())[0]
        selected_model = loaded_models[found_key]
        target_model_name = f"fallback-model-{found_key}"
    else:
        # --- ROBUSTNESS-fallback: search language-key ---
        selected_model = None
        for key in loaded_models.keys():
            # search "-de-" or "-en-"
            if f"-{key}-" in target_model_name:
                selected_model = loaded_models[key]
                found_key = key
                logger.info(f"Language key '{key}' found in '{target_model_name}'. Selecting model.")
                break  # key is found

        # Fallback
        if not selected_model:
            logger.error(f"No matching pre-loaded model found for '{target_model_name}'. Falling back.")
            found_key = list(loaded_models.keys())[0]
            selected_model = loaded_models[found_key]
            target_model_name = f"fallback-model-{found_key}"
        # --- end extra robustness  ---

    last_used_model_name = last_used_file.read_text().strip()

    if last_used_model_name != target_model_name:
        prioritize_model(logger, loaded_models, found_key)

    last_used_file.write_text(target_model_name)

    lt_language = guess_lt_language_from_model(target_model_name)
    logger.info(f"Using model for lang '{lt_language}'.")

    recognizer = vosk.KaldiRecognizer(selected_model, SAMPLE_RATE)

    if len(suspicious_events) == 0:
        silence_timout = PRE_RECORDING_TIMEOUT
        logger.info(f"silence_timout now set to = PRE_RECORDING_TIMEOUT: '{PRE_RECORDING_TIMEOUT}' ")
    else:
        silence_timout = SILENCE_TIMEOUT

    # --- MODIFIED: Process the stream of text chunks from the generator ---
    text_chunk_iterator = transcribe_audio_with_feedback(logger, recognizer, lt_language, silence_timout)

    for text_chunk in text_chunk_iterator:
        # 2. proof "strange" Events for each chunk
        if not text_chunk.strip() or len(text_chunk.split()) < 1:
            suspicious_events.append(time.time())

        # Start background processing for each valid chunk immediately
        if text_chunk.strip():
            logger.info(f"Starting background processing for chunk: '{text_chunk[:30]}...'")
            thread = threading.Thread(target=process_text_in_background,
                                      args=(logger, lt_language, text_chunk, TMP_DIR,
                                            time.time(), active_lt_url))  # Use current time
            thread.start()
            active_threads.append(thread)

    # Clean up suspicious events after the session ends
    now = time.time()
    suspicious_events = [t for t in suspicious_events if now - t < SUSPICIOUS_TIME_WINDOW]

    if len(suspicious_events) >= SUSPICIOUS_THRESHOLD:
        message = f"Recordings are often ({SUSPICIOUS_THRESHOLD}) very short. Adjust SILENCE_TIMEOUT?"
        notify(f"Tip: Short recordings detected", message, "normal")
        suspicious_events.clear()  # Reset after notification
