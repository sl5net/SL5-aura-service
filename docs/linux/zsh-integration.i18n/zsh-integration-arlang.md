# تكامل Zsh Shell

لتسهيل التفاعل مع STT (تحويل الكلام إلى نص) CLI، يمكنك إضافة وظيفة اختصار إلى `~/.zshrc`. يتيح لك ذلك كتابة "سؤالك" في الوحدة الطرفية.

                                             ## تعليمات الإعداد

1. افتح تكوين zsh الخاص بك باستخدام المحرر الذي تفضله:
   ```bash
   nano ~/.zshrc
   kate ~/.zshrc
   ```

          2. الصق الكتلة التالية في نهاية الملف:

```zsh
# --- STT Project Path Resolution ---

unalias s 2>/dev/null
s() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi

    update_github_ip

    local TEMP_FILE=$(mktemp)
    local SHORT_TIMEOUT_SECONDS=2
    local LONG_TIMEOUT_SECONDS=70

    # Path shortcuts
    local PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    local CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1

    local EXIT_CODE=$?
    local OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."

        start_service

        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        local KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'

        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1

    # 2. Timeout (124) == OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."

        local TEMP_FILE_2=$(mktemp)

        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1

        local EXIT_CODE_2=$?
        local OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ $EXIT_CODE_2 -ne 0 ]; then
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

                         3. أعد تحميل التكوين الخاص بك:
   ```bash
   source ~/.zshrc
   ```

                                                                  ## سمات
- **المسارات الديناميكية**: البحث عن جذر المشروع تلقائيًا عبر ملف العلامة `/tmp`.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فإنها تحاول تشغيل "start_service" وخدمات ويكيبيديا المحلية.
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.
                                                             __CODE_BLOCK_3__