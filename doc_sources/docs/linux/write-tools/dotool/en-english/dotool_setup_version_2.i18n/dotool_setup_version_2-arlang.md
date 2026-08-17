# dotool – التثبيت والتكوين (Manjaro / Arch-based)

                                                                  ## ملخص
`dotool` هي أداة مساعدة لمحاكاة الإدخال ذات المستوى المنخفض. على عكس xdotool، فإنه يتفاعل مباشرة مع نواة Linux عبر uinput، مما يجعله متوافقًا مع كل من **X11 وWayland**.

                                                                          ---

                                ## التثبيت (مانجارو / آرتش)

                                        ### 1. قم بتثبيت الحزمة
```bash
pamac build dotool
# or via yay: yay -S dotool
```

                                    ### 2. الأذونات وقواعد udev
للسماح لـ "dotool" بمحاكاة الإدخال بدون امتيازات الجذر، يجب أن يكون المستخدم الخاص بك جزءًا من مجموعة "الإدخال"، ويجب أن تكون قاعدة udev نشطة:

1. **أضف مستخدمًا إلى المجموعة:** `sudo gpasswd -a $USER input`
                                           2. **إنشاء قاعدة udev:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
                                3. **إعادة تحميل قواعد udev:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**هام:** يجب عليك **تسجيل الخروج وتسجيل الدخول مرة أخرى** حتى تدخل تغييرات المجموعة حيز التنفيذ.

                                                                          ---

                          ## تكوين المشروع (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

                                                                          ---

                                    ## تنفيذ البرنامج النصي

                                           ### تحسين الأداء (FIFO)
يعد بدء مثيل `dotool` جديد لكل كلمة بطيئًا (زمن الاستجابة حوالي 100 مللي ثانية). لتحقيق الكتابة "الفورية"، يستخدم البرنامج النصي عملية خلفية مستمرة للقراءة من أنبوب FIFO.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

                                                ### وظيفة الكتابة
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Pipe commands directly into the running background process
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

                                                                          ---

       ## استكشاف الأخطاء وإصلاحها والملاحظات
- **الأحرف المفقودة:** إذا تم تخطي الأحرف الخاصة (مثل علامات Umlauts)، قم بزيادة `dotool_typedelay` إلى 5 أو 10.
- **توافق التطبيقات:** قد تتطلب بعض التطبيقات (الإلكترون والمتصفحات) تأخيرًا أعلى لتسجيل الإدخال السريع بشكل صحيح.
- **دعم Wayland:** `dotool` هي الواجهة الخلفية المطلوبة لـ Wayland، حيث أن `xdotool` لا يدعمها.
- **الرجوع التلقائي:** يعود البرنامج النصي تلقائيًا إلى `xdotool` إذا لم يتم تثبيت `dotool` أو تكوينه بشكل صحيح.