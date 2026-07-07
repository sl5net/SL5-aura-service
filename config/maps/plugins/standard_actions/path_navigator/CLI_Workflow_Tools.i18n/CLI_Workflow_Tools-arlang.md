# دليل تثبيت أدوات سير العمل لـ CLI

تعتمد بعض الإجراءات في البرنامج المساعد Path Navigator على أدوات مساعدة لسطر الأوامر الخارجية لإجراء عمليات بحث غامضة، وقائمة الملفات، ومعالجة الحافظة. إذا كانت هذه الأدوات مفقودة، فسوف ترى تحذيرًا في وحدة تحكم النظام.

فيما يلي تعليمات التثبيت لكل نظام تشغيل مدعوم.

                                           ## المرافق المطلوبة

* **`fzf`**: مكتشف غامض لسطر الأوامر للأغراض العامة.
* **`find`** (أو `fd`): أداة مساعدة قياسية للبحث عن الملفات.
* **أداة الحافظة**: تستخدم لتوجيه الإخراج مباشرة إلى حافظة النظام لديك.
                              * **Linux:** `xclip` (يتطلب بيئة X11).
                               * **macOS:** `pbcopy` (مثبت مسبقًا).
                           * **Windows:** `مقطع` (مثبت مسبقًا).
* **`ملف`**: يحدد أنواع الملفات للمعاينات الطرفية الكاملة.

                                                                          ---

                                             ## تعليمات التثبيت

                                ### 1. لينكس (آرتش / مانجارو)
نظرًا لأن نظامك يعمل على Manjaro، يمكنك تثبيت الحزم المطلوبة باستخدام `pacman`:

```bash
sudo pacman -S fzf findutils xclip file
```



               ## 1. التحديد السريع للملفات (أمر Aura)

يستخدم الإجراء "path_navigator" الأمر "fzf" التالي لـ Git-aware. والغرض منه هو إخراج مسار الملف مباشرة إلى حافظة النظام.

                                                     **منطق الأمر:**
- يستخدم git ls-files داخل مستودع Git (باستثناء الملفات التي تم تجاهلها).
- يعود إلى `العثور على . -اكتب f` خارج مستودع Git.
- إخراج المسار المحدد إلى الحافظة باستخدام `xclip -selection clipboard`.

           ## 2. التنفيذ السريع للملفات (وظيفة \'k')

لإكمال الحلقة، يتم استخدام وظيفة الصدفة المخصصة `k`. تأخذ هذه الوظيفة المسار من الحافظة وتفتح الملف على الفور في "kate".

                                                               ### تطبيق

أضف الوظيفة التالية إلى ملف تكوين Shell الخاص بك (على سبيل المثال، `~/.bashrc`، `~/.zshrc`):

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

                                                       ### الاستخدام

1. استخدم الأمر "path_navigator" (على سبيل المثال، اكتب "ملف البحث" في أداة التشغيل الخاصة بك).
2. ابحث عن الملف المطلوب وحدده (على سبيل المثال، `src/main/config.py`).
3. في المحطة الطرفية الخاصة بك، اكتب "k" واضغط **ENTER**.
                   4. يتم فتح الملف على الفور في كيت.
                                                             __CODE_BLOCK_2__