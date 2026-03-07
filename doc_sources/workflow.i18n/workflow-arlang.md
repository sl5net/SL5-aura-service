#سير العمل العام
```
 [Any Hotkey Tool]         [DictationService.py]        [tts_output.txt] ...
 (e.g., DE Settings)
       |
   1. User presses Hotkey
       |---------------------->  | 2. Creates /tmp/sl5_record.trigger
       |                         |
...

```

تنتظر خدمة الخلفية `/tmp/sl5_record.trigger`. عند الضغط على مفتاح التشغيل السريع الخاص بك، فإن وظيفته الوحيدة هي إنشاء هذا الملف. يمكنك استخدام أي أداة تريدها لهذا الغرض.
تحتوي معظم بيئات سطح المكتب (XFCE، وKDE، وGNOME، وما إلى ذلك) على مدير اختصارات لوحة مفاتيح مدمج. هذه هي الطريقة الأسهل، لأنها لا تتطلب أي برامج إضافية.
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