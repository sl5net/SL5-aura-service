# reguły wyrażeń regularnych

Ważne: Proszę zastosować wyrażenia regularne w odpowiedniej kolejności.

Najpierw musisz użyć złożonego (bardziej ogólnego) wyrażenia regularnego, a następnie zastosować specjalistyczne.

Powodem jest to, że jeśli krótsze, wyspecjalizowane wyrażenie regularne zostanie uruchomione jako pierwsze, może dopasować część łańcucha niezbędną dla większego, złożonego wyrażenia regularnego. Uniemożliwiłoby to późniejsze znalezienie dopasowania złożonego wyrażenia regularnego.
(S. 20.10.'25 18:37 pon.)

# Linux/Mac

jeśli chcesz automatycznie uruchomić usługę, możesz dodać:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
do autostartu.

Uruchom usługę tylko wtedy, gdy jest połączenie internetowe:
następnie ustaw w settings_local.py :
USŁUGA_START_OPCJA = 1


## dodaj enter
kiedy ustawisz
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
do 1 dodaje enter.

kiedy ustawisz
tmp/sl5_auto_enter.flag
do 1 dodaje enter.

tmp/sl5_auto_enter.flag zostanie nadpisany po uruchomieniu usługi.
tmp/sl5_auto_enter.flag może być łatwiejszy do przeanalizowania za pomocą innych skryptów i może nieco szybciej się go czyta.

użyj innych numerów, aby wyłączyć
(S. 13.9.'25 16:12 sob.)