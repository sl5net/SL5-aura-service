# SL5 Aura – اختبارات انحدارات الصوت: Statusbericht

                                     **المرجع:** 14-03-2026XSPACEbreakX
**التاريخ:** `scripts/py/func/checks/test_youtube_audio_regression.py`

                                                                          ---

                                                    ## 1. كان رائعًا

                                              نظام اختبار واحد:
1. مقطع صوتي من رابط فيديو YouTube (عبر `yt-dlp` + `ffmpeg`)
2. إنشاء مقطع YouTube-Transcript تلقائيًا بشكل مباشر (عبر `youtube-transcript-api`)
                               3. يتم نسخ الصوت من خلال Vosk
4. اختياري من نوع Ergebnis durch **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. معدل خطأ الكلمات (WER) zwischen Aura-Output وYouTube-Transcript berechnet
          6. من أجل اختبار الانحدارات التلقائية

جميع التنزيلات werden gecacht (`scripts/py/func/checks/fixtures/youtube_clips/`)،sodass Folgetests schnell laufen.

                                                                          ---

                                                             ## 2. داتين

                                                      | داتي | زويك |
                                                                    |---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | هاوبتيستداتي |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte مقاطع صوتية |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | مخطوطات Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | ذاكرة التخزين المؤقت من Git ausschließen |
       | `conftest.py` (جذر الريبو) | Setzt PYTHONPATH für pytest |

                                                                          ---

                                                  ## 3. اختبار مودي

                        ### الوضع أ – Vosk فقط (خط الأساس)
```python
YoutubeAudioTestCase(
    test_id       = "mein_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
                 اختبار الجودة فقط. كين هالة. شنيل.

            ### الوضع B – خط أنابيب Volle Aura، WER-Vergleich
```python
YoutubeAudioTestCase(
    test_id            = "mein_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # strenger — Aura soll besser sein als Vosk
    test_aura_pipeline = True,
)
```
Schickt Vosk-Output من خلال FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### الوضع C – خط أنابيب كامل للهالة، خرج فائق
```python
YoutubeAudioTestCase(
    test_id            = "befehl_terminal_oeffnen",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",  # Aura muss genau das ausgeben
)
```
Für Segmente wo ein bekannter Befehl gesprochen wird. اختبار شارفستر.

                                                                          ---

                                        ## 4. لم يكن الأمر كذلك

                                              | كان | جيتيستيت؟ |
                                                                    |---|---|
                                                  | جودة Vosk STT | ✅ |
   | FuzzyMap ما قبل إعادة التنظيم | ✅(wenn Aura läuft) |
                           | LanguageTool-Korrekturen | ✅(wenn LT läuft) |
        | FuzzyMap بعد إعادة التنظيم | ✅(wenn Aura läuft) |
| إخراج لوحة المفاتيح (AutoHotkey/CopyQ) | ❌ رائع — OS-Ebene، keine Logik |
| تحميل نموذج فوسك | ❌ — Aura هي أحدث بيانات الإخراج، والتي لا تحتاج إلى نموذج جديد |

يتم إخراج الإخراج من `tts_output_*.txt` في درجة الحرارة المحددة - صحيح تمامًا كما أن Aura متدربة، وليست من المحطة الطرفية.

                                                                          ---

                                                               ## 5. ابدأ

                ### نورمالر تيستلوف (Aura muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

                                                ### سجل ميت فوليم:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

                                  ### اختبارات نور بيستيمت:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

                                   ### Aura + LT البداية الأولى:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

                                                                          ---

                                                    ## 6. تكوين Wichtige

                              ### Sprachcodes — نظام zwei verschiedene!

                                 | النظام | الكود | بيسبيل |
                                                                |---|---|---|
| فوسك-موديل-أوردنر | `دي` | `نماذج/فوسك-موديل-دي-0.21` |
        | هالة FuzzyMap-Ordner | `دي دي` | `config/maps/.../de-DE/` |
  | يوتيوب نسخة API | `دي` | `api.fetch(..., languages=["de"])` |

**Lösung im Code:** `language="de-DE"` setzen. يعمل الرمز تلقائيًا:
                   - لفوسك: `"de-DE"` → `"de"` (مقسمة على `-`)
          - من أجل YouTube: `"de-DE"` → `"de"` (مقسمة على `-`)
                                    - فور هالة: `"de-DE"` مباشرة

         ### تفعيل المترجم التلقائي للاختبارات:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
 Sonst übersetzt Aura deutschen Text in English — das verfälscht den WER.

                                                                          ---

                                        ## 7. مشكلة Bekannte & Lösungen

                             | مشكلة | أورساتشي | لوسونج |
                                                                |---|---|---|
| `تخطي` sofort | YouTube-Transcript nicht gefunden | `api.list(\'video_id')` يوفر لك كلمات واسعة النطاق |
| ``تم تخطي`` بعد الصوت | Vosk-Modell nicht gefunden | `language.split("-")[0]` الكود الاحتياطي |
| `تم العثور على 0 قواعد FUZZY_MAP_pre` | Falscher Sprachcode وهالة | تم استخدام `"de-DE"` statt `"de"` |
| `تم رفض الاتصال 8010` | LT لم يقم بالبدء | الهالة الأولى تبدأ، فترة الستينيات |
| `zsh: تم الإنهاء` | X11-الوكالة الدولية للطاقة قتلت Prozess | `SDL_VIDEODRIVER=dummy` verwenden; الوكالة الدولية للطاقة Schwellenwert erhöhen |
| يوتيوب `>>` علامة | Zweitsprecher im Transcript | `re.sub(r\'>>', '', text)` - فقط `>>` أدخل، Wörter behalten |
| `خطأ في السمة: get_transcript` | يوتيوب-ترانسكريبت-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` طريقة الفصل الدراسي |
| تقوم ذاكرة التخزين المؤقت بقراءة النص | تغيير لوف مع kaputtem Regex | `rm Installations/youtube_clips/*.transcript.json` |

                                                                          ---

                                                   ## 8. Ergebnisse bis jetzt

