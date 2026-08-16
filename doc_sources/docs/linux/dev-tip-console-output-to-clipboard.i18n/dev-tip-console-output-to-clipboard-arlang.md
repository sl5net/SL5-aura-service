# نصيحة المطورين: قم بنسخ مخرجات وحدة التحكم إلى الحافظة تلقائيًا

                     **الفئة:** إنتاجية Linux / ShellXSPACEbreakX
                   **النظام الأساسي:** Linux (zsh + Konsole/KDE)

                                                                          ---

                                                            ## المشكلة

عند العمل مع مساعدي الذكاء الاصطناعي، غالبًا ما تحتاج إلى نسخ مخرجات الوحدة الطرفية ولصقها في الدردشة. وهذا يعني عادة:
                                                     1. تشغيل الأمر
                                      2. حدد الإخراج بالماوس
                                                                  3. انسخ
                               4. قم بالتبديل إلى المتصفح
                                                                    5. لصق

                         هذا عدد كبير جدًا من الخطوات.

                                                                          ---

   ## الحل: الالتقاط التلقائي عبر `preexec` / `precmd`

                                             أضف هذا إلى `~/.zshrc`:

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}


precmd() {
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        cleaned=$(cat ~/t.txt \
            | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | sed "s|$HOME|~|g" \
            | sed 's/[^[:print:]]//g' \
            | grep -v '^$')
        if [ -n "$cleaned" ]; then
            echo "$cleaned" | xclip -selection clipboard
            echo "[📋 In Zwischenablage kopiert]"
        fi
    fi
}

```

                                                  ثم أعد التحميل:
```bash
source ~/.zshrc
```

                                                               ### نتيجة

بعد كل أمر، يكون الإخراج تلقائيًا في الحافظة الخاصة بك - جاهزًا للصقه في دردشة الذكاء الاصطناعي الخاصة بك باستخدام **Ctrl+V**.

يتم أيضًا حفظ الإخراج دائمًا في `~/t.txt` كمرجع.

                                                                          ---

                                                           ## كيف يعمل

                                           | الجزء | ماذا يفعل |
                                                        |------|------------|
| `preexec()` | يتم تشغيله قبل كل أمر، ويعيد توجيه الإخراج إلى `~/t.txt` |
| `بريكمد ()` | يتم تشغيله بعد كل أمر، ويستعيد stdout وينسخ إلى الحافظة |
| `تي ~/t.txt` | يحفظ الإخراج في ملف بينما يستمر في إظهاره في الوحدة الطرفية |
| `سيد\'...'' | شرائط تسلسل الهروب من عنوان KDE Konsole (`]2;...` `]1;`) |
       | `xclip` | نسخ الإخراج المنظف إلى الحافظة |

                                                                          ---

                                                            ## متطلبات

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

                                                                          ---

                                          ## ⚠️ ما لا يجب فعله

لا **لا** تستخدم `fc -ln -1 | bash` لإعادة تنفيذ الأمر الأخير:

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

يؤدي هذا إلى إعادة تنفيذ كل أمر بعد انتهائه، مما قد يسبب آثارًا جانبية مدمرة - على سبيل المثال الكتابة فوق الملفات، وإعادة تشغيل `git Commit`، وإعادة تشغيل `sed -i`، وما إلى ذلك.

يلتقط النهج `preexec`/`precmd` أعلاه المخرجات **أثناء** التنفيذ — وهي آمنة وموثوقة.