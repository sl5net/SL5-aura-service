#Requires AutoHotkey v2.0
; type_watcher.ahk (final, correct, persistent version)

; Verhindert, dass das Skript mehrfach läuft
#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"
filePattern := "tts_output_*.txt"

; --- Hauptteil des Skripts ---
; Erstelle das Monitor-Objekt.
monitor := FileChangeMonitor(watchDir, OnFileEvent)
monitor.Filter := filePattern
monitor.Start()

; --- DER ENTSCHEIDENDE FIX (Dank Ihrer Recherche) ---
; Wir setzen einen Timer. Die reine Existenz dieses Timers verhindert,
; dass sich das Skript von selbst beendet. Es bleibt aktiv und wartet
; auf die Events vom FileChangeMonitor.
SetTimer(KeepAlive, 10000) ; Rufe alle 10 Sek. eine leere Funktion auf.

return ; Beendet den "auto-execute" Teil des Skripts explizit.

; Diese Funktion tut nichts. Sie ist nur das Ziel für den Timer.
KeepAlive()
{
}

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
