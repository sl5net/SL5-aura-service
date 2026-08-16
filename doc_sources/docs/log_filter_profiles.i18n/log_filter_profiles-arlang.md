# ملفات تعريف مرشح السجل

يكون مرشح السجل النشط دائمًا `config/filters/settings_local_log_filter.py`.

                                             ## الملفات الشخصية

يتم تخزين الملفات التعريفية المحددة مسبقًا في `config/filters/.backlock/`:

                                     | الملف الشخصي | الوصف |
                                                                    |---|---|
| `التشغيل_الأول` | الحد الأدنى من الإخراج - الأخطاء والحالة فقط. يتم تطبيقه تلقائيًا عند البداية الأولى. |
        | `عادي` | مرشح قياسي للاستخدام اليومي. |

                           ## تبديل الملف الشخصي يدويًا

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

                                     ## إضافة ملف تعريف مخصص

1. أنشئ مجلدًا جديدًا ضمن `config/filters/.backlock/my_profile/`
2. انسخ ملف `settings_local_log_filter.py` الموجود فيه وقم بالتعديل حسب احتياجاتك
 3. قم بتطبيقه باستخدام `cp` كما هو موضح أعلاه

                   ## التبديل التلقائي للملف الشخصي

في البداية، تكتشف Aura أن الدليل `log/` غير موجود بعد، و
يقوم تلقائيًا بنسخ ملف التعريف `first_run` كمرشح نشط.