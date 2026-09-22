> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Haufige_Fragen.md).*

# LanguageTool

check:

java -jar C:\tmp\STT\LanguageTool-6.6\languagetool-server.jar --port 8082

# My record button no longer works

Did you change operating system or computer?

For example:
The calculator key is different on Ubuntu. This must be taken into account when installing AutoHotkey, for example.
It's best to simply register a new button.

# The STT sometimes switches off

It's best to try the following first (as of 7/7/25 1:10 p.m. Mon):

## When used on a Linux system
```sh
cd ~/projects/py/STT

./type_watcher.sh

./scripts/restart_venv_and_run-server.sh

./keep_live.sh
```sh

Then the STT should no longer provide support


## Can not access microphone

Check app permissions (Windows 10/11):

    Go to Settings > Privacy and Security > Microphone.

    Make sure the "Microphone Access" and "Allow Apps to Access Your Microphone" are turned on.

    Important: Make sure that also "Allow desktop apps (Python) to access your microphone" Turned on (since Python usually runs as a desktop app).
    
    Probably supported entry in "Data protection and security"


## Editor for Window?

Notepad++ (Please delete keyboard shortcuts 192 and 193)
Please in the menu > View > Automatic line wrap
to switch on

For Python, PyCharm is often used, e.g., the Community Edition.

For many languages, including AutoHotkey, Studio Code.

Recommended extension: AHK++ (AutoHotkey Plus Plus)

## Recommendations for Window?

Installation of :

- https://github.com/sl5net/SL5-aura-service/archive/refs/tags/v0.12.0.1.zip
Installation manual (short version)
    Open the PowerShell with administrator rights.
    Run the setup script windows11 setup.bat from the project folder with PowerShell and administrator rights.
Important: DO NOT right-click the windows11 setup.bat file in Explorer and select "Run as Administrator".
because has to be executed from the project folder.
   
- https://www.autohotkey.com/ -> https://www.autohotkey.com/download/ahk-v2.exe

- Notedpadd++ https://notepad-plus-plus.org/downloads/ (please delete key combination 192 and 193)
Please resound in the menu > View > "Automatic line rebook"

Have fun editing the:
01 koan first steps 03 koan difficult names 05 koan search example    
02 koan listen 04 koan kleine helfer 06 koan wikipedia such ...  



## How do I see if the microphone is on or off in Windows 11?

It is also very easy to see on the microphone symbol when the microphone turns on and when it turns off by itself again.



