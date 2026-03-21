# Abschlussbericht: SL5 Aura – اختبار شامل

                                   **التاريخ:** 15-03-2026XSPACEbreakX
      **التاريخ:** `scripts/py/func/checks/test_trigger_end_to_end.py`

                                                                          ---

                                                          ## 1. خطة دير

هذا هو الاختبار الشامل الذي يواجه مشكلة المشكلة التالية:
                   **Bei manchen Aufnahmen fehlt das Letzte Wort im Output.**

                                      هذا الاختبار المطلوب:
             1. بيانات WAV من الميكروفونات الرائعة
2. بدأت الهالة عند اللمس /tmp/sl5_record.trigger` - بدأت في العمل بشكل صحيح
                                         3. توقف الزناد Mit zweitem
4. قم بإخراج الإخراج باستخدام نسخة YouTube-Transcript
                               5. أعشاب نبتة نهاية المطاف

                                                                          ---

                                     ## 2. كان الأمر صحيحًا ✅

                - عادت الهالة إلى الزناد بشكل فعال
                     - LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
   - `_wait_for_output()` ابحث عن القالب `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` للرجوع إلى النص المرجعي الصحيح
- إن اختبار الاختبار الكبير متين ومصمم وظيفيًا

                                                                          ---

                                         ## 3. مشكلة Das ungelöste 🔴

             ### مشكلة Kern: `manage_audio_routing\' überschreibt alles

                                     Beim Session-Start ruft Aura intern auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

          هذه الوظيفة ماكت كما كانت في البداية:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

                      **Sie löscht jeden Sink den wir vorher stellt haben.**

تم إنشاء هذا الخيار مرة أخرى على Sink weil `mode == \'SYSTEM_DEFAULT'' (غير `MIC_AND_DESKTOP`).

                                      ### فيرسوتشتي لوسونجين

                                              | فيرساتش | مشكلة |
                                                                    |---|---|
| إنشاء مصدر افتراضي لـ PulseAudio | يتجاهل PipeWire "مصدر الوحدة الظاهري" |
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Markierten Override-Block ans Ende schreiben | إعدادات ضوء الهالة ليست جديدة تمامًا لوظيفة الزناد |
| `_create_mic_and_desktop_sink()` مباشرة للاختبار | يتم استخدام `manage_audio_routing` من خلال جلسة بدء التشغيل |
| `pw-الاسترجاع` | Erscheint als Source aber Aura hört nicht darauf |

          ### لا تعمل إعدادات التجاوز `settings_local.py`

`dynamic_settings.py` يراقب البيانات ويتابعها — من خلال فاصل زمني واحد. يبدأ Der Trigger في التحرك نحو Schreiben. تبدأ الهالة في الجلسة من وقت لآخر مع `SYSTEM_DEFAULT`.

أيضًا: يتم إنشاء Sink تلقائيًا عندما تكون Aura `MIC_AND_DESKTOP`، وهي **nächsten** Session-Start — غير مريحة.

                                                                          ---

                                    ## 4. موغليش لوسونجسويغي

        ### الخيار أ — تغيير الإعدادات إلى أسفل
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
          المخاطرة: لا يوجد أي خطأ، توقيت-abhängig.

### الخيار ب — Aura neu تبدأ من خلال ضبط الإعدادات
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
Nachteil: اختبار يستغرق أكثر من 1 دقيقة. أبر زوفيرلاسيج.

### الخيار ج — `manage_audio_routing` مباشرة في الاختبار
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
هناك أيضًا Sink قبل تشغيل Trigger — و `manage_audio_routing` أثناء جلسة بدء التشغيل `is_mic_and_desktop_sink_active() == True` وتنشيط الإعداد.

                            Das ist wahrscheinlich die **sauberste Lösung**.

### الخيار د — `process_text_in_background` متاح مباشرة (kein Trigger)
كما هو الحال في `test_youtube_audio_regression.py` — Vosk-Output يتم توجيهه مباشرة إلى خط الأنابيب، من خلال آلية الزناد الصحيحة. لن نختبر خط الأنابيب أبدًا من حيث المبدأ.

           ### الخيار E — Aura مع `run_mode_override=TEST` يبدأ
يعد Falls Aura أحد طرق الاختبار الخاصة بتوجيه الصوت.

                                                                          ---

                                                     ## 5. امبلهلونج

**الخيار C** الأكثر اختبارًا - آلة اختبار الاستيراد:

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

                                                    ما هي الوظيفة:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Dann erkennt Aura beim session-Start `is_mic_and_desktop_sink_active() == True` وآخر مرة تغرق في Ruhe.

                                                                          ---

      ## 6. هل كان اختبار ديزر لانجفريستيج بريت

                                سوبالد إير لوفت، كان رجل:
- `SPEECH_PAUSE_TIMEOUT` يتم اختبارنا (1.0، 2.0، 4.0 ثانية) ونرى ما يجب فعله.
              - `transcribe_audio_with_feedback.py` تحسين المعلمة
- يتم تحديد الانحدار عندما تنتهي معالجة الصوت
                                       - Beweisen dass ein Fix wirklich hilft

                                                                          ---

                                                                          ---

# التقرير النهائي: SL5 Aura - تشغيل الاختبار الشامل

                                   **التاريخ:** 15-03-2026XSPACEbreakX
          **الملف:** `scripts/py/func/checks/test_trigger_end_to_end.py`

                                                                          ---

                                                             ## 1. الخطة

اختبار حقيقي شامل للتحقيق في المشكلة المعروفة:
**في بعض التسجيلات، يتم قطع الكلمة الأخيرة في الإخراج.**

                                       يجب أن يكون الاختبار:
            1. قم بتغذية ملف WAV كميكروفون افتراضي
2. ابدأ تشغيل Aura عبر `touch /tmp/sl5_record.trigger` — تمامًا مثل الاستخدام الحقيقي
                                   3. توقف مع الزناد الثاني
                                  4. قارن المخرجات بنص YouTube
5. كشف ما إذا كانت هناك كلمة مفقودة في النهاية

                                                                          ---

                                             ## 2. ما تم تحقيقه ✅

                   - تستجيب الهالة للزناد بشكل صحيح
- LT قيد التشغيل ويمكن الوصول إليه (`http://127.0.0.1:8082`)
         - `_wait_for_output()` يعثر على الملف `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` يجلب النص المرجعي بشكل صحيح
