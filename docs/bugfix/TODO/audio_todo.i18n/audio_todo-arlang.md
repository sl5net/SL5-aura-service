31.12.\'25 18:25 الأربعاء

تفاصيل المهام وقائمة المهام الخاصة بالمهام:

### التوثيق: Ver such "إدخال الصوت الموحد" (ميكروفون + سطح المكتب)
**الحالة:** Pausiert (إثبات المفهوم موجود، aber nicht Stabil/performant).

                                         **التعريف / النتائج:**
* **التوجيه:** يتم توصيل PipeWire/PulseAudio بـ Python-Stream (ALSA-Bridge) عبر الميكروفون الفيزيائي القياسي (Stream-Restore-Logik).
* **الأداء:** يتم تشغيل RMS وVAD وVosk في حلقة واحدة، مدمجة مع `pactl`-Aufrufen الخارجية، مما يساعد على تشغيل وحدة المعالجة المركزية (CPU) الأخيرة.
* **الإشارة:** كان فهرس الأجهزة الصحيح في كثير من الأحيان مجرد RMS-Pegel من ~1.7 عامًا، وكان عبارة عن رسم خرائط خاطئ لـ ALSA و PipeWire.

                                                                          ---

                      ### قائمة المهام (سباق المستقبل)
1. **[ ] تكامل WirePlumber:** تم تنفيذه من خلال قواعد PipeWire الأصلية (`البرامج النصية`)، وهو عبارة عن دفق دائم من خلال `pactl` -Hooks zu binden.
2. **[ ] تحسين الأداء:** يتم تحديث حلقة الصوت (z.B. RMS-Checks اختيارية أثناء التشغيل أو تحسين معلمة VAD).
3. **[ ] حوض أحادي أصلي:** آمن، هذا النظام الرائع للحوض يعمل على 16 كيلو هرتز أحادي، مما يسمح بإعادة أخذ العينات لآخر مرة.
4. **[ ] رسم خرائط قوي للأجهزة:** يمكنك العثور على طريقة ثابتة، مما يتيح لك الوصول إلى جهاز مراقبة رائع في "جهاز الصوت".

                                                                          ---

                                          ### تحديث `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

                                                       **[EN] الملخص:**
تمت محاولة دمج صوت الميكروفون وصوت سطح المكتب باستخدام ``null-sink`` الافتراضي. كان التوجيه غير مستقر بسبب استعادة الدفق في PipeWire. وقد لوحظ ارتفاع تحميل وحدة المعالجة المركزية. تم الآن توثيق المنطق للتكرار المستقبلي.

Ich bin gespannt, ob wir bei einem späteren Ver such mit einer Performance Lösung (مباشرة مباشرة عبر PipeWire-Schnittstellen) لديها عمل! Erledigt für heute.