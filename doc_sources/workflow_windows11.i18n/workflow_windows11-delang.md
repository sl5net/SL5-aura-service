# Windows 11-Workflow
```
 [AutoHotkey (AHK)]        [DictationService.py]        [C:\tmp\tts_output.txt]       [TypeWatcher.ahk]       [Active App]
  (Recommended Tool)
       |                         |                          |                             |                     |
   1. User presses Hotkey        |                          |                             |                     |
       |---------------------->  | 2. Creates C:\tmp\sl5_record.trigger                         |                     |
       |                         |                                                        |                     |
       |               (watches for trigger file)                                         |                     |
       |                         | 3. Detects & DELETES trigger file                      |                     |
       |                         |                                                        |                     |
       |                         o 4. Records & Processes (Vosk -> LT)                    |                     |
       |                         |                                                        |                     |
       |                         | 5. Writes final text ------------------------------> o |                     |
       |                         |                          |                             |                     |
       |                         |                          |               (watches for output file)           |
       |                         |                          |                             |                     |
       |                         |                          |                             o <------------------ | 6. Detects & reads file
       |                         |                          |                             |                     |
       |                         |                          |                     [DELETES tts_output.txt]      |
       |                         |                          |                             |                     |
       |                         |                          |                             | 7. Types text ------> o
       |                         |                          |                             |                     |
```

**Der Auslösemechanismus unter Windows**

Der Dienst wird durch einen einfachen Dateitrigger aktiviert, was ihn robust und flexibel macht.

* **Der Dienst wartet** darauf, dass eine bestimmte Datei erstellt wird: „C:\tmp\sl5_record.trigger“.
* **Die Aufgabe Ihres Hotkeys** besteht lediglich darin, diese leere Datei zu erstellen.
* **Empfohlenes Tool:** Für Windows ist **AutoHotkey (AHK)** das ideale Tool. Es ist kostenlos, Open Source und bereits Teil unserer Toolchain.

**Beispiel für ein AHK-Hotkey-Skript:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```