### الفيديو: `sOjRNICiZ7Q` (باللغة الألمانية)، الجزء 5-20 ثانية

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

                                                  **بوباتشتونجن:**
- Aura hat eine Regel angewendet: `إصبع الأصابع` → `10 أصابع` ✅
     - LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am Segment: YouTube-Transcript beginnt mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

                                                                          ---

                                     ## 9.Empfehlungen für nächste Schritte

1. **القطاعات الصغيرة** — `ffplay` في ثانية واحدة لتجد ما يوجه إليك
2. **LT-Status قيد الاختبار** — `curl http://localhost:8010/v2/languages` للاختبار
3. ** متابعة اختبارات الوضع C ** — الجزء الذي سيتم تحديده بالكامل (`المخرج_المتوقع`)

                                                                          ---
                                                                          ---

# SL5 Aura – اختبارات الانحدار الصوتي: تقرير الحالة

                                   **التاريخ:** 14-03-2026XSPACEbreakX
    **الملف:** `scripts/py/func/checks/test_youtube_audio_regression.py`

                                                                          ---

                                                   ## 1. ما تم بناؤه

                                          نظام الاختبار الذي:
1. تنزيل مقطع صوتي من مقطع فيديو على YouTube (عبر `yt-dlp` + `ffmpeg`)
2. جلب نص YouTube الذي تم إنشاؤه تلقائيًا لنفس المقطع (عبر "youtube-transcript-api")
                           3. يقوم بنسخ الصوت من خلال Vosk
4. قم بتمرير النتيجة بشكل اختياري عبر **مسار Aura الكامل** (`process_text_in_background`)
5. يحسب معدل خطأ الكلمات (WER) بين إخراج Aura ونص YouTube
               6. يعمل كاختبار انحدار آلي عبر `pytest`

يتم تخزين جميع التنزيلات مؤقتًا (`scripts/py/func/checks/fixtures/youtube_clips/`) بحيث تكون عمليات التشغيل اللاحقة سريعة.

                                                                          ---

                                                         ## 2. الملفات

                                                      | ملف | الغرض |
                                                                    |---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | ملف الاختبار الرئيسي |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | مقاطع صوتية مخبأة |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | النصوص المخزنة مؤقتا |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | استبعاد ذاكرة التخزين المؤقت من Git |
    | `conftest.py` (جذر الريبو) | يضبط PYTHONPATH لـ pytest |

                                                                          ---

                                            ## 3. أوضاع الاختبار

                        ### الوضع أ – Vosk فقط (خط الأساس)
