#Requires AutoHotkey v2.0
; type_watcher.ahk (final, correct version with persistence)

#Persistent

; Verhindert, dass das Skript mehrfach läuft
#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"
filePattern := "tts_output_*.txt"

; --- Hauptteil des Skripts ---
; Erstelle das Monitor-Objekt und weise es einer Variable zu.
; Dank #Persistent bleibt diese Variable und das Objekt jetzt aktiv.
monitor := FileChangeMonitor(watchDir, OnFileEvent)
monitor.Filter := filePattern
monitor.Start()

; Die Funktion, die bei jedem Datei-Ereignis aufgerufen wird.
OnFileEvent(filename, event)
{
    static stabilityDelay := 50

    if (event != 1 and event != 3)
        return

        try
        {
            size1 := FileGetSize(filename)
            Sleep(stabilityDelay)
            size2 := FileGetSize(filename)

            if (size1 != size2 or size1 == 0)
                return
        }
        catch
        {
            return
        }

        Try
        {
            content := Trim(FileRead(filename, "UTF-8"))
            FileDelete(filename)

            if (content != "")
                SendText(content)
        }
        Catch OSError
        {
            ; Ignorieren
        }
}
