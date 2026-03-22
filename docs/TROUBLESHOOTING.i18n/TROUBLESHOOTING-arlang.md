# استكشاف أخطاء SL5 Aura وإصلاحها

                                               ## التشخيص السريع

                                                ابدأ هنا دائمًا:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

                                                                          ---

                                ## المشكلة: الهالة لا تبدأ

**العَرَض:** لا يوجد صوت عند بدء التشغيل، ولا توجد عملية مرئية في `pgrep`.

                                            **التحقق من السجل:**
```bash
tail -30 log/aura_engine.log
```

                                           **الأسباب الشائعة:**

                                      | خطأ في السجل | إصلاح |
                                                                    |---|---|
| `ModuleNotFoundError` | قم بتشغيل برنامج الإعداد مرة أخرى: `bash setup/manjaro_arch_setup.sh` |
| `لا توجد وحدة باسم \'objgraph'' | تمت إعادة إنشاء `.venv` - أعد التثبيت: `pip install -r require.txt` |
| `العنوان قيد الاستخدام بالفعل` | إنهاء العملية القديمة: `pkill -9 -f aura_engine` |
| `لم يتم العثور على النموذج` | أعد تشغيل برنامج الإعداد لتنزيل النماذج المفقودة |

                                                                          ---

    ## المشكلة: تعطل الهالة بعد الإملاء الأول

       **العَرَض:** يعمل مرة واحدة ثم يموت بصمت.

                                                    **تحقق من stderr:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**إذا رأيت "خطأ في التجزئة" أو "مجاني مزدوج":**

هذه مشكلة معروفة في الأنظمة ذات الإصدار glibc 2.43+ (CachyOS، الأحدث Arch).

```bash
sudo pacman -S mimalloc
```

يتم استخدام mimalloc تلقائيًا بواسطة البرنامج النصي للبدء إذا كان مثبتًا. تأكد من أنه نشط — يجب أن ترى هذا عند بدء التشغيل:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

                                                                          ---

        ## المشكلة: مفتاح التشغيل لا يفعل شيئًا

**العَرَض:** تضغط على مفتاح التشغيل السريع ولكن لا يحدث شيء — لا صوت ولا نص.

**تحقق مما إذا كان مراقب الملفات قيد التشغيل:**
```bash
pgrep -a type_watcher
```

                   إذا لم يظهر أي شيء، أعد تشغيل Aura:
```bash
./scripts/restart_venv_and_run-server.sh
```

   **تحقق مما إذا كان يتم إنشاء ملف التشغيل:**
```bash
ls -la /tmp/sl5_record.trigger
```

إذا لم يتم إنشاء الملف مطلقًا، فهذا يعني أن تكوين مفتاح التشغيل السريع (CopyQ / AHK) لا يعمل.
راجع قسم إعداد مفتاح التشغيل السريع في [README.md](../../README.i18n/README-arlang.md#configure-your-hotkey).

                                                                          ---

        ## المشكلة: يظهر النص ولكن بدون تصحيحات

**العَرَض:** الإملاء يعمل ولكن كل شيء يظل صغيرًا، ولا توجد إصلاحات نحوية.

                                   **تحقق من تشغيل LanguageTool:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

إذا أدى هذا إلى إرجاع خطأ، فهذا يعني أن LanguageTool لا يعمل. هالة يجب أن تبدأ ذلك
تلقائيًا - تحقق من السجل بحثًا عن الأخطاء المتعلقة بـ LanguageTool:

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

                                **تحقق من سجل أداة اللغة:**
```bash
cat log/languagetool_server.log | tail -20
```

                                                                          ---

                       ## المشكلة: توقف الهالة في DEV_MODE

**العَرَض:** مع `DEV_MODE = 1`، تتوقف Aura بعد المشغل الأول وتتوقف
                                                          الاستجابة.

**السبب:** يؤدي ارتفاع حجم السجل من عدة سلاسل إلى زيادة التحميل على نظام التسجيل.

**الإصلاح:** إضافة عامل تصفية السجل في `config/filters/settings_local_log_filter.py`:

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

احفظ الملف — تقوم Aura بإعادة تحميل الفلتر تلقائيًا. لا حاجة لإعادة التشغيل.

                                                                          ---

## المشكلة: plugins.zip ينمو إلى ما لا نهاية / وحدة المعالجة المركزية عالية

**العَرَض:** وحدة المعالجة المركزية بنسبة 100%، والمراوح بأقصى سرعة، وينمو "plugins.zip" دون توقف.

**السبب:** يقوم برنامج التعبئة الآمنة بإعادة تجميع الملفات في حلقة لا نهائية.

**الإصلاح:** تأكد من استبعاد ملفات `.blob` و`.zip` من فحص الطابع الزمني.
          حدد "scripts/py/func/secure_packer_lib.py" حول السطر 86:

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

          إذا كان هذا السطر مفقودا، قم بإضافته.

                                                                          ---

                          ## المشكلة: عدم تفعيل القواعد

**العَرَض:** أنت تملي عبارة تشغيل ولكن القاعدة لا تفعل شيئًا.

                                             **قائمة المراجعة:**

1. هل القاعدة في الملف الصحيح؟ (`FUZZY_MAP_pre.py` = قبل LanguageTool،
                                                     `FUZZY_MAP.py` = بعد)
2. هل تم حفظ ملف الخريطة؟ يتم إعادة تحميل Aura عند الحفظ - تحقق من السجل
                                 `تم إعادة التحميل بنجاح`.
3. هل يتطابق النمط مع ما يكتبه Vosk بالفعل؟ تحقق من السجل ل
                                                       النسخ الخام:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. هل تم ضبط "فقط_في_النوافذ" والنافذة الخاطئة نشطة؟
5. هل هناك قاعدة أكثر عمومية تتطابق أولاً؟ تتم معالجة القواعد من الأعلى إلى الأسفل —
             وضع قواعد محددة قبل القواعد العامة.

                                                                          ---

                       ## جمع السجلات لتقارير الأخطاء

     عند الإبلاغ عن مشكلة، يرجى تضمين ما يلي:

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

                                                   أرسل إلى: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)