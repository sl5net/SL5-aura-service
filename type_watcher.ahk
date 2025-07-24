#Requires AutoHotkey v2.0
; type_watcher.ahk (v8.3 - Correct FileRead Syntax)

#SingleInstance Force

; --- Configuration ---
watchDir := "C:\tmp\sl5_dictation"
logDir := A_ScriptDir "\log"
autoEnterFlagPath := "C:\tmp\sl5_auto_enter.flag"


; --- Global Variables ---
global pBuffer := Buffer(1024 * 16), hDir, pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global CompletionRoutineProc
global watcherNeedsRearm := false
global fileQueue := []           ; The queue for files
global isProcessingQueue := false ; Flag to prevent simultaneous processing

; --- Main Script Body ---
DirCreate(watchDir)
DirCreate(logDir)
Log("--- Script Started (v8.3 - Correct FileRead Syntax) ---")
Log("Watching folder: " . watchDir)

CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)
WatchFolder(watchDir) ; Initial arming

ProcessExistingFiles() ; Process initial files AND trigger the first queue run

; --- The Main Application Loop ---
Loop {
    DllCall("SleepEx", "UInt", 0xFFFFFFFF, "Int", true)

    if (watcherNeedsRearm) {
        Log("MainLoop: Detected re-arm flag. Calling ReArmWatcher.")
        watcherNeedsRearm := false
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
        MsgBox("CRITICAL LOGGING FAILURE!`n`nCould not write to: " . logFile . "`n`nReason: " . e.Message, "Logging Error", 16)
        ExitApp
    }
}

; =============================================================================
; INITIAL SCAN FOR EXISTING FILES
; =============================================================================
ProcessExistingFiles() {
    Log("Scanning for existing files to queue...")
    Loop Files, watchDir "\tts_output_*.txt" {
        QueueFile(A_LoopFileName)
    }
    Log("Initial scan complete. " . fileQueue.Length . " files queued.")
    TriggerQueueProcessing()
}

; =============================================================================
; FILE QUEUING FUNCTION
; =============================================================================
QueueFile(filename) {
    if InStr(filename, "tts_output_") {
        fullPath := watchDir "\" . filename
        Log("Queuing file -> " . filename)
        fileQueue.Push(fullPath)
    } else {
        Log("Ignored non-target file -> " . filename)
    }
}

; =============================================================================
; MASTER FUNCTION TO START QUEUE PROCESSING
; =============================================================================
TriggerQueueProcessing() {
    global isProcessingQueue
    if (isProcessingQueue) {
        return
    }
    isProcessingQueue := true
    Log(">>> Starting queue processing loop...")
    ProcessQueue()
    Log("<<< Queue processing loop finished.")
    isProcessingQueue := false
}

; =============================================================================
; QUEUE PROCESSING LOOP (WITH CORRECT v2 FILEREAD SYNTAX)
; =============================================================================
ProcessQueue() {
    while (fileQueue.Length > 0) {
        local fullPath := fileQueue[1]
        Log("Attempting to process from queue: " . fullPath)

        static stabilityDelay := 50
        local content := ""
        local isReadyForProcessing := false

        try {
            if !FileExist(fullPath) {
                Log("-> File no longer exists. Removing from queue.")
                fileQueue.RemoveAt(1)
                continue
            }
            size1 := FileGetSize(fullPath), Sleep(stabilityDelay), size2 := FileGetSize(fullPath)
            if (size1 != size2 or size1 = 0) {
                Log("-> File is unstable/empty. Deleting it.")
                FileDelete(fullPath)
                fileQueue.RemoveAt(1)
                continue
            }

            ; --- THE DEFINITIVE FIX IS HERE ---
            ; Using the correct AutoHotkey v2 syntax for FileRead.
            content := FileRead(fullPath, "UTF-8")
            content := Trim(content)

            isReadyForProcessing := true
            Log("-> File is stable and readable.")
        } catch as e {
            Log("-> CRITICAL ERROR while reading file. Removing to prevent blocking. Error: " . e.Message)
            fileQueue.RemoveAt(1) ; Remove blocking file
            continue ; Try next file
        }

        if (isReadyForProcessing) {
            fileQueue.RemoveAt(1)
            try {
                FileDelete(fullPath)
                Log("-> File successfully deleted.")
                if (content != "") {
                    Log("--> Sending content: '" . content . "'")
                    SendText(content)

                    ; --- Conditional Enter Key ---
                    ; Check if the auto-enter plugin is enabled
                    if FileExist(autoEnterFlagPath) {
                        flagState := Trim(FileRead(autoEnterFlagPath))
                        if (flagState = "true") {
                            SendInput("{Enter}")
                        }
                    }
                    ; --- End of Conditional Block ---

                } else {
                    Log("-> File was empty.")
                }
            } catch as e {
                Log("-> ERROR during FINAL delete/send step: " . e.Message)
            }
        }
    }
}

; =============================================================================
; WATCHER INITIALIZATION & RE-ARMING
; =============================================================================
WatchFolder(pFolder) {
    global hDir
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 7, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
    if (hDir = -1) {
        local errMsg := "FATAL: Could not watch directory: " . pFolder
        Log(errMsg), MsgBox(errMsg, "Error", 16), ExitApp
    }
    Log("Successfully opened handle for directory: " . pFolder)
    ReArmWatcher()
}

ReArmWatcher() {
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc
    static notifyFilter := 0x1
    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)
    local success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)
    if (success) {
        Log("Arming watcher successful.")
    } else {
        Log("--- WARNING: ReArmWatcher failed! Error: " . A_LastError . ". Flag will be re-checked. ---")
        watcherNeedsRearm := true
    }
}

; =============================================================================
; COMPLETION ROUTINE TRIGGERS PROCESSING
; =============================================================================
IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, watcherNeedsRearm

    try {
        if (dwErrorCode != 0) {
            Log("-> ERROR in IOCompletionRoutine. Code: " . dwErrorCode)
        } else if (dwNumberOfBytesTransfered > 0) {
            Log("==> Event TRIGGERED!")
            local pCurrent := pBuffer.Ptr
            Loop {
                local NextEntryOffset := NumGet(pCurrent, 0, "UInt")
                local Action := NumGet(pCurrent + 4, "UInt")
                local FileName := StrGet(pCurrent + 12, NumGet(pCurrent + 8, "UInt") / 2, "UTF-16")

                Log("--> Event data: Action=" . Action . ", FileName=" . FileName)

                if (Action = 1) {
                    QueueFile(FileName)
                }

                if (!NextEntryOffset) {
                    break
                }
                pCurrent += NextEntryOffset
            }
            TriggerQueueProcessing()
        }
    } catch as e {
        Log("--- FATAL ERROR in IOCompletionRoutine: " . e.Message . " ---")
    }

    watcherNeedsRearm := true
}
