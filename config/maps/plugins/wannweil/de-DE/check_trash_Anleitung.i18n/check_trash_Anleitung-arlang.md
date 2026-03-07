# خدمة Müll-Abfuhr Erinnerungs (ملحق Aura)

تعمل هذه الأداة تلقائيًا على إزالة الأخطاء من Wannweil، بناءً على مستندات Abfallkalender-PDF الرسمية.

                                                            ## الوظائف
- **PDF-Parsing**: آخر Termine مباشرة من `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Nutzt `notify-send` for visuelle Alarme unter Manjaro.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (مثالي، wenn das Handy verlegt ist).
- **Sicherheits-Check**: تحذير نشط، عندما يكون PDF-Jahr abgelaufen ist oder die Datei fehlt.

                                          ## التثبيت وVoraussetzungen
                               1. **حزمة النظام** (مانجارو):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
                                2. **Python-Abhängigkeiten** (im Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

                                  ## التشغيل الآلي (النظام)
يبدأ اليوم في تمام الساعة 17:00 على مدار الساعة لمدة دقيقة واحدة قبل Systemstart، وذلك بعد انتهاء المهمة بالكامل.

                                               ** تاريخ الخدمة: **
                                   ~/.config/systemd/user/trash_check.service

                                               **تاريخ الموقت:** `
                                     ~/.config/systemd/user/trash_check.timer

                                                      Befehle zum Aktivieren:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

                                       ## Empfehlungen für den Jahreswechsel
                1. تحميل ملف PDF الجديد من Gemeinde Wannweil.
2. قم بتغيير بيانات الطلب `config/maps/plugins/wannweil/de-DE/`.
3. يتم تشغيل الخدمة في العام الجديد تلقائيًا في البيانات.
4. لا يتم السماح بملف PDF أو كونه حقيقيًا، مما يؤدي إلى إرسال النظام إلى ملف خاص به.

                                               ## اختبار مانويلر
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
                                                             __CODE_BLOCK_4__