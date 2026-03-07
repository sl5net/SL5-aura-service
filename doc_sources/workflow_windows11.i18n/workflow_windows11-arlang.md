# سير العمل في ويندوز 11
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

           **آلية التشغيل على نظام التشغيل Windows**

يتم تنشيط الخدمة من خلال مشغل ملف بسيط، مما يجعلها قوية ومرنة.

* **تنتظر الخدمة** حتى يتم إنشاء ملف محدد: `C:\tmp\sl5_record.trigger`.
* **مهمة مفتاح التشغيل السريع الخاص بك** هي فقط إنشاء هذا الملف الفارغ.
* **الأداة الموصى بها:** بالنسبة لنظام التشغيل Windows، الأداة المثالية هي **AutoHotkey (AHK)**. إنه مجاني ومفتوح المصدر، وهو بالفعل جزء من سلسلة أدواتنا.

                                              **مثال لنص AHK Hotkey:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```