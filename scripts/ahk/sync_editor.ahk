; sync_editor.ahk
#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

; sync_editor.ahk
action := "notify" ; A_Args[1]

if (action = "save") {
    ; Sende Strg+S an das aktive Fenster
    Send("^s")
}
else if (Action = "notify") {
    ; Zeige eine Nachricht für 1 Sekunde (Timeout)
    ; 64 = Info-Icon, Titel: Aura Service
    MsgBox("🔧 Auto-Fix in Background-Loop finished ...", "Aura Service", 64 " T1")
}
