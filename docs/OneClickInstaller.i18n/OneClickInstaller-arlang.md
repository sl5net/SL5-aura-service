# 1-انقر فوق أداة التثبيت (إعداد صفري)

احصل على **Aura** وتشغيله على جهازك بنقرة واحدة. لا يلزم معرفة البرمجة أو الأوامر الطرفية أو إعداد Python اليدوي.

                                                                          ---

                                ## صفر المتطلبات الأساسية

                                           أنت **لا** تحتاج إلى:
                                         - بايثون مثبتة مسبقا
                                       - مستودعات Git أو الكود
          - تجربة سطر الأوامر أو المحطة الطرفية

                                                                          ---

                                                     ## بداية سريعة

### الطريقة الأولى: Web One-Liner (الأسرع والموصى به لنظام التشغيل Linux / macOS)
يوفر ما يقرب من 30 ثانية من المعالجة اليدوية للملفات ويبدأ فورًا في جهازك الطرفي:

                                                   **لينوكس وماك:**
                                                  #### Web One-Liner CodeBerg
```bash
curl -sSL https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
                                                                         أو
                                   #### الويب أحادي الخط GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

                                           **ويندوز (باورشيل):**
                                                  #### Web One-Liner CodeBerg
# لم يتم اختباره - يرجى استخدام الطريقة الثانية (الثنائية المستقلة) لنظام التشغيل Windows
```bash
irm https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
                                                                         أو
                                     #### جيثب ويب أحادي الخط
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

الطريقة الثانية: ثنائي مستقل (النقر على Windows وسطح المكتب)

                        ### 2.1 قم بتنزيل برنامج التثبيت
قم بتنزيل ملف التثبيت الفردي المطابق لنظام التشغيل الخاص بك من [أحدث إصدار لـ GitHub]:

                                                - **ويندوز:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
                                                  - **لينكس:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
                                                      - **ماك:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


                                       ###2.2. قم بتشغيل المثبت

إعادة تسمية aura-installer-windows.exe.zip إلى aura-installer-windows.exe

انقر نقرًا مزدوجًا فوق الملف الذي تم تنزيله. ستظهر نافذة الإعداد وتقوم تلقائيًا بإعداد البيئة.

                                              ###2.3. ابدأ الإملاء
بمجرد الانتهاء، تقوم Aura بإنشاء اختصار على سطح المكتب وتبدأ في الاستماع على الفور.

                                                                          ---

                                      ## ماذا يحدث تلقائيًا؟

عند تشغيل برنامج التثبيت، تقوم Aura تلقائيًا بما يلي:
- تكوين محرك التعرف على الكلام المحلي والخاص.
             - تنزيل النماذج الصوتية الافتراضية.
- يقوم بإعداد جميع اختصارات النظام ومشغلات سطح المكتب الضرورية.

                                                                          ---

                              ## تفاصيل ومتطلبات التثبيت

                      - **مدة التثبيت:** حوالي 2-3 دقائق.
- **مساحة القرص المطلوبة:** الحد الأدنى ~ 1.5 جيجابايت (يصل إلى 2.5 جيجابايت حسب طرازات اللغة المحددة).
                                               - **دليل التثبيت:**
                                - **Linux وmacOS:** `~/opt/sl5-aura-service`
                             - **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

                                                                          ---

                                             ## الخطوات التالية

- **وضع الجدة:** اكتب كلمة واحدة في ملف القاعدة الخاص بك وشاهد قواعد Aura تُنشئ تلقائيًا.
- **تعلم مع Koans:** استكشف المفاهيم خطوة بخطوة في [Getting Started](../GettingStarted.i18n/GettingStarted-arlang.md).