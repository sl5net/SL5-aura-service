#الجزء الثاني عشر: عرض وحدات الماكرو الخاصة

يوضح هذا التمرين كيفية استخدام وحدات الماكرو الخاصة المتداخلة وقصر نطاقها على نوافذ نشطة معينة باستخدام التكوين `only_in_windows`.

                       ## متطلبات أمان النافذة النشطة
لمنع تنفيذ هذه القواعد التوضيحية (مثل الاسم الأول أو البريد الإلكتروني أو رقم الهاتف) عالميًا أثناء اختبارات النظام الأخرى، فإنها تقتصر على النوافذ النشطة المطابقة للنمط `12_private_macros_demo`.

               لاختبار هذه القواعد، يجب عليك إما:
1. استخدم محررًا يعرض مسار الملف بالكامل في عنوان نافذته (على سبيل المثال، PyCharm أو VS Code).
2. احفظ الملف الذي تقوم بتحريره أو أعد تسميته بحيث يحتوي اسمه على `12_private_macros_demo` في المحرر الخاص بك (على سبيل المثال، في محرر Kate).

                                                                          ---

                                                            ## تعليمات

1. حدد اسم مجلد اللغة الخاص بك (على سبيل المثال، `de-DE` للغة الألمانية، و`en-US` للغة الإنجليزية، و`fr-FR` للغة الفرنسية)
2. داخل مجلد اللغة، تأكد من وجود ملف باسم `FUZZY_MAP_pre.py`. إذا لم يكن موجودا، قم بإنشائه.
3. انسخ قواعد القالب أدناه إلى قائمة `FUZZY_MAP_pre` داخل هذا الملف.

                                 ### مجلدات اللغة المدعومة
إذا لم يكن المجلد الخاص بلغتك موجودًا بعد ضمن `config/maps/koans_deutsch/12_private_macros_demo/`، فيجب عليك إنشاؤه يدويًا. الرجاء استخدام أسماء المجلدات المحددة أدناه:

                                                      - `ar` (العربية)
                                               - `de-DE` (الألمانية)
                                             - `en-US` (الإنجليزية)
                                                  - `es` (الإسبانية)
                                                    - `fr` (الفرنسية)
                                              - `مرحبا` (الهندية)
                                                - `جا` (اليابانية)
                                                    - `كو` (الكورية)
                                                      - `pl` (بولندية)
                          - `pt-BR` (البرتغالية - البرازيل)
                                                - `pt` (البرتغالية)
                                  - `zh-CN` (الصينية - المبسطة)


                                                  ### قالب القاعدة

```python
# Copy these rules to your FUZZY_MAP_pre list

# config/maps/koans_deutsch/12_private_macros_demo/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401

FUZZY_MAP_pre = [ 
# ========================================================================= 
# OUTER MACRO: PRIVATE SECTION 
# ========================================================================= 
# Triggers the 'private_section' group. 
# EXAMPLE: my private profile 
('private profile', r'my private profile', 100, { 
'group_start': 'private_section' 
}), 

# ----------------------------------------------------------------------- 
# SUB-SECTION 1: NAME DETAILS (Nested Macro) 
# ----------------------------------------------------------------------- 
# Appends the section header 'Name:' if the trigger word 'namensdetails' is not in the text. 
# EXAMPLE: name details

('Name:', r'name details', 100, {'group_start': 'name_details'}),

# Standard rules inside the name sub-section:

# EXAMPLE: first name

('Max', r'first name', 100, {}),

# EXAMPLE: last name

('Mustermann', r'last name', 100, {}),

# EXAMPLE: nixleA

('nixA', r'nixleA', 100, {}),

# EXAMPLE: nixleB

('nixB', r'nixleB', 100, {}),

# End of Name Sub-Section

(None, r'', 100, {'group_end': 'name_details'}),

# -------------------------------------------------------------------------

# SUB-SECTION 2: CONTACT DETAILS (Nested Macro) 
# ----------------------------------------------------------------------- 
# Appends the section header 'Contact:' if the trigger word 'contact details' is not in the text. 
# EXAMPLE: contact details 
('Contact:', r'contact_details', 100, {'group_start': 'contact_details'}), 

# Standard rules inside the contact sub-section: 
# EXAMPLE: email address 
('max.mustermann@example.de', r'e-mail-address', 100, {}), 
# EXAMPLE: phone number 
('+49 170 1234567', r'phone number', 100, {}), 

# End of Contact Sub Section 
(None, r'', 100, {'group_end': 'contact_details'}), 

# ========================================================================= 
# OUTER MACRO END 
# ========================================================================= 
# Passive end marker to terminate the main private section macro. 
(None, r'', 100, {'group_end': 'private_section'})
]


]
```