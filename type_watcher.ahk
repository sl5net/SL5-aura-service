#Requires AutoHotkey v2.0
; type_watcher.ahk (FINAL version using a proper event-driven wait loop)

#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Hauptteil des Skripts ---
logDir := A_ScriptDir . "\log"
DirCreate(logDir)
Log("--- Script Started ---")

; Dieser Aufruf blockiert nun und startet die Endlosschleife
WatchFolder(watchDir, ProcessFile)

; Das Skript wird diesen Punkt nie erreichen, es sei denn, WatchFolder bricht ab.
Log("--- FATAL: Watcher loop exited unexpectedly. ---")
ExitApp

; =============================================================================
; LOGGING-FUNKTION
; =============================================================================
Log(message)
{
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
}

; =============================================================================
; CALLBACK-FUNKTION ZUR DATEIVERARBEITUNG
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
; WATCHER-FUNKTION: Das Herzstück mit einer korrekten Event-Loop
; =============================================================================
WatchFolder(pFolder, pCallback)
{
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 3, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
    if (hDir = -1)
    {
        errMsg := "FEHLER: Konnte das Verzeichnis nicht überwachen: " . pFolder
        Log(errMsg), MsgBox(errMsg), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)

    pBuffer := Buffer(1024 * 16)
    pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
    hEvent := DllCall("CreateEvent", "Ptr", 0, "Int", true, "Int", false, "Ptr", 0, "Ptr")
    NumPut("Ptr", hEvent, pOverlapped, A_PtrSize * 2)
    Log("Created and assigned a manual event handle.")

    notifyFilter := 0x1 | 0x10 ; FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE

    ; --- DIE NEUE, KORREKTE ENDLOSSCHLEIFE ---
    Loop
    {
        Log("Arming watcher with ReadDirectoryChangesW and entering wait state...")

        ; "Bewaffne" die Überwachung
        DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", 0)

        ; Warte, bis unser Event signalisiert wird. Das ist ein blockierender Aufruf.
        DllCall("WaitForSingleObject", "Ptr", hEvent, "Int", -1) ; -1 = INFINITE

        Log("Wait finished! Event was signaled. Checking results...")

        dwBytes := 0
        result := DllCall("GetOverlappedResult", "Ptr", hDir, "Ptr", pOverlapped, "UInt*", &dwBytes, "Int", true)

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

                if ((Action = 1 or Action = 3) and InStr(FileName, "tts_output_"))
                {
                    Log("==> MATCH! Calling ProcessFile callback.")
                    pCallback(pFolder . "\" . FileName)
                }

                NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                if !NextEntryOffset
                    break
                    pCurrent += NextEntryOffset
            }
        }
        else
        {
            Log("GetOverlappedResult returned FALSE or 0 bytes. Error: " . A_LastError)
        }

        DllCall("ResetEvent", "Ptr", hEvent) ; Setze das Event für den nächsten Durchlauf zurück
    }
}
