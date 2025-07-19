#Requires AutoHotkey v2.0
#SingleInstance Force

watchDir := "C:\tmp"
filePattern := "tts_output_*.txt"

FileChangeMonitor(watchDir, OnFileEvent, filePattern)

OnFileEvent(filename, event)
{
    static stabilityDelay := 50

    ; Wir reagieren nur auf 'erstellt' (1) und 'geändert' (3).
    if (event != 1 and event != 3)
        return

        try
        {
            size1 := FileGetSize(filename)
            Sleep(stabilityDelay)
            size2 := FileGetSize(filename)

            if (size1 != size2 or size1 == 0)
            {
                return ; Die Datei wächst noch oder ist leer, wir warten.
            }
        }
        catch
        {
            return ; Datei wurde bereits gelöscht.
        }

        Try
        {
            content := Trim(FileRead(filename, "UTF-8"))
            FileDelete(filename)

            if (content != "")
            {
                SendText(content)
            }
        }
        Catch OSError
        {
            ; Ignorieren
        }
}
