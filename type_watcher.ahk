#Requires AutoHotkey v2.0
#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"
filePattern := "tts_output_*.txt"
; Wartezeit in Millisekunden, um zu prüfen, ob eine Datei fertig geschrieben ist.
; Erhöhen, falls sehr große Dateien unvollständig gelesen werden.
stabilityDelay := 30

monitor := FileChangeMonitor(watchDir, OnFileEvent)
monitor.Filter := filePattern
monitor.Start()

OnFileEvent(filename, event)
{
    ; Wir reagieren nur auf 'erstellt' (1) und 'geändert' (3).
    if (event != 1 and event != 3)
        return

        try
        {
            size1 := FileGetSize(filename)
            Sleep(GLOBALS.stabilityDelay)
            size2 := FileGetSize(filename)

            ; size should be stable
            if (size1 != size2 or size1 == 0)
            {
                return
            }
        }
        catch
        {
            ; Wenn die Datei bereits gelöscht wurde, während wir warteten,
            ; ignorieren wir den Fehler und beenden die Funktion.
            return
        }


        ; --- Robuste Verarbeitung der stabilen Datei ---
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
            ; Fängt den seltenen Fall ab, dass die Datei trotz Stabilitäts-
            ; prüfung immer noch gesperrt ist. Ignorieren und auf das
            ; nächste Event warten.
        }
}
