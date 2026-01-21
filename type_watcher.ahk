#Requires AutoHotkey v2.0
; type_watcher.ahk (v9.0 - Decoupled Callback & Safe SendMode, 21.1.'26 03:19 Wed)

; #SingleInstance Force ; is buggy

; --- Configuration ---
watchDir := "C:\tmp\sl5_aura"
logDir := A_ScriptDir "\log"
autoEnterFlagPath := "C:\tmp\sl5_auto_enter.flag"

heartbeat_start_File := "C:\tmp\heartbeat_type_watcher_start.txt"

; --- Main Script Body ---
myUniqueID := A_TickCount . "-" . Random(1000, 9999)

try {
    fileHandle := FileOpen(heartbeat_start_File, "w")
    fileHandle.Write(myUniqueID)
    fileHandle.Close()
} catch as e {
    MsgBox("FATAL: Could not write heartbeat file: " . e.Message, "Error", 16)
    ExitApp
}

; --- SendMode Event is safer than InputThenPlay on new Windows builds ---
SendMode('Event')
SetKeyDelay(10, 10)

; --- Global Variables ---
global pBuffer := Buffer(1024 * 16), hDir, pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global CompletionRoutineProc
global watcherNeedsRearm := false
global fileQueue := []
global isProcessingQueue := false

Sleep(200)
try {
    if FileExist(heartbeat_start_File) {
        lastUniqueID := Trim(FileRead(heartbeat_start_File))
        if (lastUniqueID != myUniqueID) {
            ExitApp ; other instance exists
        }
    }
} catch {
    ExitApp
}

SetTimer(CheckHeartbeatStart, 5000)

CheckHeartbeatStart() {
    global heartbeat_start_File, myUniqueID
    try {
        local lastUniqueID := Trim(FileRead(heartbeat_start_File, "UTF-8"))
        if (lastUniqueID != myUniqueID) {
            Log("Newer instance detected. Terminating self.")
            ExitApp
        }
    } catch {
        ExitApp
    }
}

DirCreate(watchDir)
DirCreate(logDir)
Log("--- Script Started (v9.0 - Fixed Callback Freeze) ---")
Log("Watching folder: " . watchDir)

CompletionRoutineProc := CallbackCreate(IOCompletionRoutine, "F", 3)
WatchFolder(watchDir)

ProcessExistingFiles()

; --- The Main Application Loop ---
Loop {
    ; This puts the script in "Alertable State" so callbacks can fire.
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
; LOGGING
; =============================================================================
Log(message) {
    static logFile := logDir "\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    }
}

; =============================================================================
; FILE QUEUING
; =============================================================================
ProcessExistingFiles() {
    Log("Scanning for existing files...")
    Loop Files, watchDir "\tts_output_*.txt" {
        QueueFile(A_LoopFileName)
    }
    ScheduleQueueProcessing() ; Use the safe scheduler
}

QueueFile(filename) {
    if InStr(filename, "tts_output_") {
        fullPath := watchDir "\" . filename
        for index, queuedPath in fileQueue {
            if (queuedPath = fullPath) {
                return
            }
        }
        Log("Queuing file -> " . filename)
        fileQueue.Push(fullPath)
    }
}

; =============================================================================
; Instead of running logic inside the callback, we set a Timer.
; This allows the callback to finish instantly, unfreezing the thread.
ScheduleQueueProcessing() {
    ; Run ProcessQueue once (-1) after 10ms
    SetTimer(ProcessQueue, -10)
}

; =============================================================================
; QUEUE PROCESSING LOOP
; =============================================================================
ProcessQueue() {
    global isProcessingQueue
    if (isProcessingQueue)
        return

    isProcessingQueue := true

    while (fileQueue.Length > 0) {
        local fullPath := fileQueue[1]
        static stabilityDelay := 50
        local content := ""
        local isReadyForProcessing := false

        try {
            if !FileExist(fullPath) {
                fileQueue.RemoveAt(1)
                continue
            }
            size1 := FileGetSize(fullPath), Sleep(stabilityDelay), size2 := FileGetSize(fullPath)
            if (size1 != size2 or size1 = 0) {
                FileDelete(fullPath)
                fileQueue.RemoveAt(1)
                continue
            }

            content := FileRead(fullPath, "UTF-8")
            content := Trim(content)
            isReadyForProcessing := true
        } catch as e {
            Log("Read Error: " . e.Message)
            fileQueue.RemoveAt(1)
            continue
        }

        if (isReadyForProcessing) {
            fileQueue.RemoveAt(1)
            try {
                ; --- DEBUG MESSAGE BOX ---
                ; MsgBox("Debug: I am about to send:`n" . content)
                ; -----------------------------------------------

                FileDelete(fullPath)

                if (content != "") {
                    Log("Sending: '" . SubStr(content, 1, 20) . "...'")
                    SendText(content)

                    if FileExist(autoEnterFlagPath) {
                        if (Trim(FileRead(autoEnterFlagPath)) = "true") {
                            SendInput("{Enter}")
                        }
                    }
                }
            } catch as e {
                Log("Process Error: " . e.Message)
            }
        }
    }
    isProcessingQueue := false
}

; =============================================================================
; WATCHER LOGIC
; =============================================================================
WatchFolder(pFolder) {
    global hDir
    hDir := DllCall("CreateFile", "Str", pFolder, "UInt", 1, "UInt", 7, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
    if (hDir = -1) {
        MsgBox("FATAL: Could not watch directory.", "Error", 16), ExitApp
    }
    ReArmWatcher()
}

ReArmWatcher() {
    global hDir, pBuffer, pOverlapped, CompletionRoutineProc, watcherNeedsRearm
    static notifyFilter := 0x11 ; 0x1 (Name) + 0x10 (LastWrite) - Better for file updates
    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)
    local success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", CompletionRoutineProc)
    if (!success) {
        Log("ReArmWatcher failed! Error: " . A_LastError)
        watcherNeedsRearm := true
    }
}

IOCompletionRoutine(dwErrorCode, dwNumberOfBytesTransfered, lpOverlapped) {
    global pBuffer, watcherNeedsRearm

    if (dwErrorCode != 0) {
        Log("IOCompletionRoutine Error: " . dwErrorCode)
        watcherNeedsRearm := true
        return
    }

    if (dwNumberOfBytesTransfered > 0) {
        local pCurrent := pBuffer.Ptr
        Loop {
            local NextEntryOffset := NumGet(pCurrent, 0, "UInt")
            local Action := NumGet(pCurrent + 4, "UInt")
            local FileName := StrGet(pCurrent + 12, NumGet(pCurrent + 8, "UInt") / 2, "UTF-16")

            ; Action 1 = Added, Action 3 = Modified
            if (Action = 1 or Action = 3) {
                QueueFile(FileName)
            }

            if (!NextEntryOffset)
                break
            pCurrent += NextEntryOffset
        }

        ; --- CRITICAL CHANGE: DO NOT PROCESS HERE ---
        ; Instead of calling ProcessQueue() directly, we schedule it.
        ScheduleQueueProcessing()
    }

    watcherNeedsRearm := true
}