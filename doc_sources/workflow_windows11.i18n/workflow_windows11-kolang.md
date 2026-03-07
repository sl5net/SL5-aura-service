# 윈도우 11 워크플로
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

**Windows의 트리거 메커니즘**

이 서비스는 간단한 파일 트리거로 활성화되므로 강력하고 유연합니다.

* **서비스는 특정 파일 `C:\tmp\sl5_record.trigger`가 생성될 때까지 기다립니다**.
* **단축키의 역할**은 이 빈 파일을 만드는 것뿐입니다.
* **권장 도구:** Windows의 경우 이상적인 도구는 **AutoHotkey(AHK)**입니다. 이는 무료이며 오픈 소스이며 이미 툴체인의 일부입니다.

**AHK 단축키 스크립트 예:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```