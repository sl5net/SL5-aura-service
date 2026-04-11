# 생선 껍질 통합

STT(Speech-to-Text) CLI와 더 쉽게 상호 작용할 수 있도록 Fish 구성에 바로가기 기능을 추가할 수 있습니다. 이렇게 하면 터미널에 '질문'을 입력하기만 하면 됩니다.

## 설정 지침

Fish Shell은 기능을 개별 파일로 저장합니다. 권장되는 접근 방식은 전용 함수 파일을 생성하는 것입니다.

1. 함수 파일을 생성합니다(디렉토리가 없으면 자동으로 생성됩니다).
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. 다음 블록을 파일에 붙여넣습니다.

```fish
# --- STT Project Path Resolution ---
function s --description "STT CLI shortcut"
    if test (count $argv) -eq 0
        echo "question <your question>"
        return 1
    end

    update_github_ip

    set TEMP_FILE (mktemp)
    set SHORT_TIMEOUT_SECONDS 2
    set LONG_TIMEOUT_SECONDS 70

    # Path shortcuts
    set PY_EXEC "$PROJECT_ROOT/.venv/bin/python3"
    set CLI_SCRIPT "$PROJECT_ROOT/scripts/py/cli_client.py"

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    set EXIT_CODE $status
    set OUTPUT (cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    if echo "$OUTPUT" | grep -q "Verbindungsfehler"; or not pgrep -f "streamlit-chat.py" > /dev/null
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        set KIWIX_SCRIPT "$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if test -f "$KIWIX_SCRIPT"
            bash "$KIWIX_SCRIPT"
        end
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $argv"
        return 1

    # 2. Timeout (124) OR success (0)
    else if test $EXIT_CODE -eq 124; or test $EXIT_CODE -eq 0
        if test $EXIT_CODE -eq 0
            echo "$OUTPUT"
            return 0
        end
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        set TEMP_FILE_2 (mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
            "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
            --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        set EXIT_CODE_2 $status
        set OUTPUT_2 (cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if test $EXIT_CODE_2 -ne 0
            echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        end
        return 0

    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    end
end
```

3. 이 기능은 모든 새로운 Fish 세션에서 즉시 사용할 수 있습니다. 새 터미널을 열지 않고 현재 세션에서 로드하려면:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## 물고기 관련 참고 사항

- Fish는 변수 할당을 위해 `VAR=value` 대신 `set VAR value`를 사용합니다.
- 조건은 `[ ]` 및 `fi` 대신 `test` 및 `end` 블록을 사용합니다.
- `$argv`는 인수 전달을 위해 `$*` / `$@`를 대체합니다.
- `$status`는 종료 코드의 `$?`를 대체합니다.
- `or` / `and`는 조건식에서 `||` / `&&`를 대체합니다.
- Fish는 `local`을 사용하지 **않습니다** — 함수 내부의 모든 변수는 기본적으로 로컬입니다.

## 특징

- **동적 경로**: `/tmp` 마커 파일을 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.