# تراكب التسجيل (العرض على الشاشة)

يوفر تراكب التسجيل مؤشرًا مرئيًا فوريًا عبر الأنظمة الأساسية لحالة الإملاء. وهو يعمل بشكل مستقل عن برامج إشعارات سطح المكتب ومرشحات "عدم الإزعاج"، ويعرض الحالة مباشرة على الشاشة الرئيسية.

                                                     ## أمثلة مرئية

              | أسفل اليسار (`bl`) | أعلى اليمين (`tr`) |
                                                            | :---: | :---: |
                                                    | ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *يندمج في اللوحات الداكنة وأدراج النظام* | *تباين عالٍ على النوافذ الخفيفة أو المعقدة* |

                                                           ##الولايات

- **التسجيل (```)**: دائرة حمراء زاهية مع مخطط تفصيلي مميز (`#e62222` على `#181818`) تشير إلى تسجيل صوتي نشط.
                                                              - **عاطل**:
- `مخفي` (افتراضي): يتم سحب النافذة بالكامل، مما يوفر مساحة على سطح المكتب للتفاعل العادي.
- `خماسي`: يعرض شارة خماسية هندسية دقيقة (`⬟`) أثناء وضع الخمول.

                                                            ## إعدادات

              تتم إدارة الإعدادات في `config/settings.py`:

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

                                                                ## بنيان

- تم إنشاؤه باستخدام مكتبة Python القياسية (`tkinter`)، ولا يتطلب أي تبعيات C خارجية.
- يتم تنفيذه في مؤشر ترابط خفي في الخلفية مع معالجة أحداث قائمة الانتظار الآمنة لمؤشر الترابط.
- يكتشف الشاشة الأساسية ديناميكيًا في البيئات متعددة الشاشات.

                                          (ق، 10.9.\'26 14:41 الخميس)