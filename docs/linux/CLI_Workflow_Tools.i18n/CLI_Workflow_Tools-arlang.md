# دليل تثبيت أدوات سير العمل لـ CLI

تعتمد بعض الإجراءات في البرنامج المساعد Path Navigator على أدوات مساعدة لسطر الأوامر الخارجية لإجراء عمليات بحث غامضة، وقائمة الملفات، ومعالجة الحافظة. إذا كانت هذه الأدوات مفقودة، فسوف ترى تحذيرًا في وحدة تحكم النظام.

فيما يلي تعليمات التثبيت لكل نظام تشغيل مدعوم.

                                           ## المرافق المطلوبة

* **`fzf`**: مكتشف غامض لسطر الأوامر للأغراض العامة.
* **`find`** (أو `fd`): أداة مساعدة قياسية للبحث عن الملفات.
* **أداة الحافظة**: تستخدم لتوجيه الإخراج مباشرة إلى حافظة النظام لديك.
                              * **Linux:** `xclip` (يتطلب بيئة X11).
                               * **macOS:** `pbcopy` (مثبت مسبقًا).
                           * **Windows:** `مقطع` (مثبت مسبقًا).
* **`ملف`**: يحدد أنواع الملفات للمعاينات الطرفية الكاملة.

                                                                          ---

                                             ## تعليمات التثبيت

                                ### 1. لينكس (آرتش / مانجارو)
نظرًا لأن نظامك يعمل على Manjaro، يمكنك تثبيت الحزم المطلوبة باستخدام `pacman`:

```bash
sudo pacman -S fzf findutils xclip file
```

                 ### 2. لينكس (ديبيان / أوبونتو / مينت)
 في الأنظمة المستندة إلى دبيان، استخدم `apt`:

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

                                                                ### 3. ماك
استخدم مدير الحزم [Homebrew](https://brew.sh/) لتثبيت الأدوات المفقودة:

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

                                                          ### 4. ويندوز
إذا كنت تستخدم Windows، فنوصي بتثبيت `fzf` عبر [Scoop](https://scoop.sh/) أو [Winget](https://github.com/microsoft/winget-cli):

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
                                                             __CODE_BLOCK_4__