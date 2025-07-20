#Requires AutoHotkey v2.0
; type_watcher.ahk (v6.1 - Flag-Based Re-Arming)

#SingleInstance Force

; --- Configuration ---
watchDir := "C:\tmp\sl5_dictation"
logDir := A_ScriptDir "\log"

; --- Global Variables ---
global pBuffer := Buffer(1024 * 16), hDir, pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback, CompletionRoutineProc
global watcherNeedsRearm := false ; <-- The new central flag

; --- Main Script Body ---
DirCreate(watchDir)
DirCreate(logDir)
Log("--- Script Started (v6.1 - Flag-Based Re-Arming) ---")
Log("Watching folder: " . watchDir)

pCallback := ProcessFile
CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)
WatchFolder(watchDir) ; Initial arming

; --- The Main Application Loop ---
Loop {
    ; This will sleep indefinitely until an IOCompletionRoutine runs,
    ; then it will wake up and continue the loop.
    DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)

    ; After waking up, check if the watcher needs to be re-armed.
    if (watcherNeedsRearm) {
        Log("MainLoop: Detected re-arm flag. Calling ReArmWatcher.")
        watcherNeedsRearm := false ; Reset the flag
        ReArmWatcher()
    }
}

Log("--- FATAL: Main loop exited unexpectedly. ---")
ExitApp

; =============================================================================
; LOGGING FUNCTION
; =============================================================================
Log(message) {
    static logFile := logDir "\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch as e {
        MsgBox("CRITICAL LOGGING FAILURE!`n`nCould not write to: " . logFile . "`n`nReason: " . e.Message, "Logging Error", "IconStop")
        ExitApp
    }
}

; =============================================================================
; FILE PROCESSING FUNCTION (REVISED)
; =============================================================================
ProcessFile(filename) {
    if InStr(filename, "tts_output_") {
        Log("ProcessFile: Received target file -> " . filename)
    } else {
        Log("ProcessFile: Ignored non-target file -> " . filename)
        return
    }

    static stabilityDelay := 50
    local fullPath := watchDir "\" . filename

    try {
        if !FileExist(fullPath) {
            return Log("-> File does not exist anymore.")

        }
        size1 := FileGetSize(fullPath), Sleep(stabilityDelay), size2 := FileGetSize(fullPath)
        if (size1 != size2 or size1 = 0) {
            FileDelete(fullPath)
            return Log("-> File is unstable/empty. Deleting.")

        }
        Log("-> File is stable.")
    } catch as e {
        return Log("-> ERROR during stability check: " . e.Message)

    }

    try {
        local content := Trim(FileRead(fullPath, "UTF-8"))
        FileDelete(fullPath)
        if (content != "") {
            Log("--> Sending content: '" . content . "'") ; <-- YOUR REQUESTED CHANGE
            SendText(content)
        } else {
            Log("-> File was empty and deleted.")
        }
    } catch as e {
        Log("-> ERROR during file read/delete: " . e.Message)
    }
}

; =============================================================================
; WATCHER INITIALIZATION
; =============================================================================
WatchFolder(pFolder) {
    global hDir
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 7, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
    if (hDir = -1) {
        local errMsg := "FATAL: Could not watch directory: " . pFolder
        Log(errMsg), MsgBox(errMsg), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

; =============================================================================
; STABLE RE-ARMING FUNCTION
; =============================================================================
ReArmWatcher() { ; No longer needs the (*) parameter
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1

    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)
    local success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", true, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)

    if (success) {
        Log("Arming watcher successful.")
    } else {
        Log("--- WARNING: ReArmWatcher failed! Error: " . A_LastError . ". Flag will be re-checked. ---")
        watcherNeedsRearm := true ; Set flag to retry on next loop iteration
    }
}

; =============================================================================
; BULLETPROOF COMPLETION ROUTINE (REVISED)
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, pCallback, watcherNeedsRearm

    try {
        if (dwErrorCode != 0) {
            Log("--- ERROR in IOCompletionRoutine. Code: " . dwErrorCode)
        } else if (dwNumberOfBytesTransfered > 0) {
            Log("==> Event TRIGGERED!")
            local pCurrent := pBuffer.Ptr
            Loop {
                local NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                local Action := NumGet(pCurrent + 4, "UInt"), FileName := StrGet(pCurrent + 12, NumGet(pCurrent + 8, "UInt") / 2, "UTF-16")
                Log("--> Event data: Action=" . Action . ", FileName=" . FileName)
                if (Action = 1) {
                    pCallback(FileName)

                }
                if (!NextEntryOffset) {
                    break

                }
                pCurrent += NextEntryOffset
            }
        }
    } catch as e {
        Log("--- FATAL ERROR in IOCompletionRoutine: " . e.Message . " ---")
    }

    ; --- The CRITICAL CHANGE ---
    ; Instead of using SetTimer, just set the flag.
    ; The main loop will handle the re-arming.
    watcherNeedsRearm := true
}
