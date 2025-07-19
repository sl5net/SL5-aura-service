#Requires AutoHotkey v2.0
; type_watcher.ahk (A robust, simplified DllCall version with DETAILED LOGGING)

#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Hauptteil des Skripts ---
; Erstelle das Log-Verzeichnis, falls es nicht existiert
logDir := A_ScriptDir . "\log"
DirCreate(logDir)
Log("--- Script Started ---")

WatchFolder(watchDir, ProcessFile)
Log("Watcher initialized. Waiting for file events...")
return

; =============================================================================
; LOGGING-FUNKTION: Schreibt eine Nachricht mit Zeitstempel in die Log-Datei.
; =============================================================================
Log(message)
{
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
}

; =============================================================================
; CALLBACK-FUNKTION: Wird aufgerufen, um eine Datei zu verarbeiten.
; =============================================================================
ProcessFile(filename)
{
    Log("Processing file: " . filename)
    static stabilityDelay := 50

    try
    {
        size1 := FileGetSize(filename)
        Sleep(stabilityDelay)
        size2 := FileGetSize(filename)
        if (size1 != size2 or size1 == 0)
        {
            Log("-> File is unstable or empty. Skipping for now. Size1: " . size1 . ", Size2: " . size2)
            return
        }
        Log("-> File is stable.")
    }
    catch
    {
        Log("-> ERROR during stability check (file might have been deleted).")
        return
    }

    Try
    {
        content := Trim(FileRead(filename, "UTF-8"))
        FileDelete(filename)
        if (content != "")
        {
            Log("-> Content found. Sending text and deleting file.")
            SendText(content)
        }
        else
        {
            Log("-> File was empty. Deleting file.")
        }
    }
    Catch OSError
    {
        Log("-> ERROR: File was locked during read/delete. Will retry on next event.")
    }
}

; =============================================================================
; WATCHER-FUNKTION: Das Herzstück, das die Windows API direkt nutzt.
; =============================================================================
WatchFolder(pFolder, pCallback)
{
    static hDir, pBuffer, pOverlapped

    ; Windows API Konstanten
    static FILE_NOTIFY_CHANGE_FILE_NAME := 0x1
    static FILE_NOTIFY_CHANGE_LAST_WRITE := 0x10 ; WICHTIG: Wir lauschen jetzt auch auf Schreibänderungen.
    static FILE_ACTION_ADDED := 1
    static FILE_ACTION_MODIFIED := 3

    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 3, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")

    if (hDir = -1)
    {
        errMsg := "FEHLER: Konnte das Verzeichnis nicht überwachen: " . pFolder
        Log(errMsg)
        MsgBox(errMsg)
        ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)

    pBuffer := Buffer(1024 * 16)
    pOverlapped := Buffer(A_PtrSize * 2 + 8)

    ; Starte die Überwachung. WICHTIG: Wir überwachen jetzt auch Schreibzugriffe.
    notifyFilter := FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE
    DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", 0)

    SetTimer(CheckChanges, 200)
    Log("Timer set. Initial ReadDirectoryChangesW call completed.")

    CheckChanges()
    {
        dwBytes := 0
        ; Prüfe, ob die Operation abgeschlossen ist
        result := DllCall("GetOverlappedResult", "Ptr", hDir, "Ptr", pOverlapped, "UInt*", &dwBytes, "Int", false)

        if (result and dwBytes)
        {
            Log("GetOverlappedResult returned TRUE with " . dwBytes . " bytes. Processing...")
            pCurrent := pBuffer.Ptr
            Loop
            {
                Action := NumGet(pCurrent + 4, "UInt")
                FileNameLength := NumGet(pCurrent + 8, "UInt")
                FileName := StrGet(pCurrent + 12, FileNameLength / 2)

                Log("--> Detected Event: Action=" . Action . ", FileName=" . FileName)

                ; Wir reagieren jetzt auf HINZUGEFÜGT (1) und GEÄNDERT (3)
                if ((Action = FILE_ACTION_ADDED or Action = FILE_ACTION_MODIFIED) and InStr(FileName, "tts_output_"))
                {
                    Log("==> MATCH! Calling ProcessFile callback.")
                    pCallback(pFolder . "\" . FileName)
                }

                NextEntryOffset := NumGet(pCurrent, "UInt")
                if !NextEntryOffset
                    break
                    pCurrent += NextEntryOffset
            }

            ; Starte die Überwachung erneut für die nächsten Änderungen.
            Log("Re-arming the watcher with ReadDirectoryChangesW.")
            DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", 0)
        }
    }
}
