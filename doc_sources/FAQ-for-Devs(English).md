
# Linux/Mac

if you want automaticly stat the service maybe add:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
to the autostart.

Start the service only on when there is an internet connection:
then set in settings_local.py :
SERVICE_START_OPTION = 1


## add enter
when you set 
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION
to 1 it adds enter.

when you set 
tmp/sl5_auto_enter.flag 
to 1 it adds enter.

tmp/sl5_auto_enter.flag will be overwritten when you start the service.
tmp/sl5_auto_enter.flag is may eassier to parse for you with other scripts and its maybe bit faster read it.

use other numbers for disalbe
(S. 13.9.'25 16:12 Sat)


