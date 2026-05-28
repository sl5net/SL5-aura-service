# تكامل Trino — دليل المطور

                                                                ## بنيان
                                                   واجهات الهالة:
الكلام → INTERFACE = الكلام (الاحتياطي الافتراضي في .py)
المحطة → INTERFACE = المحطة الطرفية (موضحة في s() zshrc)
                   الويب → INTERFACE=web (موضح في start_service)
                                                                          ↓
aura_state.py ← واجهة برمجة تطبيقات عالية المستوى للمطورين
                                                                          ↓
trino_client.py ← عمليات قاعدة البيانات ذات المستوى المنخفض
                                                                          ↓
                                           كتالوج ذاكرة ترينو
Memory.aura.features ← تشغيل/إيقاف الترجمة لكل واجهة
Memory.aura.translation_state ← اللغة المستهدفة لكل واجهة

                                               ## الإعداد المحلي

                                               ### 1. عامل الميناء

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

                                                 ### 2. عميل بايثون

```bash
source .venv/bin/activate
pip install trino
```

### 3. تهيئة قاعدة البيانات (يتم استدعاؤها تلقائيًا عند بدء تشغيل Aura)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

       ## واجهة برمجة تطبيقات المطور — aura_state.py

```python
from scripts.py.func.db.aura_state import (
    enable_translation,
    disable_translation,
    set_language,
    get_current_language,
    is_translation_enabled,
    get_all_status,
)

# Enable translation for speech interface
enable_translation('speech', lang='en')

# Check status
is_translation_enabled('speech')  # True
get_current_language('speech')    # 'en'

# Disable
disable_translation('speech')

# All interfaces
get_all_status()
# [
#   {'interface': 'speech',   'translation': 'on',  'language': 'en'},
#   {'interface': 'terminal', 'translation': 'off', 'language': None},
#   {'interface': 'web',      'translation': 'off', 'language': None},
# ]
```

                              ## واجهة المستخدم الإدارية

                                                        http://localhost:8084

                                                                    يبدأ:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

                                ## Trino UI (مراقبة الاستعلام)

                                                    http://localhost:8083/ui/

                            البرامج النصية/py/func/ديسيبل/
                                                            ├── init.py
├── trino_client.py ← المستوى المنخفض: الحصول على/تعيين feature_state، target_lang
├── init_trino_db.py ← بدء التشغيل: بدء Docker + المخطط + الجداول
└── aura_state.py ← واجهة برمجة تطبيقات عالية المستوى للمطورين
                           البرامج النصية/الpy/الدردشة/
└──streamlit-admin.py ← واجهة المستخدم الإدارية على المنفذ 8084


                                                    ##خارطة الطريق

                                             - [x] Trino يعمل في Docker
                                         - [x] عميل بايثون متصل
- [x] تمت تهيئة قاعدة البيانات عند بدء تشغيل Aura
                  - [x] حالة الترجمة المدركة للواجهة
- [x] الويب (Sreamlit) منفصل عن الكلام/المحطة الطرفية
  - [x] واجهة المستخدم الإدارية على المنفذ 8084
                        - [ ] محطة والكلام مستقلة تماما
- [ ] التجاوزات الخاصة بالمستخدم (متعدد المستخدمين)
- [ ] التخزين المستمر (استبدال كتالوج الذاكرة)