# إجراءات القاعدة المتقدمة: تنفيذ نصوص بايثون

يصف هذا المستند كيفية توسيع وظيفة قواعد استبدال النص البسيطة عن طريق تنفيذ برامج Python النصية المخصصة. تتيح لك هذه الميزة القوية إنشاء استجابات ديناميكية، والتفاعل مع الملفات، واستدعاء واجهات برمجة التطبيقات الخارجية، وتنفيذ منطق معقد مباشرةً ضمن سير عمل التعرف على الكلام.

                            ## المفهوم الأساسي: `on_match_exec`

بدلاً من مجرد استبدال النص، يمكنك الآن إخبار القاعدة بتنفيذ واحد أو أكثر من برامج Python النصية عندما يتطابق نمطها. ويتم ذلك عن طريق إضافة مفتاح `on_match_exec` إلى قاموس خيارات القاعدة.

تتمثل المهمة الأساسية للبرنامج النصي في تلقي معلومات حول المطابقة وتنفيذ إجراء وإرجاع سلسلة نهائية سيتم استخدامها كنص جديد.

                                                  ### هيكل القاعدة

تبدو القاعدة التي تحتوي على إجراء البرنامج النصي كما يلي:

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
                                         ** النقاط الرئيسية: **
              - يجب أن تكون قيمة `on_match_exec` **قائمة**.
- توجد البرامج النصية في نفس الدليل الذي يوجد به ملف الخريطة، ولهذا السبب فإن `CONFIG_DIR / \'script_name.py'` هي الطريقة الموصى بها لتحديد المسار.

                                                                          ---

                    ## إنشاء برنامج نصي قابل للتنفيذ

لكي يستخدم النظام البرنامج النصي الخاص بك، يجب أن يتبع قاعدتين بسيطتين:
1. يجب أن يكون ملف Python صالحًا (على سبيل المثال، `my_script.py`).
  2. يجب أن يحتوي على دالة اسمها "execute(match_data)".

                                    ### الدالة `تنفيذ(match_data)`

هذه هي نقطة الدخول القياسية لجميع البرامج النصية القابلة للتنفيذ. سيقوم النظام تلقائيًا باستدعاء هذه الوظيفة عندما تتطابق القاعدة.

- **`match_data` (dict):** قاموس يحتوي على كافة السياقات المتعلقة بالمطابقة.
- **قيمة الإرجاع (str):** الدالة **يجب** أن ترجع سلسلة. ستصبح هذه السلسلة النص المعالج الجديد.

                                                 ### قاموس "match_data".

هذا القاموس هو الجسر بين التطبيق الرئيسي والبرنامج النصي الخاص بك. ويحتوي على المفاتيح التالية:

* `\'original_text'' (str): السلسلة النصية الكاملة *قبل* تطبيق أي استبدال من القاعدة الحالية.
* `\'text_after_replacement'` (str): النص *بعد* تم تطبيق سلسلة الاستبدال الأساسية للقاعدة، ولكن *قبل* تم استدعاء البرنامج النصي الخاص بك. (إذا كان الاستبدال `لا شيء`، فسيكون هذا هو نفس `النص_الأصلي`).
* `\'regex_match_obj'' (re.Match): كائن مطابقة regex الرسمي لـ Python. يعد هذا أمرًا قويًا للغاية للوصول إلى **مجموعات الالتقاط**. يمكنك استخدام `match_obj.group(1)`، و`match_obj.group(2)`، وما إلى ذلك.
* `\'rule_options'' (dict): قاموس الخيارات الكامل للقاعدة التي أدت إلى تشغيل البرنامج النصي.

                                                                          ---

                                                                ## أمثلة

### مثال 1: الحصول على الوقت الحالي (الاستجابة الديناميكية)

يعرض هذا البرنامج النصي تحية مخصصة بناءً على الوقت من اليوم.

                          **1. القاعدة (في ملف الخريطة):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

                  **2. البرنامج النصي (`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
                                                    ** الاستخدام: **
                        > **الإدخال:** "ما هو الوقت الآن"
    > **النتيجة:** "مساء الخير! الساعة الآن 14:30."

### المثال 2: حاسبة بسيطة (باستخدام مجموعات الالتقاط)

يستخدم هذا البرنامج النصي مجموعات الالتقاط من التعبير العادي لإجراء عملية حسابية.

                          **1. القاعدة (في ملف الخريطة):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

                        **2. البرنامج النصي (`calculator.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
                                                    ** الاستخدام: **
                              > **الإدخال:** "احسب 55 زائد 10"
                              > **الإخراج:** "النتيجة هي 65."

### المثال 3: قائمة التسوق المستمرة (إدخال/إخراج الملف)

يوضح هذا المثال كيف يمكن لبرنامج نصي واحد التعامل مع أوامر متعددة (الإضافة والإظهار) عن طريق فحص النص الأصلي للمستخدم، وكيف يمكنه الاحتفاظ بالبيانات عن طريق الكتابة إلى ملف.

                          **1. القواعد (في ملف الخريطة):**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

                         **2. النص البرمجي (`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
                                                    ** الاستخدام: **
 > **الإدخال 1:** "أضف الحليب إلى قائمة التسوق"
> **النتيجة 1:** "حسنًا، لقد أضفت "الحليب" إلى قائمة التسوق."
                                                                            >
                 > **الإدخال 2:** "إظهار قائمة التسوق"
        > **النتيجة 2:** "في القائمة لديك: الحليب."

                                                                          ---

                                               ## أفضل الممارسات

- **وظيفة واحدة لكل برنامج نصي:** حافظ على تركيز البرامج النصية على مهمة واحدة (على سبيل المثال، يقوم `calculator.py` بالحساب فقط).
- **معالجة الأخطاء:** قم دائمًا بلف منطق البرنامج النصي الخاص بك في كتلة `محاولة...باستثناء` لمنعه من تعطل التطبيق بأكمله. قم بإرجاع رسالة خطأ سهلة الاستخدام من الكتلة "باستثناء".
- **المكتبات الخارجية:** يمكنك استخدام المكتبات الخارجية (مثل `الطلبات` أو `wikipedia-api`)، ولكن يجب عليك التأكد من تثبيتها في بيئة Python الخاصة بك (`pip install <library-name>`).
- **الأمان:** انتبه إلى أن هذه الميزة يمكنها تنفيذ أي كود بايثون. استخدم فقط البرامج النصية من مصادر موثوقة.