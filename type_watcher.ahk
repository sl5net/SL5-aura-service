#Requires AutoHotkey v2.0
; type_watcher.ahk (v5.3 - Robust Event Loop)

#SingleInstance Force

; --- Configuration ---
watchDir := "C:\tmp"
logDir := A_ScriptDir "\log"

; --- Global Variables ---
global pBuffer := Buffer(1024 * 16)
global hDir
global pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback
global CompletionRoutineProc ; Ensures the callback's lifetime

; --- Main Script Body ---
DirCreate(logDir)
Log("--- Script Started (v5.3 - Robust Event Loop) ---")

pCallback := ProcessFile
CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)

WatchFolder(watchDir)

; --- The Unbreakable Anchor ---
Loop {
    DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)
}

Log("--- FATAL: Main loop exited unexpectedly. ---"), ExitApp

; =============================================================================
; LOGGING FUNCTION
; =============================================================================
Log(message) {
    static logFile := logDir "\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch {
        ; Fail silently if logging fails
    }
}

; =============================================================================
; FILE PROCESSING FUNCTION
; =============================================================================
ProcessFile(filename) {
    Log("ProcessFile called for: " . filename)
    static stabilityDelay := 50 ; ms
    local fullPath := watchDir "\" . filename

    try {
        if !FileExist(fullPath) {
            Log("-> File does not exist anymore. Probably processed by another event.")
            return
        }
        size1 := FileGetSize(fullPath)
        Sleep(stabilityDelay)
        size2 := FileGetSize(fullPath)

        if (size1 != size2 or size1 = 0) {
            Log("-> File size changed or is empty. Deleting unstable file.")
            FileDelete(fullPath)
            return
        }
        Log("-> File is stable and not empty.")
    } catch {
        Log("-> ERROR during stability check for " . fullPath)
        return
    }

    try {
        content := Trim(FileRead(fullPath, "UTF-8"))
        FileDelete(fullPath)
        if (content != "") {
            Log("-> Content read successfully. Sending text.")
            SendText(content)
        } else {
            Log("-> File was empty after read. Already deleted.")
        }
    } catch OSError {
        Log("-> ERROR: File was locked, could not read/delete " . fullPath)
    }
}

; =============================================================================
; WATCHER INITIALIZATION
; =============================================================================
WatchFolder(pFolder) {
    global hDir
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 7, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")

    if (hDir = -1) {
        errMsg := "FATAL: Could not watch directory: " . pFolder
        Log(errMsg), MsgBox(errMsg), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

; =============================================================================
; STABLE RE-ARMING FUNCTION
; =============================================================================
ReArmWatcher(*) {
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1 | 0x4 | 0x10 ; Action: FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE | FILE_NOTIFY_CHANGE_ATTRIBUTES

    Log("Arming watcher...")
    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)
    success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", true, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)

    if not success {
        Log("--- WARNING: ReArmWatcher failed! Error: " . A_LastError . ". Retrying in 5 seconds... ---")
        SetTimer ReArmWatcher, -5000
    }
}

; =============================================================================
; BULLETPROOF COMPLETION ROUTINE (REVISED)
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, pCallback

    try {
        if (dwErrorCode != 0) {
            Log("--- ERROR in IOCompletionRoutine. Code: " . dwErrorCode)
        } else if (dwNumberOfBytesTransfered > 0) {
            Log("==> Event TRIGGERED!")
            pCurrent := pBuffer.Ptr
            Loop {
                NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                Action := NumGet(pCurrent + 4, "UInt") ; 1=Created, 2=Deleted, 3=Modified, 4=RenamedOld, 5=RenamedNew
                FileNameLength := NumGet(pCurrent + 8, "UInt")
                FileName := StrGet(pCurrent + 12, FileNameLength / 2, "UTF-16")

                ; --- PRIMARY LOGGING (See everything) ---
                Log("--> Event data: Action=" . Action . ", FileName=" . FileName)

                ; --- FILTERING ---
                if (FileName = "dictation_service.heartbeat") {
                    Log("    - Ignoring heartbeat.")
                } else if ((Action = 1 or Action = 3) and InStr(FileName, "tts_output_")) {
                    Log("    - MATCH! Calling ProcessFile for: " . FileName)
                    pCallback(FileName)
                }

                if !NextEntryOffset
                    break ; Exit loop if this is the last entry
                    pCurrent += NextEntryOffset ; Move to the next entry in the buffer
            }
        }
        SetTimer ReArmWatcher, -1
    } catch as e {
        Log("--- FATAL ERROR in IOCompletionRoutine: " . e.Message . " ---")
        SetTimer ReArmWatcher, -1
    }
}
