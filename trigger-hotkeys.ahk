#Requires AutoHotkey v2.0

#UseHook True
#InstallKeybdHook

; trigger_hotkey.ahk
; #SingleInstance Force ; is buggy, using Heartbeat mechanism instead

; --- Configuration ---
heartbeat_start_File := "c:\tmp\heartbeat_trigger_hotkey_start.txt"
triggerFile := "c:\tmp\sl5_record.trigger"
activeWinTitleFile := "c:\tmp\activeWinTitle.txt"

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

; --- Self-Check at Startup ---
Sleep(200) ; Give time for write operations
try {
    if FileExist(heartbeat_start_File) {
        lastUniqueID := Trim(FileRead(heartbeat_start_File))
        if (lastUniqueID != myUniqueID) {
            ExitApp ; Newer instance exists, I must exit.
        }
    }
} catch {
    ; Ignore errors here, loop will handle it
}

SetTimer(CheckHeartbeatStart, 5000)

; =============================================================================
; SELF-TERMINATION VIA HEARTBEAT CHECK
; =============================================================================
CheckHeartbeatStart() {
    global heartbeat_start_File, myUniqueID
    try {
        local lastUniqueID := Trim(FileRead(heartbeat_start_File, "UTF-8"))
        if (lastUniqueID != myUniqueID) {
            ; New instance took over
            ExitApp
        }
    } catch {
        ; If file is locked/deleted, better safe than sorry -> exit
        ExitApp
    }
}

; =============================================================================
; HOTKEY DEFINITIONS (F10 & F11)
; =============================================================================

; Prevent Windows from capturing F10 and F11 input
; the '$' modifier to the F10 and F11 hotkey forces AutoHotkey to use the keyboard hook, preventing the native Windows events (like menu activation) from firing alongside the script.

$f10::
$f11::
{
    activeWinTitle := WinGetTitle('A')
    ; MsgBox, "%activeWinTitle%"
    local activeWinTitleFile  := "c:\tmp\activeWinTitle.txt"
    try FileDelete activeWinTitleFile
    FileAppend activeWinTitle, activeWinTitleFile


    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("STT Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}


; ------------------------------------------------------------------
; STRG+Q -> CopyQ Window/Fenster toggle/umschalten (Anzeigen/Verstecken)
; ------------------------------------------------------------------
$^q::
{
    ; both should work show and toggle: https://github.com/hluk/CopyQ/issues/3011
    ; Standard-Pfad definieren
    exePath := "C:\Program Files\CopyQ\copyq.exe"
    ; "C:\Program Files\CopyQ\copyq.exe" toggle

    SplitPath exePath, &exeName, &exeDir

;    Run('"' exePath '" toggle', exeDir)
    Run('"' exePath '" show', exeDir)


}







