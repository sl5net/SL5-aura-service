# دليل إعداد DEV_MODE

                                                            ## المشكلة

نظرًا لأننا متوافقون مع Weyland، فإننا نستخدم "threading.Lock" للتسجيل.

الآن (21.3.26 السبت) تغيرت قواعد التسجيل. في مانجارو لم يكن الأمر مشكلة.

عندما يكون `DEV_MODE = 1` نشطًا، تنتج Aura مئات من إدخالات السجل في الثانية
من عدة خيوط. يمكن أن يتسبب هذا في وصول SafeStreamToLogger إلى طريق مسدود، مما يؤدي إلى حدوث خطأ
               هالة شنق بعد الزناد الإملاء الأول.

                       ## الحل: استخدم عامل تصفية LOG_ONLY

عند التطوير باستخدام `DEV_MODE = 1`، **يجب عليك** أيضًا تكوين مرشح سجل في:
                                `config/filters/settings_local_log_filter.py`

            ### الحد الأدنى من مرشح العمل لـ DEV_MODE:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

                               ## سطر واحد للإعدادات_local.py
أضف هذا التعليق كتذكير بجوار إعداد DEV_MODE الخاص بك:
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## السبب الجذري (نظرًا لأننا متوافقون مع Weyland)
يستخدم "SafeStreamToLogger" "threading.Lock" لحماية عمليات الكتابة القياسية.
ضمن تحميل السجل العالي (DEV_MODE)، يتسبب التنافس على القفل في حدوث حالة توقف تام على الأنظمة
مع جدولة سلسلة صارمة (على سبيل المثال، CachyOS مع نواة أحدث/glibc).