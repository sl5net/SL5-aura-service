; sync_editor.ahk

#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

/**
 * @file sync_editor.ahk
 * @description Handles Editor-Disk synchronization. Forces saves and
 * auto-confirms "Reload File" dialogs for a seamless user experience.
 * https://www.autohotkey.com/docs/v2/Language.htm#comments
 */


; sync_editor.ahk
action := "notify" ; A_Args[1]

if (action = "save") {
    Send("^s")
}
else if (Action = "notify") {
    ; show MsgBox 1 Sekunde (Timeout)
    ; 64 = Info-Icon, Titel: Aura Service
    MsgBox("🔧 Auto-Fix in Background-Loop finished ...", "Aura Service", 64 " T1")
}
