#Requires AutoHotkey v2.0
; type_watcher.ahk (final, correct, event-driven version)

; Verhindert, dass das Skript mehrfach läuft
#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"
filePattern := "tts_output_*.txt"

; --- Hauptteil des Skripts ---
; ERSTELLE das Monitor-Objekt und weise es einer globalen Variable zu.
; Das ist notwendig, damit der Monitor aktiv bleibt.
global monitor := FileChangeMonitor(watchDir, OnFileEvent)
; Setze den Filter für die zu überwachenden Dateien.
monitor.Filter := filePattern
; Starte die Überwachung.
monitor.Start()

; Die Funktion, die bei jedem Datei-Ereignis aufgerufen wird.
OnFileEvent(filename, event)
{
    ; Eine statische Variable ist sauberer als eine globale für diesen Zweck.
    static stabilityDelay := 50

    ; Wir reagieren nur auf 'erstellt' (1) und 'geändert' (3).
    if (event != 1 and event != 3)
        return

        ; --- Prüfung auf Dateistabilität ---
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
            ; Ignorieren, falls die Datei trotz Prüfung gesperrt ist.
        }
}
