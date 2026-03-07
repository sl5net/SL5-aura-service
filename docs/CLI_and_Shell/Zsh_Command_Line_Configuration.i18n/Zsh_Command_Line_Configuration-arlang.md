يلخص هذا المستند تكوين Zsh النهائي والمتحقق منه للتفاعل مع خدمة Python الخاصة بك عبر سطر الأوامر.

يوفر التكوين ثلاث طرق متميزة للوصول إلى الخدمة، تتراوح من الإخراج الآمن إلى التنفيذ الفوري.

                             ## ملخص تكوين سطر الأوامر Zsh

                                                 ### 1. ملف التكوين

يجب لصق كافة التعليمات البرمجية أدناه في الملف **`~/.zshrc`** الخاص بك. تذكر **`المصدر ~/.zshrc`** أو فتح جلسة طرفية جديدة بعد إجراء التغييرات.

                                    ### 2. كتلة الكود النهائي

تحدد هذه الكتلة الوظائف الثلاث المطلوبة. وهو يتضمن أوامر "unalias" الضرورية لمنع خطأ التعارض الذي واجهناه سابقًا.

```bash
# ===================================================================
# == 1. sl: Output Only (Safe Mode - Just prints the result)
# ===================================================================

# Unalias 'sl' in case it was previously defined as a simple alias
unalias sl 2>/dev/null
sl() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/scripts/py/cli_client.py "$*" --lang "de-DE"
}
# source ~/.zshrc


# ===================================================================
# == 2. slz: Zsh Line Insertion (Safe Prep Mode - Paste output to prompt)
# ===================================================================

# Unalias 'slz' in case it was previously defined as an alias
unalias slz 2>/dev/null
slz() {
    if [ $# -eq 0 ]; then
        echo "Usage: slz <your question whose result should be pasted to the line>"
        return 1
    fi

    # 1. Execute the client and capture the output (the command string)
    # "$*" ensures all arguments are passed as a single string to the CLI client.
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Use 'print -z' to paste the captured command into the current prompt line.
    print -z "$COMMAND"
}
# source ~/.zshrc

# ===================================================================
# == 3. slxXsoidfuasdzof: Immediate Execution (DANGEROUS MODE)
# ===================================================================

# Unalias the long name in case it was previously defined
unalias slxXsoidfuasdzof 2>/dev/null
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Usage: slx <your question whose result will be executed immediately>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Check if any output was received
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        echo "--> Executing command: $COMMAND"
        # DANGER: 'eval' executes the command string immediately
        eval "$COMMAND"
    else
        echo "No command output received from the service."
    fi
}
# source ~/.zshrc

```

                                                                          ---

                          ### 3. استخدام الأوامر الثلاثة

             | الأمر | وظيفة | مستوى الأمان | مثال |
                                                | :--- | :--- | :--- | :--- |
| **`سل`** | **الإخراج القياسي:** ينفذ الخدمة ويطبع المخرج بالكامل مباشرةً على وحدة التحكم. | **آمنة** | `sl ما هو المنزل` (المطبوعات: "المنزل هو...") |
| **`سلز`** | **الإعداد للتنفيذ الآمن:** ينفذ الخدمة ويلصق المخرجات (على سبيل المثال، أمر shell) في سطر إدخال Zsh، ويكون جاهزًا للمراجعة أو التنفيذ. | **آمن/الإعدادية** | `slz git` (لصقات: `git add . && git الالتزام...` **ولكن لا يتم تشغيله**.) |
| **`slxXsoidfuasdzof`** | **التنفيذ الفوري:** تنفيذ الخدمة وتشغيل الإخراج على الفور كأمر Shell. استخدم الاسم المشفر كإجراء أمني. | **خطير** | `slxXsoidfuasdzof git` (يقوم بتشغيل الأمر `git add...` فورًا.) |