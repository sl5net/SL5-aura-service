# 一般的なワークフロー
```
 [Any Hotkey Tool]         [DictationService.py]        [tts_output.txt] ...
 (e.g., DE Settings)
       |
   1. User presses Hotkey
       |---------------------->  | 2. Creates /tmp/sl5_record.trigger
       |                         |
...

```

バックグラウンド サービスは `/tmp/sl5_record.trigger` を待ちます。ホットキーが押されたときの唯一の仕事は、このファイルを作成することです。これには好きなツールを使用できます。
ほとんどのデスクトップ環境 (XFCE、KDE、GNOME など) には、キーボード ショートカット マネージャーが組み込まれています。これは追加のソフトウェアを必要としないため、最も簡単な方法です。
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