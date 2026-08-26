# openSUSE التشغيل التلقائي لـ XDG

في openSUSE، آلية التشغيل التلقائي لـ XDG هي نفسها الموجودة في Mint - `~/.config/autostart/` - لذلك ليست هناك حاجة إلى مفهوم منفصل مثل LaunchAgents لنظام التشغيل macOS هنا.

                                              ## بيئة سطح المكتب

الفرق هو بيئة سطح المكتب: سطح المكتب الافتراضي/الرئيسي لـ openSUSE هو في الواقع **KDE Plasma** (على عكس Mint)، لذا من المرجح أن يعمل النهج القائم على `konsole` من وثائقك الأصلية كما هو. يقدم openSUSE أيضًا إصدار جنوم، لذا سأقدم لك كلا الإصدارين بالإضافة إلى خيار خالٍ من الأجهزة الطرفية يعمل بغض النظر عن سطح المكتب.

**أولاً، قم بتأكيد مسار البرنامج النصي** (اضبط `linus` إذا كان جهاز SUSE يستخدم اسم مستخدم مختلف):

                                                                   ### يجد

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

                                                    ### كيدي بلازما

**الخيار أ — KDE Plasma** (سطح المكتب الافتراضي لـ openSUSE):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Starts the SL5 Aura Service
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
Icon=text-x-script
Terminal=false
StartupNotify=true
EOF
chmod +x ~/.config/autostart/aura_engine.desktop
```

                                        ### إصدار جنوم من openSUSE

**الخيار ب — إصدار جنوم من openSUSE:** فقط قم بتبديل سطر `Exec`، نظرًا لأن `konsole` عادةً لا يكون مثبتًا على جنوم:

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

                                        ### لا توجد محطة مرئية

**الخيار ج — موصى به: لا توجد محطة طرفية مرئية، خلفية + سجل** (يعمل بشكل مماثل على Plasma، GNOME، Xfce، أيًا كان — يتجنب السؤال "أي محطة تم تثبيتها" تمامًا، مثل المتغير القوي الذي قدمته لك لـ Mint):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Starts the SL5 Aura Service in the background
Exec=bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi'
Icon=text-x-script
Terminal=false
StartupNotify=false
EOF
chmod +x ~/.config/autostart/aura_engine.desktop
```

                                                  ## تحقق من السجل

                      تحقق من السجل لاحقًا باستخدام:

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**اختبار بدون تسجيل الخروج:** قم بتشغيل الجزء `bash -c\'...'` يدويًا في الوحدة الطرفية أولاً للتأكد من أنه يبدأ الخدمة فعليًا، ثم قم بتسجيل الخروج/الدخول للتحقق من مشغل التشغيل التلقائي الحقيقي. إعدادات نظام openSUSE (البلازما: *تشغيل تلقائي*؛ جنوم: *تطبيقات بدء التشغيل* عبر `gnome-tweaks`) ستدرج أيضًا هذا الإدخال بعد ذلك إذا كنت تريد تبديله من واجهة المستخدم الرسومية.