- هيكل الاختبار الأساسي متين ويعمل من الناحية النظرية

                                                                          ---

                      ## 3. المشكلة التي لم يتم حلها 🔴

### المشكلة الأساسية: `manage_audio_routing` يستبدل كل شيء

               عند بدء الجلسة، تستدعي Aura داخليًا:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

                     تقوم هذه الوظيفة أولاً بما يلي:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

               **يحذف أي حوض قمنا بإنشائه مسبقًا.**

ثم لا يقوم بإنشاء مخزن جديد لأن `mode == \'SYSTEM_DEFAULT'' (وليس `MIC_AND_DESKTOP`).

                                              ### الحلول المجربة

                                                | محاولة | مشكلة |
                                                                    |---|---|
| إنشاء مصدر افتراضي لـ PulseAudio | يتجاهل PipeWire `module-virtual-source` |
| اضبط "settings_local.py" على "MIC_AND_DESKTOP" | الملف تالف مع إدخالات متعددة |
| اكتب كتلة التجاوز المحددة في نهاية الملف | لا تقوم Aura بإعادة تحميل الإعدادات بسرعة كافية قبل إطلاق النار |
| `_create_mic_and_desktop_sink()` مباشرة في الاختبار | تم الحذف بواسطة `manage_audio_routing` عند بداية الجلسة |
| `pw-الاسترجاع` | يظهر كمصدر لكن Aura لا تستمع إليه |

                                                                          ---

                        ## 4. الخطوة التالية الموصى بها

اتصل بـ "manage_audio_routing" مباشرة من الاختبار قبل المشغل:

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

عندما تبدأ Aura الجلسة، فإنها تتحقق من `is_mic_and_desktop_sink_active()` - إذا كانت `صحيح`، فإنها تتخطى الإعداد وتترك الحوض بمفرده. هذا هو الحل الأنظف.

                                                                          ---

## 5. ما سيمكن هذا الاختبار من تحقيقه على المدى الطويل

                                                   بمجرد التشغيل:
- اختبار قيم `SPEECH_PAUSE_TIMEOUT` (1.0، 2.0، 4.0 ثانية) واكتشاف قطع الكلمات
               - تحسين معلمات "transcribe_audio_with_feedback.py".
- التقاط الانحدارات عند تغيير معالجة الصوت
                       - إثبات أن الإصلاح يعمل بالفعل