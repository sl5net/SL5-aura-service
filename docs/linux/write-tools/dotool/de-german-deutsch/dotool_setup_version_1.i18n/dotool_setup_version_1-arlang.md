# dotool – التثبيت والتكوين (Manjaro / Arch-basiert)

                                                      ## هل كان dotool؟

`dotool` هي أداة بسيطة لمحاكاة لوحة المفاتيح في نظام التشغيل Linux.
إنها أداة رائعة مثل `xdotool` ووظيفة تعمل تحت X11 مثل Wayland.

                                                                          ---

                                ## التثبيت (مانجارو / آرتش)

                                               ### 1. حزمة التثبيت

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

                      ### 2. المستخدم هو `input`-Gruppe hinzufügen

```bash
sudo gpasswd -a $USER input
```

                                                  ### 3. udev-Regel erstellen

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

                                              ### 4. udev جديد محملة

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

                                        ### 5. تسجيل جديد (wichtig!)

لا يتم تسجيل الدخول الجديد من خلال مجموعة العمل.

                                                                          ---

                                                 ## تكوين المشروع

                                   ### `التكوين/الإعدادات.py`

```python
# Eingabemethode für X11: "dotool" (schnell) oder "xdotool" (Fallback)
x11_input_method_OVERRIDE = "dotool"

# Delay zwischen Tastenanschlägen in Millisekunden
# 2ms = dotool-Default, zuverlässig auch für Umlaute (ä, ö, ü, ß)
# 0ms = maximal schnell, kann Sonderzeichen verschlucken
dotool_typedelay = 2
```

                                                                          ---

                                ## تم استخدام أداة Skript dotool

                                                ### وظيفة إينجابي

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" | dotool
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

                                 ### تكوين auslesen (ohne Seiteneffekte)

يتم تعديل الإعدادات لذلك، dass `print()`-Ausgaben في `settings.py`
                                                 den Wert nicht verfälschen:

```bash
OVERRIDE=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.x11_input_method_OVERRIDE)
")
[[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"

DOTOOL_TYPEDELAY=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.dotool_typedelay)
")
```

                                                                          ---

                                                               ##هينويز

- **Umlaute und Sonderzeichen:** `اكتب التأخير 2` (افعل الأداة الافتراضية) هو empfohlen.
يمكن أن يكون `typedelay 0` مزودًا بـ ä، ö، ü، ß verloren gehen.
- **هل تحتاج إلى مساعدة؟** تطبيقات Manche (z. B. Electron، مدخلات المتصفح)
Verlieren Zeichen bei niedrigem Delay. في هذا الخريف `dotool_typedelay = 5` أو يتم استخدامه مرة أخرى.
- **Wayland:** تعمل أداة dotool أيضًا ضمن Wayland، ولا تتضمن xdotool المفصلات.
- **الاحتياطي:** إذا لم يتم تثبيت أداة dotool، فلن يتم تشغيل البرنامج النصي تلقائيًا على `xdotool`.
                                                                          ---

                                ## تم استخدام أداة Skript dotool

يبدأ البرنامج النصي في الاستمرار في `dotool\'-Prozess über ein FIFO،
هناك عمليات علوية جديدة يتم إجراؤها بواسطة Tastendruck.

                           ### الكود ذو الصلة (`type_watcher.sh`)

```bash
export DOTOOL_DELAY=0

# Alten Listener beenden falls noch läuft
pkill -f "dotool < /tmp/dotool_fifo" 2>/dev/null

DOTOOL_PID=$!

# typedelay direkt nach Start setzen
sleep 0.1
echo "typedelay 0" > /tmp/dotool_fifo

# Cleanup beim Beenden
trap "kill $DOTOOL_PID 2>/dev/null; rm -f /tmp/dotool_fifo" EXIT
```

                                                ### وظيفة إينجابي

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay 0\ntype %s\n' "$text" | dotool
        # printf 'typedelay 0\ntype %s\n' "$text" > /tmp/dotool_fifo
        # printf 'type %s\n' "$text" | dotool

    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

                                 ### تكوين auslesen (ohne Seiteneffekte)

يتم تعديل الإعدادات لذلك، dass `print()`-Ausgaben في `settings.py`
                                                 den Wert nicht verfälschen:

```bash
OVERRIDE=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.x11_input_method_OVERRIDE)
")
[[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"
```

                                                                          ---

                                                               ##هينويز

- **هل تحتاج إلى مساعدة؟** تطبيقات Manche (z. B. Electron، مدخلات المتصفح)
verlieren Zeichen bei `typedelay 0`. في هذا الخريف، يتم استخدام `typedelay 5` أو `typedelay 10`.
- **Wayland:** تعمل أداة dotool أيضًا ضمن Wayland، ولا تتضمن xdotool المفصلات.
- **الاحتياطي:** إذا لم يتم تثبيت أداة dotool، فلن يتم تشغيل البرنامج النصي تلقائيًا على `xdotool`.