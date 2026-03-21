# سمات القاعدة: `only_in_windows` و`exclude_windows`

تتحكم هاتان السمتان في **النوافذ النشطة التي يُسمح فيها بتنشيط القاعدة**.
يتم تعريفها داخل إملاء "خيارات" القاعدة وقبول **قائمة أنماط التعبير العادي**
التي تتم مطابقتها مع عنوان النافذة النشطة الحالية (`_active_window_title`).

                                                                          ---

                                              ## `فقط_في_النوافذ`

يتم تفعيل القاعدة **فقط إذا** كان عنوان النافذة النشطة يتطابق مع **واحد على الأقل** من الأنماط المحددة.
                      يتم تجاهل كافة النوافذ الأخرى.

**حالة الاستخدام:** تقييد القاعدة على تطبيق محدد.


> سيتم تفعيل القاعدة **فقط** عندما يكون Firefox أو Chromium هو النافذة النشطة.

                                                                          ---

                                           ## `استبعاد_النوافذ`

يتم تفعيل القاعدة **ما لم** يتطابق عنوان النافذة النشطة مع **واحد على الأقل** من الأنماط المحددة.
                             يتم تخطي النوافذ المطابقة.

**حالة الاستخدام:** تعطيل قاعدة لتطبيقات محددة.

                                                                   أمثلة

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



المطابقة **غير حساسة لحالة الأحرف** وتستخدم لغة Python **التعبيرات العادية**.

                                                                          ---

                                                                  ## ملخص

                                    | السمة | يشتعل عندما... |
            |-------------------|-------------------------------------------|
| `فقط_في_النوافذ` | عنوان النافذة **يطابق** أحد الأنماط |
| `استبعاد_النوافذ` | عنوان النافذة **لا يتطابق** مع أي نمط |

                                                                          ---

                                                         ## أنظر أيضا

- `scripts/py/func/process_text_in_background.py` - السطور ~1866 و~1908
- `scripts/py/func/get_active_window_title.py` - كيفية استرداد عنوان النافذة