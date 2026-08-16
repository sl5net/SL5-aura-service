# أبرز الميزات: تحميل الخريطة الخاصة الآمنة والتعبئة التلقائية

يوضح هذا المستند بنية إدارة المكونات الإضافية الحساسة للخرائط (على سبيل المثال، بيانات العميل والأوامر الخاصة) بطريقة تسمح بـ **التحرير المباشر** مع فرض **أفضل ممارسات الأمان** لمنع التعرض غير المقصود لـ Git.

                                                                          ---

                           ## 1. المفهوم: أمن "ماتريوشكا".

لضمان أقصى قدر من الخصوصية أثناء استخدام الأدوات القياسية، تستخدم Aura استراتيجية تداخل **Matryoshka (الدمية الروسية)** للأرشيفات المشفرة.

1. **الطبقة الخارجية:** ملف ZIP قياسي مشفر باستخدام **AES-256** (عبر أمر `zip` الخاص بالنظام).
* *المظهر:* يحتوي على ملف **واحد** فقط اسمه `aura_secure.blob`.
* *الفائدة:* يخفي أسماء الملفات وبنية الدليل من أعين المتطفلين.
2. **الطبقة الداخلية (النقطة):** حاوية ZIP غير مشفرة داخل النقطة.
* *المحتوى:* بنية الدليل الفعلي وملفات بايثون.
3. **حالة العمل:** عند إلغاء القفل، يتم استخراج الملفات إلى مجلد مؤقت تسبقه شرطة سفلية (على سبيل المثال، `_خاص`).
* *الأمان:* يتم تجاهل هذا المجلد تمامًا بواسطة `.gitignore`.

                                                                          ---

                                           ## 2. سير العمل الفني

                           ### أ. البوابة الأمنية (البدء)
قبل تفريغ أي شيء، تتحقق Aura من `scripts/py/func/map_reloader.py` بحثًا عن قواعد `.gitignore` المحددة.
* **القاعدة 1:** `config/maps/**/.*` (يحمي الملفات الرئيسية)
   * **القاعدة 2:** `config/maps/**/_*` (يحمي أدلة العمل)
إذا كانت هذه العناصر مفقودة، فسيتم إحباط النظام **.

             ### ب. التفريغ (المدفوع بالاستثناءات)
1. يقوم المستخدم بإنشاء ملف مفتاح (على سبيل المثال، `.auth_key.py`) يحتوي على كلمة المرور (في نص عادي أو تعليقات).
2. تكتشف Aura هذا الملف والملف المضغوط المقابل (على سبيل المثال، `private.zip`).
3. تقوم Aura بفك تشفير الرمز البريدي الخارجي باستخدام المفتاح.
4. تكتشف Aura `aura_secure.blob`، وتستخرج الطبقة الداخلية، وتنقل الملفات إلى دليل العمل `_private`.

### ج. التحرير المباشر والتعبئة التلقائية (الدورة)
هذا هو المكان الذي يصبح فيه النظام "الشفاء الذاتي":

 1. **تحرير:** يمكنك تعديل ملف في `_private/` وحفظه.
2. **المشغل:** تكتشف Aura التغيير وتعيد تحميل الوحدة.
3. **خطاف دورة الحياة:** تقوم الوحدة بتشغيل وظيفة `on_reload()` الخاصة بها.
4. **SecurePacker:** يتم تنفيذ البرنامج النصي (`secure_packer.py`) في جذر المجلد الخاص:
* يقوم بإنشاء الرمز البريدي الداخلي (الهيكل).
                         * يقوم بإعادة تسميته إلى `.blob`.
* يقوم باستدعاء أمر النظام "zip" لتشفيره في الأرشيف الخارجي باستخدام كلمة المرور من ملف ".key".

**النتيجة:** يكون ملف `private.zip` الخاص بك محدثًا دائمًا بأحدث التغييرات، ولكن Git لا يرى سوى تغيير ملف ZIP الثنائي.

                                                                          ---

                                                ## 3. دليل الإعداد

                                    ### الخطوة 1: بنية الدليل
                           قم بإنشاء بنية مجلد مثل هذا:
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

                   ### الخطوة 2: ملف المفتاح (`.auth_key.py`)
                                             يجب أن تبدأ بنقطة.
```python
# MySecretPassword123
# This file is ignored by Git.
```

      ### الخطوة 3: برنامج Packer النصي (`secure_packer.py`)
ضع هذا البرنامج النصي داخل مجلد الخريطة الخاصة بك (قبل ضغطه في البداية). يتعامل مع منطق التشفير. تأكد من أن خرائطك تستدعي هذا البرنامج النصي عبر الخطاف `on_reload`.

                                  ### الخطوة 4: تنفيذ الخطاف
في ملفات الخريطة (`.py`)، أضف هذا الخطاف لتشغيل النسخة الاحتياطية عند كل عملية حفظ:

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

                                                                          ---

                               ## 4. حالة البوابة والسلامة

عند الإعداد بشكل صحيح، ستعرض `git Status` **فقط**:
```text
modified:   config/maps/private/private_maps.zip
```
لا يتم تعقب المجلد `_private_maps` والملف `.auth_key.py` أبدًا.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# دليل المطور: خطافات دورة حياة البرنامج المساعد

يسمح Aura SL5 للمكونات الإضافية (الخرائط) بتعريف "خطافات" محددة يتم تنفيذها تلقائيًا عندما تتغير حالة الوحدة. يعد هذا أمرًا ضروريًا لسير العمل المتقدم مثل نظام **الخريطة الخاصة الآمنة**.

                                                ## الخطاف `on_reload()`

تعتبر وظيفة `on_reload()` وظيفة اختيارية يمكنك تحديدها في أي وحدة خريطة.

                                                                 ### سلوك
* **المشغل:** يتم تنفيذه مباشرة بعد نجاح الوحدة **إعادة التحميل السريع** (تعديل الملف + المشغل الصوتي).
* **السياق:** يتم تشغيله ضمن سلسلة رسائل التطبيق الرئيسية.
* **السلامة:** ملفوفة في كتلة `محاولة/باستثناء`. سيتم تسجيل الأخطاء هنا ولكنها لن تؤدي إلى تعطل التطبيق.

                         ### نمط الاستخدام: "سلسلة ديزي"
بالنسبة للحزم المعقدة (مثل الخرائط الخاصة)، غالبًا ما يكون لديك العديد من الملفات الفرعية، ولكن يجب أن يتعامل برنامج نصي مركزي واحد فقط (`secure_packer.py`) مع المنطق.

 يمكنك استخدام الخطاف لتفويض المهمة لأعلى:

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

                                              ### أفضل الممارسات
1. **حافظ على السرعة:** لا تقم بتشغيل مهام الحظر الطويلة (مثل التنزيلات الضخمة) في الخطاف الرئيسي. استخدم الخيوط إذا لزم الأمر.
2. **العجز:** تأكد من إمكانية تشغيل الخطاف عدة مرات دون كسر الأشياء (على سبيل المثال، لا تقم بإلحاق ملف إلى ما لا نهاية، أعد كتابته بدلاً من ذلك).