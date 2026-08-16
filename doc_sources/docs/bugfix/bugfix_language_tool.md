ps aux | grep languagetool

ps aux | grep languagetool                                                             

netstat -tulpn | grep 80port
# OR
ss -tulpn | grep 80port

ss -tulpn | grep 80port

tcp   LISTEN 0      50                      [::ffff:127.0.0.1]:80port  *:*    users:(("java",pid=...,fd=136))    

grep -rniI "language" ./*.py


# German specific :
```sh


curl -X POST "http://localhost:8082/v2/check" \
     -d "language=de-DE" \
     -d "text=Sebastian mit nachnamen"

     
     
```
