#المغسلة_الموحدة
                          ## settings.AUDIO_INPUT_DEVICE == \'MIC_AND_DESKTOP
### الإستراتيجية لنظام التشغيل Windows (الحل البديل)
تحت نظام Windows، **كابلات الصوت الافتراضية** مدمجة مع **مراقبة OBS**.

                                                          **الإعداد:**
1. **تثبيت الكابل الافتراضي:** (z. B. *VB-Cable*). إنه يعمل كـ "Unified_Sink" على نظام التشغيل Windows.
2. **مراقبة OBS:** في إعدادات OBS من خلال *Audio -> Erweitert -> Monitor-Gerät* أثناء استخدام "Virtual Cable".
3. **Mix erstellen:** Für jede Quelle in OBS (Mic, Desktop) stellst du *Erweiterten Audioeigenschaften* “Monitoring und Ausgabe”.
4. **Python:** في الإعدادات، اضبط على `AUDIO_INPUT_DEVICE = "CABLE Output"`.

                                                               ### تحليل
* **Vorteil:** OBS übernimmt das Complete Mixing. لا يوجد أي تعقيدات لبرمجة Python لنظام التشغيل Windows.
     * **المحتوى:** Der Benutzer muss OBS im Hintergrund lafen lassen.

بالنسبة لمستخدم Windows، يجب أن يكون هذا هو الطريق الثابت.

**الحصول على Windows (PowerShell) من أسماء الكابلات:**
                  "احصل على قائمة الأجهزة الصوتية".
                     *(Hinweis: Erfordert oft das AudioDeviceCmdlets-Modul).*