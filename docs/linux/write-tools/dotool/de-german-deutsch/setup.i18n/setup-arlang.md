## تكوين طريقة إدخال النص

                    ### Voraussetzungen für `dotool` (schneller als xdotool)

                 1. التثبيت: `pamac build dotool` أو `yay -S dotool`
   2. مجموعة إدخال المستخدم: `sudo gpasswd -a $USER input`
                                                    3. تصميم udev-Regel:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. قم بالتعديل الجديد: `sudo udevadm control --reload-rules && sudo udevadm Trigger`
                                                 5. ** تسجيل جديد **

                                                           ### التكوين

                                 في "التكوين/الإعدادات.py":
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

                                                             ### هينويز

- `dotool` ist deutlich شنلر مثل `xdotool` – bei sehr شنلر Ausgabe kann es sein، dass die Zielanwendung Zeichen verliert
- تم إلغاء قفل الإعدادات بشكل رائع من خلال Print-Ausgaben aus `settings.py` أثناء عمليات الاستيراد – وهذا هو الأفضل
- يستمع dotool-Listener إلى Hintergrundprozess über ein FIFO (`/tmp/dotool_fifo`) مع `typedelay 0`

                                                                          ---