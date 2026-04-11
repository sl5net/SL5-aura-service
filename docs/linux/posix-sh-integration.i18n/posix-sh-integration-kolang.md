# POSIX sh / 대시 통합

STT(Speech-to-Text) CLI와 더 쉽게 상호 작용할 수 있도록 셸 프로필에 바로가기 기능을 추가할 수 있습니다. 이렇게 하면 터미널에 '질문'을 입력하기만 하면 됩니다.

> **참고:** Dash 및 기타 엄격한 POSIX 셸(Debian/Ubuntu의 `/bin/sh`는 기본적으로 Dash입니다.) 모든 컨텍스트, 프로세스 대체 또는 배열에서 `local` 키워드를 지원하지 **않습니다**. 아래 함수는 POSIX와 완전히 호환되도록 작성되었습니다.

## 설정 지침

1. 원하는 편집기로 쉘 프로필을 엽니다.
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. 파일 끝에 다음 블록을 붙여넣습니다.

```sh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
    TEMP_FILE=$(mktemp)
    SHORT_TIMEOUT_SECONDS=2
    LONG_TIMEOUT_SECONDS=70
    # Path shortcuts
    PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"
    # --- 1. try
    timeout "$SHORT_TIMEOUT_SECONDS" \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    EXIT_CODE=$?
    OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            sh "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ "$EXIT_CODE" -eq 124 ] || [ "$EXIT_CODE" -eq 0 ]; then
        if [ "$EXIT_CODE" -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout "$LONG_TIMEOUT_SECONDS" \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ "$EXIT_CODE_2" -ne 0 ]; then
            echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        fi
        return 0
    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
```

3. 구성을 다시 로드합니다.
   ```sh
   . ~/.profile
   ```

## POSIX / Dash 관련 메모

- 'local'은 최대 호환성을 위해 여기서 사용되지 **않습니다**. 모든 변수는 관례에 의해서만 함수 범위로 지정됩니다. 엄격한 POSIX sh에서는 기술적으로 전역적입니다.
- 명령에 인수를 전달할 때 인용된 인수를 사용하여 적절한 단어 분할을 유지하기 위해 `$@`가 `$*`보다 선호됩니다.
- POSIX 툴체인 내에 유지하기 위해 Kiwix 도우미 스크립트를 실행할 때 `bash`는 `sh`로 대체됩니다.
- 이 구성 파일은 로그인 셸에서 제공되는 `~/.profile`에 배치하는 것이 가장 좋습니다. 대화형 비로그인 셸의 경우 배포판에서 `~/.shrc`를 사용할 수 있습니다. 시스템 설명서를 확인하세요.

## 특징

- **동적 경로**: `/tmp` 마커 파일을 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.