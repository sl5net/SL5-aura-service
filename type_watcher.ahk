#Requires AutoHotkey v2.0
; type_watcher.ahk (v6.0 - Back to Basics)

#SingleInstance Force

; --- Configuration ---
watchDir := "C:\tmp\sl5_dictation"
logDir := A_ScriptDir "\log"

; --- Global Variables ---
global pBuffer := Buffer(1024 * 16)
global hDir
global pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback
global CompletionRoutineProc

; --- Main Script Body ---
DirCreate(watchDir)
DirCreate(logDir)
Log("--- Script Started (v6.0 - Back to Basics) ---")
Log("Watching folder: " . watchDir)

pCallback := ProcessFile
CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)
WatchFolder(watchDir)

Loop {
    DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)
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
; FILE PROCESSING FUNCTION
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
            Log("-> File does not exist anymore.")
            return
        }

        size1 := FileGetSize(fullPath)
        Sleep(stabilityDelay)
        size2 := FileGetSize(fullPath)

        if (size1 != size2 or size1 = 0) {
            Log("-> File is unstable or empty. Deleting.")
            FileDelete(fullPath)
            return
        }
        Log("-> File is stable.")
    } catch as e {
        Log("-> ERROR during stability check: " . e.Message)
        return
    }

    try {
        local content := Trim(FileRead(fullPath, "UTF-8"))
        FileDelete(fullPath)
        if (content != "") {
            Log("-> Content read. Sending text.")
            SendText(content)
        } else {
            Log("-> File was empty and has been deleted.")
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
        Log(errMsg)
        MsgBox(errMsg)
        ExitApp
    }

    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

; =============================================================================
; STABLE RE-ARMING FUNCTION
; =============================================================================
ReArmWatcher(*) {
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1

    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)
    local success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", true, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)

    if (success) {
        Log("Arming watcher successful.")
    } else {
        Log("--- WARNING: ReArmWatcher failed! Error: " . A_LastError . ". Retrying in 5s... ---")
        SetTimer(ReArmWatcher, -5000)
    }
}

; =============================================================================
; BULLETPROOF COMPLETION ROUTINE
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, pCallback

    try {
        if (dwErrorCode != 0) {
            Log("--- ERROR in IOCompletionRoutine. Code: " . dwErrorCode)
        } else if (dwNumberOfBytesTransfered > 0) {
            Log("==> Event TRIGGERED!")
            local pCurrent := pBuffer.Ptr
            Loop {
                local NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                local Action := NumGet(pCurrent + 4, "UInt")
                local FileName := StrGet(pCurrent + 12, NumGet(pCurrent + 8, "UInt") / 2, "UTF-16")

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
        SetTimer(ReArmWatcher, -1) ; SAFETY NET: Re-arm even on fatal error
        return
    }

    SetTimer(ReArmWatcher, -1) ; PRIMARY: Re-arm after processing
}
