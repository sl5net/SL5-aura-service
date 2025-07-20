#Requires AutoHotkey v2.0
; type_watcher.ahk (v5.1 - Asynchronous Redemption, memset fix)

#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Globale Variablen für die DllCalls ---
global pBuffer := Buffer(1024 * 16)
global hDir
global pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback
global CompletionRoutineProc ; Garantiert die Lebensdauer des Callbacks

; --- Hauptteil des Skripts ---
logDir := A_ScriptDir . "\log"
DirCreate(logDir)
Log("--- Script Started (v5.1 - Asynchronous Redemption Strategy) ---")

pCallback := ProcessFile
CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)

WatchFolder(watchDir)

; --- DER UNZERSTÖRBARE ANKER ---
Loop {
    DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)
}

Log("--- FATAL: Main loop exited unexpectedly. ---"), ExitApp


; =============================================================================
; LOGGING-FUNKTION (Unverändert)
; =============================================================================
Log(message) {
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch { ; Silent fail

    }
}

; =============================================================================
; DATEIVERARBEITUNGS-FUNKTION (Unverändert)
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
            ; SendText(content)
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

    ; Diese Parameter sind für die asynchrone Methode korrekt und haben in den ersten Versuchen funktioniert.
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 3, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")

    if (hDir = -1) {
        errMsg := "FEHLER: Konnte das Verzeichnis nicht überwachen: " . pFolder
        Log(errMsg), MsgBox(errMsg), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

; =============================================================================
; STABILE BEWAFFNUNGS-FUNKTION
; =============================================================================
ReArmWatcher(*) { ; Akzeptiert den optionalen Parameter von SetTimer
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1 | 0x10

    Log("Arming watcher...")
    ; <<< KORREKTUR: Ersetze das fehlerhafte pOverlapped.Fill(0) durch den korrekten DllCall.
    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)

    success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)

    if not success {
        Log("--- WARNING: ReArmWatcher failed! Error: " . A_LastError . ". Retrying in 5 seconds... ---")
        SetTimer ReArmWatcher, -5000
    }
}

; =============================================================================
; KUGELSICHERE COMPLETION ROUTINE
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, pCallback, watchDir

    try {
        if (dwErrorCode != 0) {
            Log("--- ERROR in IOCompletionRoutine. ErrorCode: " . dwErrorCode)
        }
        else if (dwNumberOfBytesTransfered > 0) {
            Log("==> Event TRIGGERED!")
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
                if !NextEntryOffset
                    break
                    pCurrent += NextEntryOffset
            }
        }
        SetTimer ReArmWatcher, -1

    } catch as e {
        Log("--- FATAL ERROR in IOCompletionRoutine: " . e.Message . " ---")
        SetTimer ReArmWatcher, -1
    }
}
