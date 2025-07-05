#Requires AutoHotkey v2.0
; type_watcher.ahk

filePath := "C:\tmp\tts_output.txt"

Loop
{
    if FileExist(filePath)
    {
        content := FileRead(filePath)
        Send(content)

        ; Lösche die Datei
        FileDelete filePath
    }
    Sleep 1000
}
