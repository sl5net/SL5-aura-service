; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des STT Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f10::
f11::
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
