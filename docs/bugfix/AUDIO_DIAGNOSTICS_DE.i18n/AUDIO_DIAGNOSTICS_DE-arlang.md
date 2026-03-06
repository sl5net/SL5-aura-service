# النسخة الألمانية: `AUDIO_DIAGNOSTICS_DE.md`

                                              # Linux Audio-Diagnose for Aura

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Conflikte auftreten (المهلات، "الجهاز مشغول" أو التحكم في معدل العينة). Diese Befehle helfen bei der Fehlersuche.

                                      ### 1. أداة تحديد الهوية
قم بتشغيل جميع برامج الصوت من خلال Python-Umgebung:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **الصفحة:** يرجى ملاحظة **رقم الفهرس** و**معرف الجهاز (hw:X,Y)** الخاص بأجهزة الميكروفون.

                                   ### 2. هل نرغب في الأجهزة؟
عندما يكون "الجهاز مشغولاً" أو "انتهاء المهلة" في البداية، قم بإجراء العملية (PID) لحظر الأجهزة:
```bash
fuser -v /dev/snd/*
```
* **نصيحة:** إذا كان هناك أسلاك أنابيب أو أسلاك سباك، يتم تشغيلها بواسطة خادم الصوت. إذا كان أحد `python3` أو `obs` PID مباشرًا على جهاز PCM واحد، فسيتم حظره على الإطلاق. دن زوغريف للآخرين.

                                      ### 3. مراقبة Echtzeit (PipeWire)
يعتبر نظام Manjaro الحديث المزود بـ PipeWire من أفضل الأدوات:
```bash
pw-top
```
* **الصفحة:** اختبار Spalte `ERR` على الشاشة والنمط الآمن، مثل Aura (16000 هرتز) وOBS (48000 هرتز) لا يدومان وحدة المعالجة المركزية من خلال إعادة تشكيل العينات.

                            ### 4. متابعة الأحداث الصوتية
البث المباشر، عندما يتم تشغيل Mikrofone stummgeschaltet أو تدفقات جديدة:
```bash
pactl subscribe
```
* **الإجابة:** ابدأ بالموت والهالة. عندما يتم حذف الكثير من "الإزالة" - تبدأ الأحداث، مما يؤدي إلى حدوث عملية من خلال تغيير النظام.

                            ### 5. اختبار الأجهزة المباشر
تم اختباره باستخدام الميكروفون الخاص بالأجهزة (يشمل PulseAudio/PipeWire). بعد 5 ثواني:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **التوضيح:** عندما لا تكون هناك وظيفة، لا توجد هالة، حيث تكمن المشكلة في تكوين خوادم الصوت، ولا تتعلق بالأجهزة.

                             ### 6. عدم السقوط-إعادة الضبط
                               فشل النظام الصوتي الكامل:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

                                                                          ---

**نصيحة لسير العمل:** يمكنك توجيهه مباشرة إلى Kate، وذلك ببساطة `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` في هذا الأمر. 🌵🚀