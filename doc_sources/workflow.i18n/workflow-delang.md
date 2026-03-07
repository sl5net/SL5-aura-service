# Allgemeiner Arbeitsablauf
```
 [Any Hotkey Tool]         [DictationService.py]        [tts_output.txt] ...
 (e.g., DE Settings)
       |
   1. User presses Hotkey
       |---------------------->  | 2. Creates /tmp/sl5_record.trigger
       |                         |
...

```

Der Hintergrunddienst wartet auf einen „/tmp/sl5_record.trigger“. Wenn Ihr Hotkey gedrückt wird, besteht seine einzige Aufgabe darin, diese Datei zu erstellen. Sie können hierfür jedes beliebige Werkzeug verwenden.
Die meisten Desktop-Umgebungen (XFCE, KDE, GNOME usw.) verfügen über einen integrierten Tastaturkürzel-Manager. Dies ist die einfachste Methode, da keine zusätzliche Software erforderlich ist.
```


 [User/AutoKeyAutoHotKey/..]  [DictationService.py]   [tts_output.txt]        [TypeWatcher]           [Active App]
       |                         |                          |                       |                     |
   1. User presses Hotkey        |                          |                       |                     |
       |---------------------->  | 2. Creates /tmp/sl5_record.trigger                     |                     |
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