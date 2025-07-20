#Requires AutoHotkey v2.0
; type_watcher.ahk (v4.0 - Final "By-the-Book" Handle Fix)

#SingleInstance Force

; --- Konfiguration ---
watchDir := "C:\tmp"

; --- Globale Variablen für die DllCalls ---
global pBuffer := Buffer(1024 * 16)
global hDir
global pOverlapped := Buffer(A_PtrSize * 2 + 8, 0)
global pCallback

; --- Hauptteil des Skripts ---
logDir := A_ScriptDir . "\log"
DirCreate(logDir)
Log("--- Script Started (v4.0 - By-the-Book Strategy) ---")

pCallback := ProcessFile

; --- Windows API Konstanten für CreateFile ---
FILE_LIST_DIRECTORY       := 0x0001     ; Nötiges Zugriffsrecht für ReadDirectoryChangesW
FILE_SHARE_READ           := 0x0001
FILE_SHARE_WRITE          := 0x0002
FILE_SHARE_DELETE         := 0x0004
OPEN_EXISTING             := 3
FILE_FLAG_BACKUP_SEMANTICS := 0x02000000 ; Muss gesetzt sein, um ein Handle auf ein Verzeichnis zu bekommen
FILE_FLAG_OVERLAPPED      := 0x40000000 ; Muss gesetzt sein für Overlapped I/O

; <<< DIE FINALE KORREKTUR: Alle Parameter für CreateFile sind jetzt 100% nach offizieller Doku.
desiredAccess := FILE_LIST_DIRECTORY
shareMode := FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
flagsAndAttributes := FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OVERLAPPED

hDir := DllCall("CreateFile", "Str", watchDir, "UInt", desiredAccess, "UInt", shareMode, "Ptr", 0, "UInt", OPEN_EXISTING, "UInt", flagsAndAttributes, "Ptr", 0, "Ptr")
if (hDir = -1) {
    Log("FATAL: Could not open directory handle. Error: " . A_LastError), MsgBox("FATAL: Could not open directory handle."), ExitApp
}
Log("Successfully opened handle for directory: " . watchDir)

; --- DIE FINALE, ROBUSTE HAUPTSCHLEIFE ---
Loop {
    bytesReturned := Buffer(4)
    notifyFilter := 0x1 | 0x10 ; FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE

    DllCall("msvcrt\memset", "Ptr", pOverlapped.Ptr, "Int", 0, "Ptr", pOverlapped.Size)

    success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", 0)

    if not success {
        Log("FATAL: ReadDirectoryChangesW failed on setup. Error: " . A_LastError . ". Exiting.")
        ExitApp
    }

    Log("--- Watcher armed. Waiting for changes... ---")

    DllCall("GetOverlappedResult", "Ptr", hDir, "Ptr", pOverlapped, "Ptr", bytesReturned, "Int", true)

    numBytes := NumGet(bytesReturned, 0, "UInt")
    if (numBytes > 0) {
        Log("==> Event TRIGGERED! Processing " . numBytes . " bytes.")
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
    } else {
        Log("--> Spurious wakeup, no data. Re-arming...")
    }
}

Log("--- FATAL: Main loop exited unexpectedly. ---"), ExitApp


; =============================================================================
; LOGGING-FUNKTION (Unverändert)
; =============================================================================
Log(message) {
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch {
        ; Silent fail
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
