#Requires AutoHotkey v2.0
; type_watcher.ahk (final, robust DllCall version)

; Verhindert, dass das Skript mehrfach läuft
#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Hauptteil des Skripts ---
; Starte die Überwachung des Verzeichnisses.
WatchFolder(watchDir, ProcessFile)
return ; Beendet den auto-execute-Teil

; -----------------------------------------------------------------------------
; CALLBACK-FUNKTION: Diese Funktion wird aufgerufen, wenn eine Datei erstellt wird.
; -----------------------------------------------------------------------------
ProcessFile(filename)
{
    static stabilityDelay := 50

    try
    {
        ; Prüfung auf Dateistabilität
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

; -----------------------------------------------------------------------------
; WATCHER-FUNKTION: Das Herzstück, das die Windows API direkt nutzt.
; Basierend auf der von Ihnen gefundenen Low-Level-Methode.
; -----------------------------------------------------------------------------
WatchFolder(pFolder, pCallback)
{
    static hDir, pBuffer, pOverlapped

    ; Erstelle einen Handle für das zu überwachende Verzeichnis.
    hDir := DllCall("CreateFile", "Str", pFolder
    , "UInt", 0x1 ; FILE_LIST_DIRECTORY
    , "UInt", 0x3 ; FILE_SHARE_READ | FILE_SHARE_WRITE
    , "Ptr", 0
    , "UInt", 0x3 ; OPEN_EXISTING
    , "UInt", 0x40000000 | 0x02000000 ; FILE_FLAG_OVERLAPPED | FILE_FLAG_BACKUP_SEMANTICS
    , "Ptr", 0, "Ptr")

    if (hDir = -1)
    {
        MsgBox("Fehler: Konnte das Verzeichnis nicht öffnen: " . pFolder)
        return
    }

    ; Allokiere Speicher für die Informationen, die wir vom OS erhalten.
    pBuffer := Buffer(1024 * 64)
    pOverlapped := Buffer(A_PtrSize * 2 + 8)

    ; Starte den ersten Lese-Vorgang, um die Überwachung zu beginnen.
    DllCall("ReadDirectoryChangesW"
    , "Ptr", hDir
    , "Ptr", pBuffer
    , "UInt", pBuffer.Size
    , "Int", true ; bWatchSubtree
    , "UInt", 0x1 ; FILE_NOTIFY_CHANGE_FILE_NAME
    , "Ptr", 0
    , "Ptr", pOverlapped
    , "Ptr", 0)

    ; Setze einen Timer, der regelmäßig prüft, ob Änderungen aufgetreten sind.
    ; Das ist der "Anker", der das Skript am Leben erhält.
    SetTimer(CheckChanges, 200)

    CheckChanges() ; Führe die Prüfung einmal sofort aus.
    {
        ; Diese Funktion wird vom Timer aufgerufen.
        dwBytes := 0
        if (DllCall("GetOverlappedResult", "Ptr", hDir, "Ptr", pOverlapped, "UInt*", &dwBytes, "Int", false))
        {
            pCurrent := pBuffer
            Loop
            {
                Action := NumGet(pCurrent, 4, "UInt")
                FileNameLength := NumGet(pCurrent, 8, "UInt")
                FileName := StrGet(pCurrent.Ptr + 12, FileNameLength / 2)

                ; Wir interessieren uns nur für neu erstellte Dateien (Action = 1)
                if (Action = 1 and RegExMatch(FileName, "i)^tts_output_.*\.txt$"))
                {
                    ; Rufe die Callback-Funktion mit dem vollen Pfad auf.
                    pCallback(pFolder . "\" . FileName)
                }

                NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                if (!NextEntryOffset)
                    break
                    pCurrent.Ptr += NextEntryOffset
            }

            ; Starte den nächsten Lese-Vorgang, um die Überwachung neu zu "bewaffnen".
            DllCall("ReadDirectoryChangesW"
            , "Ptr", hDir
            , "Ptr", pBuffer
            , "UInt", pBuffer.Size
            , "Int", true
            , "UInt", 0x1
            , "Ptr", 0
            , "Ptr", pOverlapped
            , "Ptr", 0)
        }
    }
}
