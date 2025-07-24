# General Workflow
```
 [Any Hotkey Tool]         [DictationService.py]        [tts_output.txt] ...
 (e.g., DE Settings)
       |
   1. User presses Hotkey
       |---------------------->  | 2. Creates /tmp/vosk_trigger
       |                         |
...

```

The background service waits for a `/tmp/vosk_trigger`. When your hotkey is pressed, its only job is to create this file. You can use any tool you like for this.
Most desktop environments (XFCE, KDE, GNOME, etc.) have a built-in keyboard shortcut manager. This is the simplest method, as it requires no extra software.
```


 [User/AutoKeyAutoHotKey/..]  [DictationService.py]   [tts_output.txt]        [TypeWatcher]           [Active App]
       |                         |                          |                       |                     |
   1. User presses Hotkey        |                          |                       |                     |
       |---------------------->  | 2. Creates /tmp/vosk_trigger                     |                     |
       |                         |                                                  |                     |
       |               (watches for trigger file)                                   |                     |
       |                         | 3. Detects & DELETES trigger file                |                     |
       |                         |                                                  |                     |
       |                         o 4. Records & Processes (Vosk -> LT)              |                     |
       |                         |                                                  |                     |
       |                         | 5. Writes final text ------------------------> o |                     |
       |                         |                          |                       |                     |
       |                         |                          |               (watches for output file)     |
       |                         |                          |                       |                     |
       |                         |                          |                       o <------------------ | 6. Detects & reads file
       |                         |                          |                       |                     |
       |                         |                          |             [DELETES tts_output.txt]        |
       |                         |                          |                       |                     |
       |                         |                          |                       | 7. Types text ----> o
       |                         |                          |                       |                     |
       
```
