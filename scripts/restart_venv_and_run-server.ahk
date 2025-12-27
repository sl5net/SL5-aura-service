#Requires AutoHotkey v2.0
; restart_venv_and_run-server.ahk

FileReadLine(File, LineNumber)
{
    FileRead FileContents, %File%
    FileContents := ""
    Loop Parse, FileContents, "`n", "`r"
    {
        If (A_Index = LineNumber)
        return Trim(A_LoopField)
    }
    return ""
}

; Setzen Sie den Pfad zum Skript-Verzeichnis
; ScriptDir := FileGetDir(A_ScriptFullPath)
ScriptDir := A_ScriptDir

; Setzen Sie den Pfad zur Konfigurationsdatei
ConfigFile := ScriptDir . "\..\config\server.conf"

; Setzen Sie den Pfad zum Server-Skript
ServerScript := ScriptDir . "\activate-venv_and_run-server.sh"

; Lese die Konfigurationsdatei und lade die Variable PORT
FileRead ConfigFile, "r"
PORT := Trim(FileReadLine(ConfigFile, 1), " `t")

; Starte den Server neu
MsgBox "Restarting TTS Server on Port " PORT "..."
Run "pkill -f aura_engine.py"
Run "pkill -f type_watcher.sh"
; DO NOT kill LanguageTool server here. Run "pkill -f languagetool-server.jar"

Sleep 1000

; Überprüfe, ob ein Prozess auf dem Port läuft
PID := ""
PID := Run("lsof -t -i :" PORT, "", "", Output)
if (PID != "")
{
    Run "kill " PID
    Sleep 1000
}

; Starte das Server-Skript neu
Run ServerScript
