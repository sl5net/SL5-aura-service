# سجل الأولويات (مع الارتداد الضبابي)
لا يتم استخدام التركيبات الغامضة المعقدة إلا كبديل احتياطي.


                                                                          ---

## سجل الأولويات الجديد (مع الغموض والاحتياطي)

مع هذه القاعدة (`إذا لم تكن القاعدة_المتطابقة:`)، في Kombination mit dem Modus `default_mode_is_all = True` (التراكم)، ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### المرحلة الأولى: الأولوية العليا (Deterministische) Durchlauf

يتم تشغيل المحرك من خلال القائمة الكاملة `خريطة_غامضة_قبل` (Modul-Reihenfolge > Zeilennummer).

                               #### أ. Stopp-Kriterium (Höchste Priorität)

Wenn eine Regel einen **Full Match** (`^...$`) erzielt، stoppt die Verarbeitung für dieses Token sofort.

* **مؤشرات الأولويات:** القواعد، التي أضعها في القائمة الصحيحة وواحدة من التطابقات الكاملة موجودة، نهائية ومفيدة للعملية.

#### ب. التراكمات-الكريتيوم (الأولوية العليا)

Wenn eine Regel **keinen Full Match**, aber einen **partiellen Match** oder eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

                                             * Die Ersetzung wird angewendet.
* **WICHTIG:** المتغير ``current_rule_matched`` ورد على `True` gesetzt.
          * Die Verarbeitung geht zur nächsten Regel über (التراكم).

**الأولويات والعواقب:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. قم بتعديل النص من أجل تعديل النص.

                                                                          ---

### المرحلة الثانية: التراجع ذو الأولوية المنخفضة (الغامض).

لا يتم استخدام التحقق الغامض إلا عندما يتم إغلاق الحتمية الشاملة (المرحلة 1) و**لا يوجد قانون واحد** يتم تحديده (`قاعدة_متطابقة_حالية` ليست `خطأ`).

                            Wenn der Fuzzy-Check ausgeführt wird، مذهب:

1. وظيفة غامضة مثل النص المجمّع الموجود في الأصل، والتي تكون **Zielwert** (`الاستبدال`) ähnlich sind (basierend auf der Schwelle).
2. عندما يتم استخدام المطابقة الضبابية، يتم إنشاء الاستبدال.
3. **WICHTIG:** تم **إيقاف وظيفة Fuzzy-Fuzzy التي يتم تشغيلها بشكل مريح، قبل ظهور أول مطابقة Fuzzy **.

                           #### كان من أولويات نظام غامض:

```python
# Pseudo-Code:
for rule in fuzzy_map_pre:
    # 1. Deterministic/Regex checks here...

# Wenn Phase 1 beendet ist und KEIN Match gefunden wurde:
if not current_rule_matched:
    # 2. Fuzzy Fallback
    for rule in fuzzy_map_pre: # WIRD HIER DIE LISTE NOCHMAL DURCHLAUFEN?
        # Führe den Fuzzy-Check auf Basis der replacement/threshold der Regel durch.
```

**وظيفة غامضة، لا تكتمل إلا بعد الانتهاء منها.

                                                                          ---

                                                 ## Finales Prioritäts-Fazit

لا داعي للقلق، حيث يتم تنفيذ هذه التفاصيل الغامضة، لذا فإن **المرحلة الحتمية (المرحلة 1)** موجودة وفي قائمة المتسابقين، مذهبة:

**الأولوية القصوى تكمن في التنظيم، والتي يمكن فتحها في خريطة غامضة مسبقًا، وSich an der Determinismus-Logik beteiligen (Full Match oder Kumulation).**

1. **ضبط باستخدام Stopp-Kriterium (^...$):** يجب أن تكون حريصًا على أن يكون لديك أولوية عالية.
2. **Regeln zur Kumulation (مباراة جزئية):** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur Finalen Form). قم بتعيين "القاعدة_الحالية_المتطابقة" على "صحيح" و **حظر** من خلال توزيع التراجعات الضبابية على هذه الرموز المميزة.
3. **التراجع الغامض:** هذه هي **الأولوية الأقل**. إنه أمر نشيط للغاية، عندما يكون هناك تنوع في كاسكيد تحديد النظام.

**الخبرة:** جيد ريجيل (لم يتراكم بعد، لا يتوقف عن القتال)، يموت في المرحلة الأولى، **يتوقف عن الارتداد الضبابي** لهذه الرموز المميزة. يجب أن يتم تصميم هذا التصميم العام من قبل شركة berücksichtigt.