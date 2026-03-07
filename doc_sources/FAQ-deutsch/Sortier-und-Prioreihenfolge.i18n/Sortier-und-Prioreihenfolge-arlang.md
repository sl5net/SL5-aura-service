يتم الفرز من خلال الجمع بين **الفرز الأبجدي** من خلال Ebene und der **Hierarchie** der Ordner.

مبدأ "الفوز بالمباراة الأولى" هو الأفضل من خلال الحفاظ على الأولوية.

يمكنك البدء في استخدام مجموعة من أدوات التحكم الأساسية، من خلال "DE" و"الولايات المتحدة" و"المكونات الإضافية".

                                                                          ---

                            ## Allgemeine Sortier- und Prioritätsreihenfolge

إن Ladereihenfolge (ومع مراعاة الأولويات) يجب أن تكون ضمن النظام من خلال الترتيب الأبجدي للترتيب والوحدة النمطية على جميع المستويات.

             ### 1. النظام العالمي - Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst الأبجدية durchlaufen:

                     | أوردنر | الأولوية | بيميركونج |
                                                       | :--- | :--- | :--- |
             | `دي دي` | **1. الأولوية** | Wird zuerst geladen. |
      | `ar-US` | **2. الأولوية** | Wird nach `de-DE` جيلادن. |
 | "الإضافات" | **3. الأولوية** | ويرد zuletzt geladen. |

                                ### 2. Ladung der Kern-Regeln (de-DE وen-US)

سيتم إعادة صياغة نظام Kern-Sprachordnern في القائمة "الخريطة_الغامضة_السابقة".

                     ### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

تأتي المكونات الإضافية في المرتبة الأولى، حيث يتم ترتيب "المكونات الإضافية" أبجديًا في "DE" و"في الولايات المتحدة".

Innerhalb des `plugins\'-Ordners werden die Unterordner Wieder Alphabetisch durchlaufen:

               | البرنامج المساعد | أبجدية Reihenfolge |
                                                              | :--- | :--- |
                           | `CCC_tue` | 1. البرنامج المساعد |
      | `أرقام_إلى_أرقام` | 2. البرنامج المساعد |

     ### 4. تحديد الأولويات الشاملة لـ `FUZZY_MAP_pre`

تم إعادة تنظيم جميع * جميع * Ladevorgang في القائمة النهائية. أولويات الأولوية:

| بلاتز في `fuzzy_map_pre` | بفاد زور ريجل | الأولوية |
                                                       | :--- | :--- | :--- |
    | **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
       | **2.** | `en-US/FUZZY_MAP_pre.py` | هوش (أساس-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (المكونات الإضافية يتم فرزها أبجديًا، `CCC` يتم حفظها بواسطة `الأرقام`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (المكونات الإضافية التي يتم فرزها أبجديًا) |

                                                                          ---

                     ## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

              يتم استخدام فلتر Sprache النشط حاليًا.

إذا كنت ترغب في ضبط إعدادات **Deutsch (`de-DE`)** المحملة بالكامل، فيجب عليك تحديد أولوية السجل، حيث يجب أن يكون مفتاح التحكم أفضل من ضبط المكونات الإضافية:

                         1. **كيرن-ريجلن:** `de-DE/FUZZY_MAP_pre.py`
         2. **Plugin-Regeln (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Plugin-Regeln (أرقام):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

                                           **الفوز بالأولوية:**

* **ضبط كيرن** setzen sich gegen all plugins durch، da sie duch die Alphabische Sortierung der Ordner zuerst geladen werden.
* **تم تحديد المكونات الإضافية** يتم ترتيبها أبجديًا بشكل صارم من خلال تسمية ترتيب المكونات الإضافية (`C` إلى `D`). من الأفضل أن يكون `CCC_tue` له الأولوية في `الأرقام_إلى_الأرقام`.