# تكامل Ksh (Korn Shell).

لتسهيل التفاعل مع STT (تحويل الكلام إلى نص) CLI، يمكنك إضافة وظيفة اختصار إلى `~/.kshrc`. يتيح لك ذلك كتابة "سؤالك" في الوحدة الطرفية.

                                             ## تعليمات الإعداد

1. افتح تكوين Ksh الخاص بك باستخدام المحرر الذي تفضله:
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

          2. الصق الكتلة التالية في نهاية الملف:

```ksh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
function s {
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
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
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
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
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

3. تأكد من قيام Ksh بتحميل ملف التكوين الخاص بك. أضف هذا أو تحقق منه في `~/.profile`:
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

                         4. أعد تحميل التكوين الخاص بك:
   ```ksh
   . ~/.kshrc
   ```

                                           ## ملاحظات خاصة بـKsh

- يدعم Ksh بناء جملة `اسم الوظيفة { }` و`name() { }`؛ يتم استخدام الكلمة الأساسية "function" هنا للتوضيح.
- `local` **غير** مدعوم في جميع متغيرات Ksh (على سبيل المثال `ksh88`). ولذلك يتم الإعلان عن المتغيرات في الوظيفة أعلاه بدون "محلي". إذا كنت تستخدم `mksh` أو `ksh93`، فيمكن استخدام `typeset` بدلاً من ذلك: `typeset TEMP_FILE=$(mktemp)`.
- يتحكم المتغير `ENV` في ملفات مصادر Ksh للجلسات التفاعلية، على غرار `.bashrc`.

                                                                  ## سمات

- **المسارات الديناميكية**: البحث عن جذر المشروع تلقائيًا عبر ملف العلامة `/tmp`.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فإنها تحاول تشغيل "start_service" وخدمات ويكيبيديا المحلية.
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.