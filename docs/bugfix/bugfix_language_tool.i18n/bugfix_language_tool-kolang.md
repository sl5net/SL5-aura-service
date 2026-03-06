PS 보조 | grep 언어 도구

PS 보조 | grep 언어 도구   

netstat -tulpn | grep 80포트
# 또는
ss -tulpn | grep 80포트

ss -tulpn | grep 80포트

tcp LISTEN 0 50 [::ffff:127.0.0.1]:80port *:* 사용자:(("java",pid=...,fd=136))   

grep -rniI "언어" ./*.py


# 독일어 특정:
```sh


curl -X POST "http://localhost:8082/v2/check" \
     -d "language=de-DE" \
     -d "text=Sebastian mit nachnamen"

     
     
```