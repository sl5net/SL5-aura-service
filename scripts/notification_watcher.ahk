#Requires AutoHotkey v2.0

#SingleInstance Force ; is buggy, using Heartbeat mechanism instead

/**
 * @file notification_watcher.ahk
 * @description Displays non-blocking system notifications and feedback
 * from the STT background service.
 * https://www.autohotkey.com/docs/v2/Language.htm#comments
 */


A_IconTip := "SL5 Aura Notifier"

; Create a borderless, always-on-top GUI window for our notification
noteGui := Gui("+AlwaysOnTop -Caption +ToolWindow")
noteGui.SetFont("s10", "Segoe UI")
titleCtrl := noteGui.Add("Text", "w300")
noteGui.SetFont("s9", "Segoe UI")
bodyCtrl := noteGui.Add("Text", "w300 y+5")

SetTimer(WatchForNotification, 250)

WatchForNotification() {
    static notifyFile := "C:\tmp\notification.txt"

    if FileExist(notifyFile) {
        content := Trim(FileRead(notifyFile))
        FileDelete(notifyFile)
        if (content = "")
            return

        parts := StrSplit(content, "|")
        titleCtrl.Text := parts[1]
        bodyCtrl.Text := parts.Has(2) ? parts[2] : ""

        ; Position and show the GUI
        noteGui.Show("NA")
        ; Hide it after 5 seconds
        SetTimer(HideGui, -5000)
    }
}

HideGui() {
    noteGui.Hide()
}
