#Requires AutoHotkey v2.0
; type_watcher.ahk

; Verhindert, dass das Skript mehrfach läuft (wie die Lockfile-Logik)
#SingleInstance Force

; --- Konfiguration ---
; Das Skript überwacht dieses Verzeichnis auf Dateien, die dem Muster entsprechen.
watchDir := "C:\tmp"
filePattern := watchDir . "\tts_output_*.txt"

; --- Endlosschleife zum Überwachen ---
Loop
{
    ; Durchsuche das Verzeichnis nach passenden Dateien.
    ; Die Verarbeitung erfolgt alphabetisch. Stelle sicher, dass der Timestamp
    ; im Dateinamen das ermöglicht (z.B. YYYYMMDD_HHMMSS).
    Loop Files, filePattern
    {
        ; A_LoopFileFullPath enthält den Pfad zur gefundenen Datei
        content := Trim(FileRead(A_LoopFileFullPath))
        FileDelete(A_LoopFileFullPath)

        if (content != "")
        {
            SendText(content) ; Zuverlässiger als Send()
        }
    }

    ; Kurze Pause, um CPU-Last zu reduzieren, bevor erneut gesucht wird.
    Sleep 0.02
}
