# ملحق تدريب لا مثيل له (`1_collect_unmatched_training`)

                                                                  ## غاية

يقوم هذا البرنامج الإضافي تلقائيًا بجمع المدخلات الصوتية غير المعروفة وإضافتها
كمتغيرات جديدة للخريطة الغامضة regex. وهذا يسمح للنظام "بالتدريب الذاتي"
بمرور الوقت من خلال التعلم من نتائج التعرف التي لا مثيل لها.

                                                           ## كيف يعمل

1. يتم تفعيل قاعدة التقاط الكل `COLLECT_UNMATCHED` في حالة عدم مطابقة أي قاعدة أخرى.
2. يتم استدعاء `collect_unmatched.py` عبر `on_match_exec` بالنص المطابق.
3. يتم توسيع التعبير العادي في الاستدعاء `FUZZY_MAP_pre.py` تلقائيًا.

                                                        ## الاستخدام

أضف قاعدة استقبال الرسائل الخاطئة هذه في نهاية أي `FUZZY_MAP_pre.py` تريد تدريبه:
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

تشير التسمية `f\'{str(__file__)}'' إلى `collect_unmatched.py` بالضبط
`FUZZY_MAP_pre.py` للتحديث — بحيث تكون القاعدة قابلة للنقل عبر أي مكون إضافي.

                                ## تعطيل البرنامج المساعد

عندما تقوم بجمع ما يكفي من بيانات التدريب، قم بتعطيلها إما عن طريق:

                          - التعليق على قاعدة الالتقاط
- إعادة تسمية المجلد باسم غير صالح (مثل إضافة مسافة)
- إزالة مجلد البرنامج المساعد من دليل "الخرائط".

                                                       ## هيكل الملف
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

                                                              ## ملحوظة

يقوم البرنامج الإضافي بتعديل `FUZZY_MAP_pre.py` في وقت التشغيل. ارتكاب المحدثة
قم بالملف بانتظام للحفاظ على بيانات التدريب التي تم جمعها.