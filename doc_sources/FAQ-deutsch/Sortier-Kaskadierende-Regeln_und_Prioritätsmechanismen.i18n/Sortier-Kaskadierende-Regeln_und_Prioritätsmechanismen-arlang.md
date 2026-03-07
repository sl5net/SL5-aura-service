# Kaskadierende Regelausführung وآليات الأولوية

يتم تحديد كافة التفاصيل، وهي مجموعة معقدة من الأولويات والطرق والتراجع.

                                                                          ---

               # Kaskadierende Regelausführung وآليات الأولوية

يتم تحديد نظام التنظيم بشكل متتابع من خلال تحديد موضعه في قائمة "الخريطة الغامضة" التي تحدد أولوياتها (Modul-Lade-Reihenfolge > Zeilennummer).

Dies folt dem Prinzip der **Kaskadierenden Regelausführung** (`default_mode_is_all = True`)، wobei alle passenden Regeln nacheinander angewendet werden، bis ein spezifisches Stopp-Kriterium erfüllt ist.

             ## 1. الأولوية القصوى: حتمية دورشلاوف

بدأ Die Verarbeitung مع Durchlauf der Regeln في der geladenen Reihenfolge. هناك نوع آخر من أنواع النصائح التي تحدد أولوياتك:

               ### أ. المطلقات Stopp-Kriterium (Höchste Priorität)
وفقًا للأولوية القصوى، هناك **مطابقة كاملة** (من `^` مكررة `$`) من خلال الرمز المميز، يتم إرسالها وتخصيصها بشكل عام لهذه الرموز المميزة (**الفوز بالمباراة الأولى**). إنها أكثر أمانًا، حيث أن التخصصات والحتمية هي التي تحددها القواعد.

                          ### ب. التراكم (Transformationsreihenfolge)
عندما يتم تغيير الحجم، لا توجد مطابقة كاملة (`^...$`) متجددة، مما يؤدي إلى إرجاع الاستبدال. يتم تنفيذ هذا الإجراء من خلال القواعد التالية. Da jede Regel auf dem **bereits modifizierten** text abeitet، is the الاستماع reihenfolge entscheidend ür die **Kaskadierung** der Transformationen.

             ## 2. الأولوية القصوى: التراجع الغامض

تتميز وحدة المنطق الضبابي (النتيجة 0–100) أيضًا بأنها احتياطية، مما يؤدي إلى إرجاع نص النص إلى النص الصحيح.

Aus Performance- und Stabilitätsgründen wird die Fuzzy Logik ** لا يوجد ** نشيط، عندما يتم تحديد دورشلاوف الحتمي بالكامل (النقطة 1) ** لا يوجد تعديل واحد **. لقد تم ضبط الضوابط الحتمية الحديثة على العلم الجديد و**الحظر** من خلال التراجع الغامض للرمز المميز الحالي.

                      ## 3. التحقق الخارجي (أداة اللغة)

بعد ذلك، ستتم عملية التحقق من خلال أداة LanguageTool (LT) التي تستخدم أسلوبًا أو أسلوبًا نحويًا.

يتم استخدام هذه الأداة بشكل متواصل، عند الانتهاء من عملية إعادة ضبط إعدادات النص في إطار نصي خاص بك (`LT_SKIP_RATIO_THRESHOLD`). يبدو الأمر أكثر أمانًا، حيث أن LT لا يحتوي على نص يتم عرضه، حيث أن Kaskade غير مكتمل يؤدي إلى تحويل صارخ للغاية، حيث أن التصحيح من خلال LT يفشل.