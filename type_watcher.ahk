#Requires AutoHotkey v2.0
; type_watcher.ahk (FINAL - Synchronous Blocking Strategy)

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
Log("--- Script Started (SYNCHRONOUS Strategy) ---")

pCallback := ProcessFile

; Öffne das Verzeichnis zum Überwachen
hDir := DllCall("CreateFile", "Str", watchDir, "UInt", 1, "UInt", 3, "Ptr", 0, "UInt", 3, "UInt", 0x42000000, "Ptr", 0, "Ptr")
if (hDir = -1) {
    Log("FATAL: Could not open directory handle."), MsgBox("FATAL: Could not open directory handle."), ExitApp
}
Log("Successfully opened handle for directory: " . watchDir)

; --- DIE NEUE, ROBUSTE HAUPTSCHLEIFE ---
Loop {
    bytesReturned := Buffer(4)
    notifyFilter := 0x1 | 0x10 ; FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE

    ; Setze den Watcher auf. Dieser Call kehrt sofort zurück.
    success := DllCall("ReadDirectoryChangesW", "Ptr", hDir, "Ptr", pBuffer, "UInt", pBuffer.Size, "Int", false, "UInt", notifyFilter, "Ptr", 0, "Ptr", pOverlapped, "Ptr", 0)

    if not success {
        Log("FATAL: ReadDirectoryChangesW failed on setup. Error: " . A_LastError . ". Exiting.")
        ExitApp
    }

    Log("--- Watcher armed. Waiting for changes... ---")

    ; Dies ist der entscheidende Punkt: Wir warten hier, bis die obige Operation ein Ergebnis liefert.
    ; Der Befehl blockiert das Skript, bis ein Event eintritt.
    DllCall("GetOverlappedResult", "Ptr", hDir, "Ptr", pOverlapped, "Ptr", bytesReturned, "Int", true)

    ; Wenn wir hier ankommen, ist ein Event passiert.
    numBytes := NumGet(bytesReturned, 0, "UInt")
    if (numBytes > 0)
    {
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

; Diese Zeilen sollten niemals erreicht werden.
Log("--- FATAL: Main loop exited unexpectedly. ---")
ExitApp


; =============================================================================
; LOGGING-FUNKTION (Unverändert)
; =============================================================================
Log(message) {
    static logFile := A_ScriptDir . "\log\type_watcher.log"
    try {
        FileAppend(A_YYYY "-" A_MM "-" A_DD " " A_Hour ":" A_Min ":" A_Sec " - " . message . "`n", logFile)
    } catch {
        ; Silent fail, um MsgBox-Spam zu verhindern
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
