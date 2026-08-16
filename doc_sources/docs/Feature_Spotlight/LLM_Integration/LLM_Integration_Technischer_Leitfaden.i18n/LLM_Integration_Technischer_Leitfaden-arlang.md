# 🧠 SL5 Aura: تكامل Erweiterte Offline LLM

                                          **الحالة:** Produktionsbereit
                             **المحرك:** أولاما (لاما 3.2 3B)
**التأخر:** Sofort (<0.1 ثانية بعد إصابة ذاكرة التخزين المؤقت) / ~20 ثانية (إنشاء وحدة المعالجة المركزية)

       ## 1. فلسفة "الهندسة المعمارية والعملية".
هالة هي نموذج هجين، وهو **التطبيق** و**المرونة**:
* **Der Architekt (RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle ("Browser öffnen"، "Lauter").
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. ليس هناك أي نشاط، ولكن لا داعي للقلق.

                                                                          ---

                                          ## 2. الأداء المعماري

في أحد المواقع المحلية LLM على وحدات المعالجة المركزية (CPUs) العادية (وحدة معالجة الرسوميات) التي يمكن استخدامها، قم بإعدادها **3-استراتيجية-الاستراتيجية**:

                  ### المادة 1: "الوضع الفوري" (Schlagworte)
              * **Trigger:** Wörter مثل "Instant"، "Schnell"، "Sofort".
* **المنطق:** محتوى LLM الكامل. يتم إنشاء Schlagworte من Eingabe مباشرة من خلال SQLite-Datenbank.
                                    * **لاتينز:** **< 0.05 ثانية**

### المادة 2: ذاكرة التخزين المؤقت الذكية (SQLite)
* **المنطق:** Jeder Prompt wird gehasht (SHA256). من أجل نشر المعلومات، سيتم استخدام `llm_cache.db`.
* **ميزة "التنوع النشط":** تم إنشاء صندوق تخزين ذاكرة التخزين المؤقت من خلال النظام العشوائي (فرصة 20%) *جديد* بديل متغير. العدد: ~5 خيارات مختلفة من أجل المزيد من الحياة.
* **ميزة "التجزئة الدلالية":** Bei langen Fragen (>50 Zeichen) extrahiert das LLM zuerst Keywords (z.B. "installation anleitung") و hasht diese. لذلك werden "Wie installiere ich es؟" و"تثبيتات التثبيت" هي نفسها أيضًا.
                                                * **لاتينز:** **~0.1s**

              ### المادة 3: إنشاء API-Generierung (احتياطي)
* **المنطق:** في حال عدم وجود ذاكرة تخزين مؤقت، سنتمكن من استخدام واجهة برمجة تطبيقات Olma (`http://localhost:11434/api/generate`).
                                                        * **التحسين:**
* **الحدود الصلبة:** `num_predict=60` zwingt das Modell, nach ca. 40 Wörtern zu stoppen.
* **أنابيب الإدخال:** يتم إرسال النص الكبير (README) إلى STDIN übergeben، وهو ما يسمح بتوسيع حدود أنظمة المشتركين.
* **التأخر:** **~15-25 ثانية** (من وحدة المعالجة المركزية)

                                                                          ---

                      ## 3. نظام التأريض (مضاد للهلوسة)

تتعرف Generische LLMs في كثير من الأحيان على واجهات المستخدم الرسومية (الأزرار، القوائم). سنساعدك على إضافة المزيد من القوة **`AURA_TECH_PROFILE`**:

1. **لا توجد واجهة مستخدم رسومية:** Aura ist ein Headless CLI-Dienst.
2. **ملفات التكوين البسيطة:** المنطق هو رمز Python، لا يحتوي على `.json`/`.xml`.
3. **المشغل:** التحكم الخارجي في أحداث نظام البيانات (`touch /tmp/sl5_record.trigger`)، لا يوجد به واجهات برمجة التطبيقات.
4. ** التثبيت: ** Dauert real 10-20 Min wegen 4GB Modelldownloads (verhindert falsche Versprechen).

                                                                          ---

                                 ## 4. جسر الحافظة (أمان Linux)

لا يمكن استخدام الخلفية (systemd) في الغالب من خلال ميزة الأمان (X11/Wayland).
* **الملف:** يتم حفظ النص في جلسة المستخدم (`clipboard_bridge.sh`) في ملف ذاكرة الوصول العشوائي (RAM)-القرص (`/tmp/aura_clipboard.txt`).
            * **Aura:** Liest diese Datei und umgeht so alle Rechte-Probleme.

                                                                          ---

      ## 5. Selbst-Lernen (تدفئة ذاكرة التخزين المؤقت)

          سنتعرف على البرنامج النصي "warm_up_cache.py":
                        1. إنه أحدث `README.md` من المشاريع.
2. إنه جزء جميل من LLM، وهو أمر سهل الاستخدام للغاية.
3. تم تصميم هذه الرائحة على شكل هالة، مما يجعل بنك البيانات يعمل تلقائيًا.