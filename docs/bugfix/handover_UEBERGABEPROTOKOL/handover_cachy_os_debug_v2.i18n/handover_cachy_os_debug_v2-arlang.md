# Übergabe-Bericht v2: تصحيح أخطاء نظام CachyOS – المعالجة اللاحقة لـ Aura STT

**التاريخ:** 21 مارس 2026 (الجلسة: 20.03.14:00 – 21.03.07:00 ظهرًا)XSPACEbreakX
**المشروع:** `~/projects/py/stt` (Aura STT - نظام تحويل الصوت إلى نص دون اتصال بالإنترنت)XSPACEbreakX
**الحالة:** أكبر فورتسشريت — 4+ erfolgreiche Diktate möglich، aber noch instabilXSPACEbreakX

                                                                          ---

                             ## 1.Ausgangssituation (بداية الجلسة)

                     لا تعمل وظيفة **CachyOS** على أي شيء:
                            - Keine Rechtschreibkorrektur عبر LanguageTool
                                                 - Keine Regex-Regeln griffen
                                 - Aura stürzte nach erstem Diktat sofort ab
                                  - CPU dauerhaft bei 100%, Lufter auf Volgas

        تعمل جميع وظائف **Manjaro وWindows** برمز محدد.

                                                                          ---

                  ## 2. مشكلة Gelöste (في Reihenfolge der Entdeckung)

                           ### ✅ المشكلة 1: Falsches venv beim Start
    **التاريخ:** `scripts/activate-venv_and_run-server.sh`XSPACEbreakX
**Ursache:** `python3 -m venv .env` كلمة لـ `python3 -m venv .venv` ausgeführt → falsches venv، fehlende PaketeXSPACEbreakX
                    **الإصلاح:** Zeile `python3 -m venv .env` entfernt

                                                                          ---

                      ### ✅ المشكلة 2: Vosk Double-Free (glibc 2.43)
**Ursache:** Vosk 0.3.45 يحتوي على خطأ مزدوج مجاني. تم تحديث glibc 2.43 على CachyOS وإنهاء العملية. مانجارو/ältere glibc ignierte es لا يزال.XSPACEbreakX
                  **الإصلاح:** mimalloc als البديل المخصص:
```bash
sudo pacman -S mimalloc
```
الآن يتم تنفيذ برنامج Startskript — مثل هذا تلقائيًا بعد `/usr/lib/libmimalloc.so`.

                                                            **التحقق:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

                                                                          ---

### ✅ المشكلة 3: plugins.zip Endlos-Repack-Loop (وحدة المعالجة المركزية 100%)
**Ursache:** `secure_packer_lib.py` scannte beim Timestamp-Check all Dateien in Quellverzeichnis — شامل `aura_secure.blob` (2,4 جيجابايت). Jeder Zugriff على `.blob` تحديث الوقت → الطابع الزمني الجديد مثل ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff على `.blob` → Endlosschleife.XSPACEbreakX
**الإضافة:** يتم إرسال بيانات ZIP في عمليات المسح الضوئي إلى Wachstum المتكررة.XSPACEbreakX
      **الإصلاح:** `scripts/py/func/secure_packer_lib.py`، Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

                                                                          ---

### ✅ المشكلة 4: اختبارات e2e beim Start (89توازي Prozesse)
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen، startete 89 المتوازي Prozesse → Lüfter، CPU-Last، Absturz wenn erster Test fehlschlug.XSPACEbreakX
            **الإصلاح:** `aura_engine.py` رقم 1167-1168 تعليق:
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

                                                                          ---

                  ### ✅ المشكلة 5: "أو صحيح" Window-Title-Spam
       **Datei:** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE أو True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/SekundeXSPACEbreakX
                                                                **يصلح:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

                                                                          ---

         ### ✅ المشكلة 6: Gefährliche Regeln في فارغ_الكل
**التاريخ:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**المفتاح:** نشط (ليس هناك تعليق) قم بتسجيل **المحتوى** النص مفتوح:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungenXSPACEكسرX
**الإصلاح:** جميع التعليقات المتعلقة باللعبة متاحة. Nur `LECKER_EXAKT` (harmlos) blieb aktiv.

                                                                          ---

  ### ✅ المشكلة 7: pygame Segfault (خيط قياسي غير آمن)
**Ursache:** `SafeStreamToLogger.write()` schrieb `self.terminal.write(buf)` من خلال قفل الموضوع. يعمل نظام CachyOS (جدولة الخيوط العدوانية) على تعطيل pygame من خلال تقليص حجم Zugriff من خلال Threads.XSPACEbreakX
                                                   **تتبع المكدس:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
          **الإصلاح:** `aura_engine.py`، فئة `SafeStreamToLogger`:
```python
def __init__(self, ...):
    ...
    self._lock = threading.Lock()  # NEU

def write(self, buf):
    ...
    with self._lock:               # NEU
        self.terminal.write(buf)
```

                                                                          ---

                         ### ✅ المشكلة 8: os.path.relpath() Segfault
      **التاريخ:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` Triggerte intern stdout → pygame Segfault aus ThreadXSPACEbreakX
                                                                **يصلح:**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

                                                                          ---

                                                ## 3. منصة أكتويلر

هالة ترفرف على CachyOS ويمكن **4+ إملاء تلميحات** erfolgreich verarbeiten:
                                          - ✅ وظيفة Vosk-Transkription
                                          - ✅ ضبط وظيفةXSPACEbreakX
                  - ✅ LanguageTool-Korrektur funktioniert (Großschreibung)
                                   - ✅ نص wird geschrieben und gesprochen
                              - ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

                                                                          ---

## 4. مشكلة لا توجد مخالفات: تحطم ستيلر بعد 1-5 إملاءات

**العَرَض:** هالة ستيربت من خلال Segfault في stderr، لا يمكن نطقها باستخدام شريط Python-Traceback.

               **رسالة إلى Stack vor Crash (من früherem stderr):**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

                                                **Wahrscheinliche Ursachen:**
1. المزيد من الخيوط غير الآمنة في `SafeStreamToLogger` (z.B. `self.file_handler_ref.handle(record)`)
2. استثناء غير قابل للتنفيذ في الخلفية - لا يزال مؤشر الترابط متوقفًا
3. مهمة الصيانة (`trigger_aura_maintenance.py`) بدأت في بدء العملية الفرعية وتعطلت

                                                  ** تشخيص Nächster: **
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**النجمة الحقيقية الأكثر** — `is_logging` العلم ليس آمنًا للخيط:
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
                                                                    بيسر:
```python
with self._lock:
    if buf and not buf.isspace() and not self.is_logging:
        self.is_logging = True
        try:
            ...
        finally:
            self.is_logging = False
```

                                                                          ---

                           ## 5. مشكلة Weitere bekannte (nicht kritisch)

                                       ### أخطاء اتصال أولاما
لم يتم تشغيل الاتصال على CachyOS → `z_fallback_llm/ask_ollama.py` إنتاج عدد كبير من Fehler-Logs.  
                                                         تعطيل مؤقت:
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

            ### الإضافات/ Verzeichnis zu groß (2,8 جيجابايت)
تأمين البيانات - بيانات ZIP والنسخ الاحتياطية الأخرى.

                ### DEV_MODE_all_processing vs settings.DEV_MODE Inkonsistenz
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` يخفي الضوء الزائف. لا داعي للقلق.

                  ### خطأ في الاسم في الخرائط الخاصة
`_apply_fix_name_error(\'FUZZY_MAP.py' None ...)` أكمل كل الإملاء — خطأ في الاسم يتم تصحيحه تلقائيًا في خريطة خاصة. كين أبستورز، لا يمكن أن يكون مستقرًا.

                                                                          ---

                          ## 6. جياندرتي داتين (Zusammenfassung)

                                                | داتي | أندرونج |
                                                                    |---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` و `.zip` من مسح الطابع الزمني |
| `aura_engine.py` | e2e-Test auskommentiert; "threading.Lock" في "SafeStreamToLogger"؛ `أو صحيح` entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (مؤقت لتصحيح الأخطاء) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | قم بتعليق كل ما يتعلق بالصيد الشامل |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | محيط بـ `.py_bak` |

                                                                          ---

                    ## 7. الملف التمهيدي جاهز للتشغيل

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
       الالتزام: ``CachyOS محدود في الوقت الحالي\''

                                                                          ---


Auf CachyOS هو نظام pygame\'s stdout-Ersatz غير آمن للخيوط.
                                           Der Fix is ist ein threading Lock:
                                        bashsed -n \'418,422p' aura_engine.py



                                          ## 8. هيلفريتش بيفيهل

```bash
# Aura starten:
~/projects/py/stt/scripts/restart_venv_and_run-server.sh

# Crash-Log:
cat /tmp/aura_stderr.log | tail -30

# CPU-Verbrauch prüfen:
top -b -n 1 | head -15

# Hintergrundprozesse nach Crash killen:
pkill -f gawk; pkill -f translate_md; pkill -f maintenance

# mimalloc aktiv? (in Konsole beim Start sichtbar):
# "Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so)."

# Alle Prozesse nach Crash killen:
pkill -9 -f aura_engine; pkill -9 -f python3
```

                                                                          ---

*تم التحديث حاليًا في 21.03.2026 الساعة 07:00 صباحًا — جلسة تصحيح الأخطاء مع Claude Sonnet 4.6*XSPACEbreakX
                                          *جلسة داور: ~17 مذهلة*