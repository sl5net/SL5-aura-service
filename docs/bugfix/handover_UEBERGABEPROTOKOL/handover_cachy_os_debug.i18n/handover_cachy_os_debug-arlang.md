# Übergabe-Bericht: تصحيح أخطاء نظام CachyOS - المعالجة اللاحقة لـ Aura STT

                              **المرجع:** 20. مارس 2026XSPACEbreakX
**المشروع:** `~/projects/py/stt` (Aura STT - نظام تحويل الصوت إلى نص دون اتصال بالإنترنت)XSPACEbreakX
**الحالة:** مشكلة لا داعي للقلق – Übergabe an nächsten MitarbeiterXSPACEbreakX

                                                                          ---

                                                    ## 1. حل المشكلة

بعد البدء في تشغيل وظائف **CachyOS** في Aura، لا يوجد شيء أكثر:

- **تصحيح الأخطاء عبر LanguageTool** لا يمكن الوصول إليها
    - **جميع ~674 Regex-Regeln** من FUZZY_MAP_pre-Dateien greifen nicht
- Vosk-Transkriptionen werden **ungefiltert and uncorrigiert** ausgegeben (alls kleingeschrieben, keine Ersetzungen)
- **يعمل كل من Manjaro وWindows** مع كود المصدر المحدد

Beispiel: Vosk liefert `"mal sehen ob es schwitzt bretzfeld"\' → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

                                                                          ---

                                                         ## 2. Systemumgebung

                               | | مانجارو ✅ | كاشيوس ⚠️ |
                                                                |---|---|---|
                                           | بايثون | 3.14.2 | 3.14.3 |
                | جافا | أوبن جي دي كيه 17 | OpenJDK 17.0.18 |
                                          | أداة اللغة | 6.6 | 6.6 |
                                              | LT-ميناء | 8082 | 8082 |
   | WatchFiles-Reloads beim Start | 0 | früher viele (inzwischen behoben) |

                                                                          ---

                            ## 3. هل كان الأمر كذلك أم لا؟

                                           ### ✅LanguageTool läuft korrekt
                                   - LT يبدأ تشغيل المنفذ 8082
- اختبار العزل مع وظيفة برمجة Python المباشرة:
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- المشكلة: LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

                                        ### ✅ الإعدادات صحيحة
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

                                               ### ✅ وظيفة Regex-Cache
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

    ### ✅ نسخة بايثون متطابقة (3.14.x بعد النظام)

                             ### ✅ inotify-Werte identisch (524288 / 16384)

                                                 ### ✅ venv-Problem behoben
                Das Startskript `activate-venv_and_run-server.sh` متضمن:
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```
حدث هذا المزدوج venv-Erstellen. Dadurch ist jetzt wieder ein Log vorhanden.

                                           ### ✅ مشكلة في السجل
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand. Gelöst durch Umleitung in Log-Datei (Empfehlung, noch nicht umgesetzt):
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

                                                                          ---

               ## 4. وظيفة خط الأنابيب (wichtig zum Verstehen)

```
Vosk (Speech-to-Text)
    ↓
process_text_in_background.py
    ↓
apply_all_rules_may_until_stable(text, GLOBAL_FUZZY_MAP_PRE, logger)
    ↓
apply_all_rules_until_stable(text, rules_map, logger)
    ↓  (gibt zurück: current_text, full_text_replaced_by_rule, skip_list, privacy_taint)
    ↓
if not regex_pre_is_replacing_all        # ← HIER wird LT blockiert
   and not is_only_number
   and 'LanguageTool' not in skip_list:
    correct_text_by_languagetool(...)    # ← wird nie erreicht
```

                                  ### Warum LT nie aufgerufen wird (bekannt):

                                     في `apply_all_rules_may_until_stable`:
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

              والمزيد مفتوح في `process_text_in_background.py`:
```python
regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe
# ...
if (not regex_pre_is_replacing_all ...):
    correct_text_by_languagetool(...)  # ← nur wenn False
```

                                            Im Log steht bei jedem Durchlauf:
```
🚀Iterative-All-Rules: full_text_replaced_by_rule='True, skip_list='[]'
```

هذه الميزة: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**هجوم:** هل تم استبدال النص الكامل بقاعدة بقاعدة CachyOS في نظام `صحيح\'، أم في Manjaro aber nicht؟

                                                                          ---

                           ## 5. تنسيق التسجيل (zum Verständnis)

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

التنسيق: `(استبدال، regex_pattern، العتبة، options_dict)`

                         تم استخدام `apply_all_rules_until_stable\':
