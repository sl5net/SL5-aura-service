# 🧠 الوضع الهجين SL5 Aura: تكامل LLM المحلي

                                    **الحالة:** تجريبي/مستقر
**التكنولوجيا:** أولاما (لاما 3.2) + عملية بايثون الفرعية
                **الخصوصية:** 100% غير متصل بالإنترنت

        ## المفهوم: "المهندس المعماري والمتدرب"

تقليديا، تعتمد Aura على القواعد الحتمية (RegEx) - سريعة ودقيقة ويمكن التنبؤ بها. هذا هو **"المهندس المعماري"**. ومع ذلك، في بعض الأحيان يرغب المستخدم في طرح شيء "غامض" أو إبداعي، مثل *"أخبرني نكتة"* أو *"تلخيص هذا النص"*.

هذا هو المكان الذي يأتي فيه **المكون الإضافي LLM المحلي** (**"المتدرب"**):
1. **Aura (RegEx)** تتحقق أولاً من جميع الأوامر الصارمة ("تشغيل الأضواء"، "فتح التطبيق").
2. إذا لم يتطابق أي شيء مع **AND**/ **OR**، تم اكتشاف كلمة تشغيل محددة (على سبيل المثال، "Aura...")، فسيتم تنشيط القاعدة الاحتياطية.
3. يتم إرسال النص إلى نموذج الذكاء الاصطناعي المحلي (Ollama).
4. يتم تعقيم الاستجابة وإخراجها عبر TTS أو كتابة النص.

                                                                          ---

                                  ## 🛠 المتطلبات الأساسية

يتطلب البرنامج المساعد نسخة قيد التشغيل من [Ollama](https://ollama.com/) تعمل محليًا على الجهاز.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

                                                                          ---

                             ## 📂 ترتيب الهيكل والحمولة

يتم وضع البرنامج المساعد عمدا في المجلد `z_fallback_llm`.
نظرًا لأن Aura تقوم بتحميل المكونات الإضافية **أبجديًا**، فإن هذه التسمية تضمن تحميل قاعدة LLM **أخيرًا**. إنه بمثابة "شبكة أمان" للأوامر غير المعروفة.

                **المسار:** `config/maps/plugins/z_fallback_llm/de-DE/`

                                   ### 1. الخريطة (`FUZZY_MAP_pre.py`)

نستخدم **درجة عالية (100)** وكلمة تشغيل لإجبار Aura على تسليم السيطرة إلى البرنامج النصي.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

                                      ### 2. المعالج (`ask_ollama.py`)

             يتواصل هذا البرنامج النصي مع Ollama CLI.
**هام:** يحتوي على وظيفة `clean_text_for_typing`. غالبًا ما تحتوي مخرجات LLM الأولية على رموز تعبيرية (😂، 🚀) أو أحرف خاصة يمكنها تعطل أدوات مثل `xdotool` أو أنظمة TTS القديمة.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

                                                                          ---

                                        ## ⚙️ خيارات التخصيص

                                                  ### تغيير الزناد
قم بتعديل RegEx في `FUZZY_MAP_pre.py` إذا كنت لا تريد استخدام "Aura" ككلمة تنبيه.
* مثال لجملة شاملة حقيقية (كل شيء لا تعرفه Aura): `r\'^(.*)$'` (تنبيه: اضبط النتيجة!)

                                                ### تبديل النموذج
يمكنك بسهولة تبديل النموذج في `ask_ollama.py` (على سبيل المثال، إلى `mistral` للحصول على منطق أكثر تعقيدًا، على الرغم من أنه يتطلب المزيد من ذاكرة الوصول العشوائي).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

                                   ### موجه النظام (الشخصية)
يمكنك منح Aura شخصية عن طريق ضبط "تعليمات_النظام":
              > "أنت مساعد ساخر من فيلم خيال علمي."

                                                                          ---

                                      ## ⚠️ القيود المعروفة

1. **زمن الوصول:** قد يستغرق الطلب الأول بعد التمهيد من 1 إلى 3 ثوانٍ أثناء تحميل النموذج في ذاكرة الوصول العشوائي (RAM). الطلبات اللاحقة تكون أسرع.
2. **التعارضات:** إذا كان RegEx واسعًا جدًا (`.*`) بدون بنية مجلد مناسبة، فقد يبتلع الأوامر القياسية. الترتيب الأبجدي (`z_...`) ضروري.
3. **الأجهزة:** يتطلب تقريبًا. 2 غيغابايت من ذاكرة الوصول العشوائي المجانية لـ Llama 3.2.