# Fluxo de trabalho geral
```
 [Any Hotkey Tool]         [DictationService.py]        [tts_output.txt] ...
 (e.g., DE Settings)
       |
   1. User presses Hotkey
       |---------------------->  | 2. Creates /tmp/sl5_record.trigger
       |                         |
...

```

O serviço em segundo plano aguarda um `/tmp/sl5_record.trigger`. Quando sua tecla de atalho é pressionada, sua única tarefa é criar este arquivo. Você pode usar qualquer ferramenta que desejar para isso.
A maioria dos ambientes de desktop (XFCE, KDE, GNOME, etc.) possui um gerenciador de atalhos de teclado integrado. Este é o método mais simples, pois não requer software extra.
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