# regular expressions rules

Important: Please apply the regular expressions in the correct order.

You must use the composite (more general) regular expression first, and then apply the specialized one.

The reason is that if the shorter, specialized regex runs first, it might match a part of the string that is essential for the larger, composite regex. This would make it impossible for the composite regex to find its match afterwards.
(S. 20.10.'25 18:37 Mon)

# Linux/Mac

if you want automaticly stat the service maybe add:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
to the autostart.

Start the service only on when there is an internet connection:
then set in settings_local.py :
SERVICE_START_OPTION = 1


## add enter
when you set 
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
to 1 it adds enter.

when you set 
tmp/sl5_auto_enter.flag 
to 1 it adds enter.

tmp/sl5_auto_enter.flag will be overwritten when you start the service.
tmp/sl5_auto_enter.flag is may eassier to parse for you with other scripts and its maybe bit faster read it.

use other numbers for disalbe
(S. 13.9.'25 16:12 Sat)


