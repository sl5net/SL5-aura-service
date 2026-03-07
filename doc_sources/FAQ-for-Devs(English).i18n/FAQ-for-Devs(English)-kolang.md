# 정규식 규칙

중요: 정규식을 올바른 순서로 적용하세요.

먼저 복합(보다 일반적인) 정규식을 사용한 다음 특수 정규식을 적용해야 합니다.

그 이유는 더 짧고 전문화된 정규식이 먼저 실행되면 더 큰 복합 정규식에 필수적인 문자열 부분과 일치할 수 있기 때문입니다. 이렇게 하면 나중에 복합 정규 표현식이 일치하는 항목을 찾는 것이 불가능해집니다.
(S.20.10.'25 18:37 월)

# 리눅스/맥

자동으로 서비스를 시작하려면 다음을 추가할 수 있습니다.
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
자동 시작에.

인터넷에 연결되어 있는 경우에만 서비스를 시작하세요.
그런 다음 settings_local.py에서 설정합니다.
SERVICE_START_OPTION = 1


## 추가 엔터
당신이 설정할 때
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
1에 Enter를 추가합니다.

당신이 설정할 때
tmp/sl5_auto_enter.flag
1에 Enter를 추가합니다.

서비스를 시작하면 tmp/sl5_auto_enter.flag를 덮어쓰게 됩니다.
tmp/sl5_auto_enter.flag는 다른 스크립트를 사용하여 구문 분석하는 것이 더 쉬울 수 있으며 읽기가 조금 더 빠를 수도 있습니다.

해제하려면 다른 번호를 사용하세요
(S. 13.9.'25 16:12 토)