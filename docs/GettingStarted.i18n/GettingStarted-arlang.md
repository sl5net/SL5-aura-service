# البدء مع SL5 Aura

> **المتطلبات الأساسية:** لقد أكملت البرنامج النصي للإعداد وقمت بتكوين مفتاح التشغيل السريع الخاص بك.
               > إذا لم يكن الأمر كذلك، راجع [Installation section in README.md](../../README.i18n/README-arlang.md#installation).

                                                                          ---

## الخطوة 0: قم بتكوين مفتاح التشغيل السريع الخاص بك

                        اختر النظام الأساسي الخاص بك:

**Linux/macOS** — قم بتثبيت [CopyQ](https://github.com/hluk/CopyQ) وأنشئ أمرًا باستخدام اختصار عام:
```bash
touch /tmp/sl5_record.trigger
```

**Windows** — استخدم [AutoHotkey v2](https://www.autohotkey.com/) أو CopyQ. يتم تثبيت البرنامج النصي للإعداد تلقائيًا.
                      ملف التشغيل هو: `c:\tmp\sl5_record.trigger`

                                 > التفاصيل الكاملة: [README.md#configure-your-hotkey](../../README.i18n/README-arlang.md#configure-your-hotkey)

                                   ## الخطوة 1: إملاءك الأول

1. ابدأ تشغيل Aura (إذا لم يكن قيد التشغيل بالفعل):
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
انتظر صوت بدء التشغيل — وهذا يعني أن Aura جاهزة.

2. انقر فوق أي حقل نصي (المحرر، المتصفح، المحطة الطرفية).
3. اضغط على مفتاح التشغيل السريع الخاص بك، وقل **"Hello World"**، ثم اضغط على مفتاح التشغيل السريع مرة أخرى.
                                               4. شاهد النص يظهر.

> **لم يحدث شيء؟** تحقق من وجود أخطاء في `log/aura_engine.log`.
> الإصلاح الشائع لنظام CachyOS/Arch: `sudo pacman -S mimalloc`

                                                                          ---

           ## الخطوة الثانية: اكتب قاعدتك الأولى

                      أسرع طريقة لإضافة قاعدة شخصية:

             1. افتح `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
                       2. أضف قاعدة داخل `FUZZY_MAP_pre = [...]`:
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **حفظ** — تتم إعادة تحميل Aura تلقائيًا. لا حاجة لإعادة التشغيل.
4. قم بإملاء عبارة "hello World" وشاهدها تصبح "Hello World".

> راجع `docs/FuzzyMapRuleGuide.md` للحصول على مرجع القاعدة الكامل.

                    ### أوما مودوس (اختصار للمبتدئين)

 لا تعرف التعبير العادي حتى الآن؟ لا مشكلة.

      1. افتح أي `FUZZY_MAP_pre.py` فارغ في وضع الحماية
2. اكتب فقط كلمة واضحة في السطر الخاص بها (بدون علامات الاقتباس، بدون صف):
   ```
   raspberry
   ```
3. حفظ — يكتشف نظام الإصلاح التلقائي الكلمة المجردة تلقائيًا
                            يحوله إلى إدخال قاعدة صالح.
   4. يمكنك بعد ذلك تحرير النص البديل يدويًا.

وهذا ما يسمى **Oma-Modus** — وهو مصمم للمستخدمين الذين يريدون الحصول على نتائج بدونها
                                                  تعلم ريكس أولا.

                                                                          ---

                                       ## الخطوة 3: تعلم مع Koans

Koans عبارة عن تمارين صغيرة يعلم كل منها مفهومًا واحدًا.
إنهم يعيشون في `configmaps/koans deutsch/` و`configmaps/koans english/`.

                                                             ابدأ هنا:

                                       | المجلد | ماذا تتعلم |
                                                                    |---|---|
| `00_koan_oma-modus` | الإصلاح التلقائي، القاعدة الأولى بدون regex |
| `01_koan_erste_schritte` | القاعدة الأولى، أساسيات خطوط الأنابيب |
                        | `02_koan_listen` | العمل مع القوائم |
| `03_koan_schwierige_namen` | مطابقة غامضة للأسماء التي يصعب التعرف عليها |
          | `04_كوان_كلين_هيلفر` | اختصارات مفيدة |

يحتوي كل مجلد koan على `FUZZY_MAP_pre.py` مع الأمثلة المعلقة.
قم بإلغاء التعليق على القاعدة، ثم احفظها، ثم قم بإملاء عبارة التشغيل - تم.

                                                                          ---

                                     ## الخطوة 4: المضي قدمًا

                                                        | ماذا | أين |
                                                                    |---|---|
     | مرجع القاعدة الكاملة | `docs/FuzzyMapRuleGuide.md` |
| قم بإنشاء البرنامج المساعد الخاص بك | `docs/CreatingNewPluginModules.md` |
| تشغيل البرامج النصية لبايثون من القواعد | `docs/advanced-scripting.md` |
| DEV_MODE + إعداد مرشح السجل | `docs/Developer_Guide/dev_mode_setup.md` |
| القواعد المدركة للسياق (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |