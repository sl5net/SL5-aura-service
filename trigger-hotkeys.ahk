#Requires AutoHotkey v2.0
CoordMode("Mouse", "Screen")
CoordMode("Caret", "Screen")
CoordMode("Pixel", "Screen")

; trigger-hotkeys.ahk
; #SingleInstance Force ; is buggy, using Heartbeat mechanism instead
#SingleInstance Off
#UseHook True
ListLines(False)
; trigger_hotkey.ahk
/**
 * @file trigger-hotkeys.ahk
 * @description Captures global hotkeys (F10/F11) to control the STT service.
 * Designed to run with high privileges via Task Scheduler to override system keys.
 * https://www.autohotkey.com/docs/v2/Language.htm#comments
 *
 */

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

*$f10::
$f11::
{
    static lastPress := 0
    if (A_TickCount - lastPress < 900) ; 500ms Sperre
        return
    lastPress := A_TickCount

    activeWinTitle := WinGetTitle('A')
    ; MsgBox, "%activeWinTitle%"
    local activeWinTitleFile  := "c:\tmp\activeWinTitle.txt"
    try FileDelete activeWinTitleFile
    FileAppend activeWinTitle, activeWinTitleFile

    if InStr(activeWinTitle, ".py - Notepad++")
    {
        Send("^s")
    }

    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("STT Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}

def calc_y(mouse_y, offset, height):
    bottom_edge = mouse_y - offset
    top_edge = bottom_edge - height
return top_edge

; ------------------------------------------------------------------
; F12 -> Launch Search Rules / Command Palette on Windows
; ------------------------------------------------------------------
*$f12::
*$#y::
{
    static lastPress := 0
    if (A_TickCount - lastPress < 900) ; Debounce protection
        return
    lastPress := A_TickCount

    project_root_file := "c:\tmp\sl5_aura\sl5net_aura_project_root"
    if not FileExist(project_root_file) {
        MsgBox("Error: Project root file not found at " . project_root_file, "Aura Error", 16)
        return
    }

    try {
        project_root := Trim(FileRead(project_root_file, "UTF-8"))
        bat_dir := project_root . "\scripts\search_rules"
;        bat_path := bat_dir . "\search_rules.bat"
        ps_path := bat_dir . "\search_rules.ps1"

;        if not FileExist(bat_path) {
;            MsgBox("Error: Batch script not found at " . bat_path, "Aura Error", 16)
;            return
;        }
        if not FileExist(ps_path) {
            MsgBox("Error: ps1 script not found at " . ps_path, "Aura Error", 16)
            return
        }

        ; OLD Run the batch file with the correct working directory
        ; Run('"' . bat_path . '"', bat_dir)

        ; Neu: 3.7.'26 13:50 Fri


        callerHWND := WinExist("A")
        ; Run('powershell.exe -NoProfile -ExecutionPolicy Bypass -File "' . ps_path . '"', bat_dir, , &psPID)


        Run('wt.exe powershell.exe -NoProfile -ExecutionPolicy Bypass -File "' . ps_path . '"', bat_dir, , &psPID)
        if (targetHWND := WinWait("powershell.exe", , 5)) {
            WinActivate(targetHWND)


			CoordMode("Mouse", "Screen")
			CoordMode("Caret", "Screen")
			CoordMode("Pixel", "Screen")

            MouseGetPos(&mouseX, &mouseY)
            WinGetPos(&currentX, &currentY, &currentW, , targetHWND)
            targetX := currentX
            targetHeight := 300
            targetY := mouseY - 10 - targetHeight
			Sleep(10)
			WinSetAlwaysOnTop(true, targetHWND)

            WinMove(targetX, targetY, currentW, targetHeight, targetHWND)
			Sleep(10)
            WinMove(targetX, targetY, currentW, targetHeight, targetHWND)
			Sleep(10)
            WinMove(targetX, targetY, currentW, targetHeight, targetHWND)


            ; 4. WAIT for this specific search terminal window to close
            WinWaitClose(targetHWND)

            ; 5. Once it closed, immediately refocus your original working window!
            if WinExist(callerHWND) {
                WinActivate(callerHWND)
            }

        }

    } catch as e {
        MsgBox("Error launching Search Rules: " . e.Message, "Aura Error", 16)
    }
}

#HotIf WinActive("ahk_class CASCADIA_HOSTING_WINDOW_CLASS")
^Backspace::Send("!{Backspace}")
#HotIf

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







