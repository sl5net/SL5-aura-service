### الجزء الأول: التوثيق الألماني

        # dotool – التثبيت والتكوين (Manjaro / Arch-basiert)

                                                      ## هل كان dotool؟
`الأداة` هي أداة محاكاة لـ Tatatureingaben. يتم التواصل مع `xdotool` مباشرة من خلال Kernel عبر `uinput` والوظائف العالمية تحت **X11 وWayland**.

                                                                          ---

                                ## التثبيت (مانجارو / آرتش)

                                               ### 1. حزمة التثبيت
```bash
pamac build dotool
# oder: yay -S dotool
```

                                                  ### 2.Berechtigungen setzen
ومع ذلك، يجب أن تقوم "أداة النقر" بتفعيل الجذر الصحيح، ويجب على المستخدم إدخال مجموعة "الإدخال" وضبط إعدادات المستخدم:

                        1. **User zur Gruppe:** `sudo gpasswd -a $USER input`
                                                         2. ** udev-Regel: **
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
                                        3. **التغذية الجديدة:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**الموافقة:** معلومات بسيطة **تسجيل دخول جديد**، يرجى الاتصال بالمجموعة النشطة.

                                                                          ---

                          ## تكوين المشروع (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

                                                                          ---

                                                         ## تنفيذ Skript

                                                      ### Prozessenter (FIFO)
في حالة عدم وجود لوحات مفاتيح جيدة وفقًا لمعايير النفقات العامة، يرجى استخدام أنبوب Skript (FIFO). تم إعادة تعيين Dadurch `dotool` verzögerungsfrei.

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

                                                     ### Die Eingabe-Funktion
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Sendet Befehle direkt an den wartenden Prozess
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

                                                                          ---

                                   ## هينويز وفيهلربهيبونج
- **Fehlende Zeichen:** Wenn Umlaute verschluckt werden، erhöhe `dotool_typedelay` auf 5 oder 10.
- **الاحتياطي:** لم يتم تكوين `dotool` بشكل صحيح، حيث يتم تشغيل النظام تلقائيًا على `xdotool` من البداية.
- **دعم Wayland:** ضمن Wayland يتم استخدام `dotool` تلقائيًا، ولا تعمل `xdotool`.tool`.