- تطابق regex.full المترجم (current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → تطابق جزئي، setzt `full_text_replaced_by_rule` **nicht**

                                                                          ---

                                ## 6. اختبار ذاتي سهل (DEV_MODE)

Im DEV_MODE führt Aura beim ابدأ الاختبارات تلقائيًا. عوف كاشيوس:
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```

**الميزة:** نمط الاختبار هو `r\'^geht cobit einen$'` (يسمى "einen")، اختبار الإدخال ليس سوى ``geht cobit'` → هذا الاختبار الخاص لا يكتمل ولا يختص بنظام CachyOS. **Aber:** جميع الاختبارات الأخرى تعمل على CachyOS تمامًا، على Manjaro laufen sie alle durch.

                                                                          ---

                            ## 7.Der nächste Schritt: GLOBAL_debug_skip_list

تم تنشيط قائمة التصحيح العالمية هذه ``GLOBAL_debug_skip_list\''. علامة Dieser Flag gibt `print()` - يتم إرسالها مباشرة إلى النظام القياسي — وهي غير متاحة لنظام التسجيل. Das zeigt Schritt für Schritt كان في der Regelschleife passiert.

```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```

تبدأ مجموعة "True" وAura. يتم إرسال النسخة المطبوعة مباشرة إلى المحطة الطرفية.

    ### البديل: اختبار العزل المباشر من Regelengine

```python
# /tmp/test_rules.py
import sys, re
sys.path.insert(0, '/home/seeh/projects/py/stt')

# Regeln direkt laden
from config.maps.plugins.git.de_DE import FUZZY_MAP_pre  # Pfad anpassen
from scripts.py.func.process_text_in_background import apply_all_rules_until_stable
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

result = apply_all_rules_until_stable('geht cobit einen', FUZZY_MAP_pre, logger)
print('Ergebnis:', result)
```

                                                                          ---

                                           ## 8. Verdächtige Stellen im Code

                       ### 8 أ. Privacy_taint_occurred wird zu früh gesetzt
                                         في `apply_all_rules_until_stable`:
```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```
يمكن أن يتم حظر هذه السجلات ويتم إغلاقها من قبل الآخرين.

                                  ### 8ب. Zwei verschiedene Regex-Funktionen
```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```
               Unterschiedliche Signaturen – könnte zu Verwirrung führen.

                                ### 8ج. NameError-Risiko في aura_engine.py
```python
if settings.USE_EXTERNAL_LANGUAGETOOL:
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # languagetool_process ← NIE gesetzt in diesem Zweig!

if not languagetool_process:  # ← NameError wenn USE_EXTERNAL_LANGUAGETOOL=True
    sys.exit(1)
```

                                                                          ---

          ## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

                                      في "correct_text_by_languagetool.py":
- `get_lt_session_202601311817()` مرجع `_lt_session` غير موجود → `NameError` عند الغلق
 - `correct_text_by_languagetool_202601311818()` هذه نسخة حقيقية
- `adapter` مع `pool_connections=25` لم يتم استخدام الوحدة النمطية

                                                                          ---

                   ## 10. الملف التمهيدي جاهز للتشغيل

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```

       الالتزام: ``CachyOS محدود في الوقت الحالي\''

                                                                          ---

                                    ## 11. البيانات ذات الصلة

                                              | داتي | ريليفانس |
                                                                    |---|---|
        | `aura_engine.py` | Haupteinstiegspunkt، LT-Start، active_lt_url |
| `scripts/py/func/process_text_in_background.py` | خط أنابيب ريجل، LT-أوفروف |
| `scripts/py/func/start_languagetool_server.py` | LT-Start-Logik، Sentinel |
 | `scripts/py/func/correct_text_by_languagetool.py` | LT HTTP-أوفروف |
       | `scripts/py/func/config/dynamic_settings.py` | DEV_MODE محملة |
| `التكوين/الإعدادات.py` | LANGUAGETOOL_PORT=8082، CHECK_URL |
| `config/settings_local.py` | DEV_MODE=صواب/خطأ (محلي überschreiben) |
   | `config/filters/settings_local_log_filter.py` | LOG_ONLY، LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
         | `سجل/aura_engine.log` | Hauptlog (war lange leer wegen &-Bug) |
                       | `log/languagetool_server.log` | LT-خادم-سجل |

                                                                          ---

                                         ## 12. هيلفريتش بيفيهل

```bash
# Aura starten:
~/projects/py/stt/scripts/restart_venv_and_run-server.sh

# venv aktivieren (Fish):
source ~/projects/py/stt/.venv/bin/activate.fish

# LT manuell starten:
java -Xms512m -Xmx4g \
  -jar ~/projects/py/stt/LanguageTool-6.6/languagetool-server.jar \
  --port 8082 --address 127.0.0.1 --allow-origin "*" &

# LT direkt testen:
curl -s -d "language=de-DE&text=Das ist ein gross Fehler" \
  http://127.0.0.1:8082/v2/check | python3 -m json.tool

# Laufende Prozesse:
pgrep -a -f "aura\|languagetool"

# Log live verfolgen:
tail -f log/aura_engine.log
```

                                                                          ---

*تم إرساله بتاريخ 20.03.2026 — جلسة تصحيح الأخطاء مع كلود سونيت 4.6*