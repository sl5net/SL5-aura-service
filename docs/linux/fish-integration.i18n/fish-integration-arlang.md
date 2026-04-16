# تكامل قشرة السمك

لتسهيل التفاعل مع STT (تحويل الكلام إلى نص) CLI، يمكنك إضافة وظيفة اختصار إلى تكوين Fish الخاص بك. يتيح لك ذلك كتابة "سؤالك" في الوحدة الطرفية.

                                             ## تعليمات الإعداد

تعمل مخازن قشر السمك كملفات فردية. الطريقة الموصى بها هي إنشاء ملف دالة مخصص.

1. قم بإنشاء ملف الوظيفة (سيتم إنشاء الدليل تلقائيًا إذا لم يكن موجودًا):
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

                     2. الصق الكتلة التالية في الملف:

```fish


please newest updates in zsh - verson


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

3. الوظيفة متاحة على الفور في جميع جلسات Fish الجديدة. لتحميله في الجلسة الحالية دون فتح محطة جديدة:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

                                  ## ملاحظات خاصة بالأسماك

- يستخدم Fish "قيمة VAR المحددة" بدلاً من "VAR=value" لتعيين المتغير.
- تستخدم الشروط كتلتي `test` و`end` بدلاً من `[ ]` و`fi`.
              - يستبدل `$argv` `$*` / `$@` لتمرير الوسيطة.
                      - يحل `$status` محل `$?` لرموز الخروج.
- `أو` / `و` استبدل `||` / `&&` في التعبيرات الشرطية.
- السمك **لا** يستخدم `محلي` - جميع المتغيرات داخل الوظائف محلية بشكل افتراضي.

                                                                  ## سمات

- **المسارات الديناميكية**: البحث عن جذر المشروع تلقائيًا عبر ملف العلامة `/tmp`.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فإنها تحاول تشغيل "start_service" وخدمات ويكيبيديا المحلية.
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.