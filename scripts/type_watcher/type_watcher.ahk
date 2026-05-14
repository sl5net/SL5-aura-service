#Requires AutoHotkey v2.0

#SingleInstance Off
; #SingleInstance Force ; is buggy, using Heartbeat mechanism instead
/**
 *
„Could not close the previous instance“ tritt genau dann auf, wenn ein Skript in einem Alertable State (SleepEx) oder einem tiefen DllCall (wie Folder-Watcher) feststeckt. AHKs Standardbefehl kann den Prozess dann nicht sauber beenden.
*/


/**
 * @file type_watcher.ahk
 * @description Monitors the STT output folder and types incoming text.
 * Includes a "Zombie Map" state machine to prevent double-processing
 * due to redundant Windows file system events.
 * https://www.autohotkey.com/docs/v2/Language.htm#comments
 *
 *
 * planed:
 * ListLines(False)
 *
 */

; --- Configuration ---

watchDir := "C:\tmp\sl5_aura\tts_output"
logDir := A_ScriptDir "\log"
autoEnterFlagPath := "C:\tmp\sl5_aura\sl5_auto_enter.flag"

heartbeat_start_File := "C:\tmp\heartbeat_type_watcher_start.txt"

global processedZombies := Map() ; Key: FullPath, Value: Timestamp
global isProcessingQueue := false


global fileStates := Map() ; Mögliche Zustände: "queued", "processing", "done"




; Am Anfang des Skripts (bevor der Watcher startet)
CleanTempFolder() {
    global watchDir
    Log("Cleaning up old session files...")
    Loop Files, watchDir "\tts_output_*.txt" {
        try {
            FileDelete(A_LoopFileFullPath)
        }
    }
}
CleanTempFolder() ; Einmal beim Start ausführen


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

; type_watcher.ahk:29
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

; type_watcher.ahk:69

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
QueueFile(filename) {
    global fileStates ; <--- Diese Zeile oben in der Funktion hinzufügen, falls sie fehlt
    if InStr(filename, "tts_output_") {
        fullPath := watchDir "\" . filename

        ; Wenn der Pfad in der Map ist (als "queued", "processing" oder Zeitstempel),
        ; ignorieren wir das Event.
        if fileStates.Has(fullPath) {
            return
        }

        fileStates[fullPath] := "queued"
        Log("Queuing new file -> " . filename)
        fileQueue.Push(fullPath)
    }
}


ProcessExistingFiles() {
    Log("Scanning for existing files...")
    Loop Files, watchDir "\tts_output_*.txt" {
        QueueFile(A_LoopFileName)
    }
    ScheduleQueueProcessing() ; Use the safe scheduler
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
; --- Ganz oben im Skript ---
global processedHistory := Map()







CleanupZombies() {
    global fileStates
    if (fileStates.Count == 0)
        return

    toDelete := []
    now := A_TickCount

    for fullPath, timestamp in fileStates {
        ; WICHTIG: Wenn val ein Text ist ("queued" oder "processing"),
        ; überspringen wir die Zeitberechnung, da die Datei noch in Arbeit ist.
        if !IsNumber(timestamp) {
            continue
        }

        ; 1. Versuche zu löschen, wenn die Datei noch da ist
        if FileExist(fullPath) {
            try {
                FileDelete(fullPath)
                ; Wenn erfolgreich, markieren wir den Map-Eintrag zum Löschen
                ; aber erst nach einer Sicherheitsmarge von 10 Sekunden
                if (now - timestamp > 10000) {
                    toDelete.Push(fullPath)
                }
            } catch {
                ; Noch gesperrt...
                ; Datei ist noch gesperrt (wahrscheinlich von Python)
                ; Wir lassen sie in der Map, damit sie nicht doppelt getippt wird.
            }
        } else {
            ; Datei ist physisch schon weg
            if (now - timestamp > 10000) {
                toDelete.Push(fullPath)
            }
        }

        ; 2. Aus der Map löschen, wenn Datei weg UND 10 Sek um
        if !FileExist(fullPath) && (now - timestamp > 10000) {
            toDelete.Push(fullPath)
        }

        ; 3. Sicherheits-Timeout (5 Min), falls Datei niemals gelöscht werden kann
        if (now - timestamp > 300000) {
            toDelete.Push(fullPath)
        }
    }

    for path in toDelete {
        if FileExist(path){
        fileStates.Delete(path)
        }
    }
}






; --- 2. Anpassung in ProcessQueue ---
ProcessQueue() {
    global isProcessingQueue, fileQueue, fileStates

    if (isProcessingQueue)
        return
    isProcessingQueue := true

    while (fileQueue.Length > 0) {
        local fullPath := fileQueue[1]
        ; fileQueue.RemoveAt(1) ; <--- WICHTIG: Sofort aus der Liste nehmen!

        ; Nur verarbeiten, wenn sie im Status "queued" ist
        if (!fileStates.Has(fullPath) || fileStates[fullPath] != "queued") {
            continue
        }

        ; Status auf "processing" setzen
        fileStates[fullPath] := "processing"

        try {
            ; Stabilitäts-Check (Punkt 3 der Experten: Sicherstellen, dass Python fertig ist)
            size1 := FileGetSize(fullPath), Sleep(100), size2 := FileGetSize(fullPath)
            if (size1 != size2 || size1 == 0) {
                fileStates[fullPath] := "queued" ; Zurücksetzen für nächsten Versuch
                isProcessingQueue := false
                return
            }

            content := Trim(FileRead(fullPath, "UTF-8"))
            if (content != "") {
                fileStates[fullPath] := A_TickCount
                Log("Typing content from " . fullPath)

                SendText(content)

                ; Erfolg! Status auf "done" setzen
                ; fileStates[fullPath] := "done"
                ; fileStates["last_processed_time_" . fullPath] := A_TickCount ; Für Debouncing
            }

            fileQueue.RemoveAt(1)

        } catch as e {
            Log("Error: " . e.Message)
            fileStates[fullPath] := "queued" ; Bei Fehler zurück in Warteschlange
            fileQueue.RemoveAt(1)
        }
    }

    CleanupZombies() ; Hier nutzen wir weiterhin fileStates statt processedZombies
    isProcessingQueue := false
} ; Ende von ProcessQueue()



; Hilfsfunktion für rückstandsloses Löschen
SecureDelete(filePath) {
    Loop 100 { ; Versuche es bis zu 10-mal (ca. 1 Sekunde lang)
        try {
            if !FileExist(filePath)
                return
            FileDelete(filePath)
            return ; Erfolg!
        } catch {
            Sleep(100) ; Warte 100ms, falls Datei noch gesperrt ist
        }
    }
    Log("CRITICAL: Could not delete sensitive file after 10 attempts: " filePath)
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
