# Windows 11 Workflow
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

**The Trigger Mechanism on Windows**

The service is activated by a simple file trigger, making it robust and flexible.

*   **The Service waits** for a specific file to be created: `C:\tmp\sl5_record.trigger`.
*   **Your Hotkey's job** is just to create this empty file.
*   **Recommended Tool:** For Windows, the ideal tool is **AutoHotkey (AHK)**. It's free, open-source, and already part of our toolchain.

**Example AHK Hotkey Script:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```
