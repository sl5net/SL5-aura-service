# dotool على Wayland - الإعداد واستكشاف الأخطاء وإصلاحها

مطلوب `dotool` لكي تتمكن Aura من كتابة نص في تطبيقات أخرى على Wayland.
على عكس `xdotool`، فإنه يتصل مباشرة مع Linux kernel عبر `uinput`
                               ويعمل على كل من **X11 وWayland**.

في X11، يتم استخدام `xdotool` بشكل افتراضي. `dotool` اختياري على X11 ولكن
يوصى به لتحسين استقرار التخطيط (خاصة مع علامات تغير الصوت).

                                                                          ---

                                           ## 1. قم بتثبيت دوتول

                         ** آرتش / مانجارو / كاشيوس (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu / Debian (إذا كان متوفرًا في اتفاقيات إعادة الشراء):**
```bash
sudo apt install dotool
```

**إذا لم يكن في اتفاقات إعادة الشراء — قم بالإنشاء من المصدر:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

                                                                          ---

      ## 2. السماح بتشغيل dotool بدون الجذر (مطلوب)

يحتاج `dotool` إلى الوصول إلى `/dev/uinput`. وبدون هذا، سوف تفشل بصمت.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**يلزم إعادة تسجيل الدخول** بعد تغيير المجموعة حتى تدخل حيز التنفيذ.

                                                                          ---

                                           ## 3. تحقق من التثبيت

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

إذا لم تعرض "المجموعات" "الإدخال"، فقم بتسجيل الخروج ثم الدخول مرة أخرى (أو أعد التشغيل).

                                                                          ---

                                        ## 4. كيف تستخدم Aura dotool

                                     Aura `type_watcher.sh` تلقائيًا:

           - يكتشف Wayland عبر `$WAYLAND_DISPLAY` ويحدد `dotool`
- بدء تشغيل البرنامج الخفي `dotoold` في الخلفية إذا كان موجودًا ولا يعمل
- يعود إلى `xdotool` إذا لم يتم تثبيت `dotool` (X11 فقط)
- لتعيين تخطيط لوحة المفاتيح من طراز Vosk النشط لديك (على سبيل المثال، `de` → `XKB_DEFAULT_LAYOUT=de`)

ليست هناك حاجة إلى إدارة البرنامج الخفي يدويًا — يتعامل Aura مع هذا الأمر عند بدء التشغيل.

                                                                          ---

                         ## 5. استكشاف الأخطاء وإصلاحها

                       **تسجل الهالة ولكن لا يظهر نص:**
```bash
# Check if dotool is installed:
command -v dotool

# Check group membership:
groups | grep input

# Test manually (focus a text field first):
echo "type hello" | dotool

# Check the watcher log:
tail -30 log/type_watcher.log
```

**أحرف مفقودة أو مشوهة (خاصة علامات تغير الصوت):**

 قم بزيادة تأخير الكتابة في `config/settings_local.py`:
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

** يعمل dotool في الوحدة الطرفية ولكن ليس في Aura:**

تأكد من أن مجموعة "الإدخال" نشطة في جلسة سطح المكتب (وليس فقط محطة طرفية جديدة).
 يلزم إعادة تسجيل الدخول بالكامل بعد `gpasswd`.

**فرض أداة dotool على X11** (اختياري، لتحقيق استقرار أفضل للتخطيط):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

                                                                          ---

    ## 6. الإجراء الاحتياطي إذا تعذر تثبيت dotool

إذا لم يكن `dotool` متاحًا على نظامك، فستعود Aura إلى `xdotool` على X11.
في Wayland بدون `dotool`، تكون الكتابة **غير مدعومة** — وهذا هو Wayland
                            قيود أمنية، وليس قيود هالة.

الأدوات البديلة التي قد تعمل على مكونات محددة:

                                               | أداة | يعمل على |
                                                                    |---|---|
                                                   | `xdotool` | X11 فقط |
                       | `دوتول` | X11 + وايلاند (مستحسن) |
                          | `ydotool` | X11 + وايلاند (البديل) |

                                  لاستخدام `ydotool` كحل يدوي:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
ملاحظة: لا تقوم Aura بدمج `ydotool` أصلاً — يلزم التكوين اليدوي.