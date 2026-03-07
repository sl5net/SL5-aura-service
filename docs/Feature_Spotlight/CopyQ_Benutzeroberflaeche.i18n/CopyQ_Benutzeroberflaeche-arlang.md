# CopyQ – Benutzeroberfläche والتكامل في SL5 Aura

                                                       ## هل كان CopyQ؟

يعد CopyQ أحد أفضل أدوات إدارة الحافظة مع شريط نصوص برمجي واحد.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
                                بايثون سكريبت أو Tastenkürzel.

بالنسبة لـ SL5 Aura هو CopyQ من الأداة الأساسية للنشر بالنص
                      In die Zwischenablage zu Bringen und dort zu verwalten.

                      ## البيانات ذات الصلة في الريبو

                                                      | داتي | زويك |
                                                                    |---|---|
      | `tools/export_to_copyq.py` | Exportiert FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` | Verarbeitet Text und sendet ihn an CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | أرقام الحافظة-النص أم |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | اختبار النصي لـ Clipboard-Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

                                                ## تصدير_إلى_copyq.py

هذا البرنامج النصي `tools/export_to_copyq.py` هو أحدث خريطة لتاريخ المستودعات (للقراءة فقط)
          وإرسالها لإعادة تنظيم العناصر في CopyQ.

**الصلاحية:** لا يُرسل البرنامج النصي إلى بيانات مخزنة - فهو يُرسل فقط إلى الأوامر
                                   برنامج CopyQ-Prozess الخارجي.

                                                           ### المنصات

            - **Linux:** `copyq` موجود مباشرة في PATH verfügbar
- **Windows:** Typische Pfade werden automatisch ge sucht, z.B. "C:\Program Files\CopyQ\copyq.exe".

                                                           ### نوتزونج

```bash
python tools/export_to_copyq.py
```

                                        ## CopyQ لكل Kommandozeile steuern

              CopyQ يحتوي على واجهة سطر الأوامر (CLI):

```bash
# Aktuellen Clipboard-Inhalt zeigen
copyq read 0

# Text in Clipboard schreiben
copyq add "Mein Text"

# Item aus History holen (Index 0 = aktuell)
copyq read 0

# CopyQ-Fenster öffnen
copyq show

# Script ausführen
copyq eval "popup('Hallo von Aura!')"
```

                               ## الحجر 11 – CopyQ Benutzeroberfläche

   يحتوي Der Koan `11_copyq_benutzeroberflaeche` على نبتة "koans"
                      من النوع STT-Erkennungsfehlern wiederherstellen.

                               ### FUZZY_MAP_pre.py (لأداة LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Diese Regel greift bei Fullmatch (`^...$`) - توقف أيضًا عن خط الأنابيب الأكثر حداثة.

                                         ### FUZZY_MAP.py (nach LanguageTool)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

هذه الأيام ستمنحك المزيد من البهجة الداخلية (لا تحتاج إلى Fullmatch).

                                           ## Typische STT-Fehler bei "CopyQ"

                      غالبًا ما يتم تحديث "CopyQ" أيضًا:
                                                       - "نسخ جديلة".
                                                            - `كوبي كو`
                                      - "نسخ قائمة الانتظار".
                                                              - `كوبي ف`

                  دليل تصحيح الأخطاء لـ `FUZZY_MAP_pre.py`:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

                                          ## pyperclip als Python-Alternative

عندما لا يتم تحديث CopyQ، يتم استخدام Aura `pyperclip` كإجراء احتياطي:

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` موجود في `.venv` installiert (`site-packages/pyperclip/`).

                                                               ##هينويز

- يجب أن يتم تشغيل CopyQ كوظيفة Hintergrundprozess حتى تعمل واجهة سطر الأوامر (CLI)
                                 - نظام Linux: `copyq &` beim Systemstart
- ضمن نظام التشغيل Windows: يبدأ تشغيل CopyQ تلقائيًا في الدرج عند تثبيته
- للاختبارات: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`