```python
YoutubeAudioTestCase(
    test_id       = "my_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
      اختبارات الجودة فوسك فقط. لا هالة. سريع.

  ### الوضع B – خط أنابيب Aura الكامل، مقارنة WER
```python
YoutubeAudioTestCase(
    test_id            = "my_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # stricter — Aura should improve on Vosk
    test_aura_pipeline = True,
)
```
يرسل إخراج Vosk من خلال FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### الوضع C - خط أنابيب Aura الكامل، تطابق تام للمخرجات
```python
YoutubeAudioTestCase(
    test_id            = "command_open_terminal",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",   # Aura must produce exactly this
)
```
للمقاطع التي تحتوي على أمر صوتي معروف. وضع الاختبار الأكثر صرامة.

                                                                          ---

             ## 4. ما تم اختباره وما لم يتم اختباره

                                         | ماذا | تم اختباره؟ |
                                                                    |---|---|
                                              | جودة فوسك STT | ✅ |
| القواعد المسبقة لـ FuzzyMap | ✅(عند تشغيل الهالة) |
           | تصحيحات أداة اللغة | ✅(عند تشغيل LT) |
   | قواعد مشاركة FuzzyMap | ✅(عند تشغيل الهالة) |
| إخراج لوحة المفاتيح (AutoHotkey/CopyQ) | ❌ مقصود — مستوى نظام التشغيل، بدون منطق |
| إعادة تحميل موديل فوسك | ❌ — Aura تقرأ ملف الإخراج، ولا تعيد تحميل النموذج |

تتم قراءة الإخراج من `tts_output_*.txt` في دليل مؤقت - تمامًا كما تفعل Aura داخليًا، وليس من الوحدة الطرفية.

                                                                          ---

                                                  ## 5. أوامر البدء

### تشغيل اختباري عادي (يجب أن تكون Aura قيد التشغيل بالفعل):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

                                            ### مع السجل الكامل:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

                                      ### اختبارات محددة فقط:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

                                ### ابدأ تشغيل Aura + LT أولاً:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

                                                                          ---

                                              ## 6. التكوين المهم

                       ### رموز اللغة - نظامان مختلفان!

                                     | النظام | الكود | مثال |
                                                                |---|---|---|
| مجلد نموذج فوسك | `دي` | `نماذج/فوسك-موديل-دي-0.21` |
          | مجلد Aura FuzzyMap | `دي دي` | `config/maps/.../de-DE/` |
  | يوتيوب نسخة API | `دي` | `api.fetch(..., languages=["de"])` |

**الحل في الكود:** set `language="de-DE"`. يتعامل الكود تلقائيًا مع:
   - بالنسبة إلى Vosk: `"de-DE"` → `"de"` (مقسمة إلى `-`)
- بالنسبة إلى YouTube: `"de-DE"` → `"de"` (مقسمة إلى `-`)
                                        -للهالة: `"de-DE"` مباشرة

  ### تعطيل المترجم التلقائي قبل الاختبارات:
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
بخلاف ذلك، تقوم Aura بترجمة النص الألماني إلى الإنجليزية - مما يفسد قياس WER.

                                                                          ---

                       ## 7. المشكلات والحلول المعروفة

                                     | مشكلة | السبب | إصلاح |
                                                                |---|---|---|
| `تم تخطيه` فورًا | لم يتم العثور على نسخة يوتيوب | اتصل بـ `api.list(\'video_id')` لمعرفة اللغات المتاحة |
| ``تخطي`` بعد الصوت | لم يتم العثور على نموذج Vosk | `language.split("-")[0]` احتياطي في الكود |
| `تم العثور على 0 قواعد FUZZY_MAP_pre` | تم تمرير رمز لغة خاطئ إلى Aura | استخدم `"de-DE"` وليس `"de"` |
| `تم رفض الاتصال 8010` | LT لم يبدأ | ابدأ تشغيل Aura أولاً، وانتظر 60 ثانية |
| `zsh: تم الإنهاء` | عملية قتل الوكالة الدولية للطاقة X11 | استخدم `SDL_VIDEODRIVER=dummy`; رفع عتبة المراقبة |
| يوتيوب `>>` علامات | المتحدث الثاني في النص | `re.sub(r\'>>', '', text)` - أزل `>>` فقط، واحتفظ بالكلمات |
| `خطأ في السمة: get_transcript` | يوتيوب-ترانسكريبت-api v1.x | استخدم `api = YouTubeTranscriptApi(); api.fetch(...)` |
| تحتوي ذاكرة التخزين المؤقت على نص فارغ | تشغيل قديم مع regex مكسور | `rm Installations/youtube_clips/*.transcript.json` |

                                                                          ---

                                         ## 8. النتائج حتى الآن

### الفيديو: `sOjRNICiZ7Q` (الألمانية)، الجزء 5-20 ثانية

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

                                                          **ملاحظات:**
        - طبقت Aura قاعدة: `إصبع زين` → `10 أصابع` ✅
- حالة LT أثناء هذا التشغيل غير واضحة — تم رفض الاتصال
- يرجع ارتفاع WER إلى اختيار المقطع: يبدأ نص YouTube بالكلمات التي لا يستطيع Vosk سماعها (مكبر الصوت ليس في الميكروفون بعد)
- **التوصية:** قم بتحويل المقطع إلى قسم به كلام واضح

                                                                          ---

                      ## 9. الخطوات التالية الموصى بها

1. **اختر مقطعًا أفضل** — استخدم `ffplay` للعثور على اللحظة المحددة التي يكون فيها الكلام واضحًا
2. **التحقق من حالة LT قبل الاختبار** — `curl http://localhost:8010/v2/languages` قبل التشغيل
3. **إضافة اختبارات الوضع C** — المقاطع التي تحتوي على أوامر صوتية معروفة (`الإخراج_المتوقع`)