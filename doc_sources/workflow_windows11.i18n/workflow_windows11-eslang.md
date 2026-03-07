# Flujo de trabajo de Windows 11
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

**El mecanismo de activación en Windows**

El servicio se activa mediante un simple activador de archivo, lo que lo hace robusto y flexible.

* **El Servicio espera** a que se cree un archivo específico: `C:\tmp\sl5_record.trigger`.
* **El trabajo de tu tecla de acceso rápido** es simplemente crear este archivo vacío.
* **Herramienta recomendada:** Para Windows, la herramienta ideal es **AutoHotkey (AHK)**. Es gratuito, de código abierto y ya forma parte de nuestra cadena de herramientas.

**Ejemplo de secuencia de comandos de teclas de acceso rápido AHK:**
```ahk
#Requires AutoHotkey v2.0

; Example: Win + Space hotkey to trigger dictation
#Space::
{
    FileAppend("", "C:\tmp\sl5_record.trigger")
}
```