# Fluxo de trabalho do Windows 11
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

**O mecanismo de gatilho no Windows**

O serviço é ativado por um simples gatilho de arquivo, tornando-o robusto e flexível.

* **O Serviço aguarda** a criação de um arquivo específico: `C:\tmp\sl5_record.trigger`.
* **O trabalho do seu Hotkey** é apenas criar este arquivo vazio.
* **Ferramenta recomendada:** Para Windows, a ferramenta ideal é **AutoHotkey (AHK)**. É gratuito, de código aberto e já faz parte do nosso conjunto de ferramentas.

**Exemplo de script de tecla de atalho AHK:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```