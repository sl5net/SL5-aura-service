@echo off

:: Setzen Sie die Datei und das Verzeichnis
set FILE_TO_WATCH=C:\tmp\tts_output.txt
set DIR_TO_WATCH=C:\tmp

echo watch %FILE_TO_WATCH%

:: Überprüfen Sie, ob die Datei existiert
:loop
    if exist "%FILE_TO_WATCH%" (
        set /p TEXT_TO_TYPE=<"%FILE_TO_WATCH%"
        del /q /f "%FILE_TO_WATCH%"
        if not "%TEXT_TO_TYPE%"=="" (
            echo Typing: %TEXT_TO_TYPE%
            :: Verwenden Sie AutoHotkey oder AutoIt, um den Text zu tippen
			"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" typen.ahk %TEXT_TO_TYPE%
            timeout /t 1 /nobreak
        )
    )
    start /min robocopy /MON:1 /MOT:1 "%DIR_TO_WATCH%" "%DIR_TO_WATCH%" > nul
	timeout /t 1 /nobreak >nul
    goto loop
