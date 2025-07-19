#Requires AutoHotkey v2.0
; type_watcher.ahk (FINAL - New strategy using a Completion Routine)

#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Globale Variablen für die DllCalls ---
global pBuffer := Buffer(1024 * 16)
global hDir
global pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback
global CompletionRoutineProc

; --- Hauptteil des Skripts ---
logDir := A_ScriptDir . "\log"
DirCreate(logDir)
Log("--- Script Started (Completion Routine Strategy) ---")

pCallback := ProcessFile
; <<< KORREKTUR: Den Callback einmalig im globalen Kontext erstellen, um seine Lebensdauer zu garantieren.
CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)

; Starte die Überwachung
WatchFolder(watchDir)

; --- DER NEUE, KORREKTE "ANKER" ---
DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)

Log("--- FATAL: Watcher loop exited unexpectedly. ---")
ExitApp


; =============================================================================
; LOGGING-FUNKTION
; =============================================================================
Log(message) {
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch as e {
        MsgBox("FATAL LOGGING ERROR: " . e.Message . "`n`nMessage was: " . message)
    }
}

; =============================================================================
; DATEIVERARBEITUNGS-FUNKTION (Ihre bewährte Logik)
; =============================================================================
ProcessFile(filename) {
    Log("ProcessFile called for: " . filename)
    static stabilityDelay := 50
    try {
        size1 := FileGetSize(filename)
        Sleep(stabilityDelay)
        size2 := FileGetSize(filename)
        if (size1 != size2 or size1 == 0) {
            Log("-> File is unstable or empty. Skipping.")
            return
        }
        Log("-> File is stable.")
    } catch {
        Log("-> ERROR during stability check.")
        return
    }
    Try {
        content := Trim(FileRead(filename, "UTF-8"))
        FileDelete(filename)
        if (content != "") {
            Log("-> Content found. Sending text.")
            ; SendText(content) ; <<< HINWEIS: Diese Funktion muss noch definiert werden.
        } else {
            Log("-> File was empty. Deleting.")
        }
    } Catch OSError {
        Log("-> ERROR: File was locked.")
    }
}

; =============================================================================
; WATCHER-INITIALISIERUNG
; =============================================================================
WatchFolder(pFolder) {
    global hDir

    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 3, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
    if (hDir = -1) {
        errMsg := "FEHLER: Konnte das Verzeichnis nicht überwachen: " . pFolder
        Log(errMsg), MsgBox(errMsg), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

; =============================================================================
; BEWAFFNUNGS-FUNKTION
; =============================================================================
ReArmWatcher(*) {
    ; <<< KORREKTUR: Verwende die globalen Variablen, erstelle sie hier aber nicht neu.
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1 | 0x10 ; FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE

    Log("Arming watcher with ReadDirectoryChangesW and Completion Routine...")
    success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)

    if not success {
        Log("--- FATAL: ReadDirectoryChangesW failed. Error: " . A_LastError . ". Exiting. ---")
        ExitApp
    }
}

; =============================================================================
; COMPLETION ROUTINE - Diese Funktion wird direkt von WINDOWS aufgerufen!
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, pCallback, watchDir

    try {
        Log("==> IOCompletionRoutine TRIGGERED! ErrorCode: " . dwErrorCode . ", Bytes: " . dwNumberOfBytesTransfered)

        if (dwErrorCode = 0 and dwNumberOfBytesTransfered > 0) {
            pCurrent := pBuffer.Ptr
            Loop {
                Action := NumGet(pCurrent + 4, "UInt")
                FileNameLength := NumGet(pCurrent + 8, "UInt")
                FileName := StrGet(pCurrent + 12, FileNameLength / 2)
                Log("--> Detected Event: Action=" . Action . ", FileName=" . FileName)

                if ((Action = 1 or Action = 3) and InStr(FileName, "tts_output_")) {
                    Log("==> MATCH! Calling ProcessFile callback.")
                    pCallback(watchDir . "\" . FileName)
                }

                NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                if !NextEntryOffset {
                    break
                }
                pCurrent += NextEntryOffset
            }
        }
        else if (dwErrorCode != 0) {
            Log("--- ERROR: Completion Routine received ErrorCode: " . dwErrorCode)
        }

        SetTimer ReArmWatcher, -1

    } catch as e {
        Log("--- FATAL ERROR in IOCompletionRoutine: " . e.Message . " ---")
        SetTimer ReArmWatcher, -1
    }
}
