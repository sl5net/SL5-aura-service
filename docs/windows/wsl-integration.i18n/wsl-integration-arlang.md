# تكامل WSL (نظام Windows الفرعي لنظام Linux).

يتيح لك WSL تشغيل بيئة Linux كاملة مباشرة على Windows. بمجرد الإعداد، يعمل تكامل STT shell ** بشكل مماثل مع أدلة Linux Bash أو Zsh ** - ولا يلزم إجراء أي تعديل خاص بنظام التشغيل Windows لوظيفة الصدفة نفسها.

> **موصى به لـ:** مستخدمي Windows الذين يشعرون بالارتياح عند استخدام محطة Linux، أو الذين قاموا بالفعل بتثبيت WSL لأعمال التطوير. توفر WSL التجربة الأكثر إخلاصًا وأقل تنازلات في التوافق.

                                       ## المتطلبات الأساسية

                          ### تثبيت WSL (إعداد لمرة واحدة)

         افتح PowerShell أو CMD ** كمسؤول ** وقم بتشغيل:

```powershell
wsl --install
```

يقوم هذا بتثبيت WSL2 مع Ubuntu بشكل افتراضي. أعد تشغيل جهازك عندما يُطلب منك ذلك.

                                        لتثبيت توزيعة محددة:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

                     قائمة بجميع التوزيعات المتاحة:

```powershell
wsl --list --online
```

                             ### تحقق من إصدار WSL الخاص بك

```powershell
wsl --list --verbose
```

تأكد من أن عمود "الإصدار" يعرض "2". إذا ظهر `1`، فقم بالترقية باستخدام:

```powershell
wsl --set-version <DistroName> 2
```

                                              ## تكامل شل داخل WSL

بمجرد تشغيل WSL، افتح محطة Linux الخاصة بك واتبع **دليل Linux shell** للصدفة المفضلة لديك:

                                                          | شل | دليل |
                                                            |-------|-------|
                              | باش (WSL الافتراضي) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-arlang.md) |
                                                         | زش | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-arlang.md) |
                                                       | سمك | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-arlang.md) |
                                                         | كش | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-arlang.md) |
                                     | بوسيكس ش / داش | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-arlang.md) |

بالنسبة لإعداد Ubuntu/Debian WSL الافتراضي مع Bash، المسار السريع هو:

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

                                ## الاعتبارات الخاصة بـ WSL

                          ### الوصول إلى ملفات Windows من WSL

تم تثبيت محركات أقراص Windows الخاصة بك ضمن `/mnt/`:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

إذا كان مشروعك موجودًا على نظام ملفات Windows (على سبيل المثال، `C:\Projects\stt`)، فاضبط `PROJECT_ROOT` على:

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

أضف هذا السطر إلى `~/.bashrc` (أو ما يعادله لـ Shell الخاص بك) **فوق** الدالة `s()`.

> **نصيحة الأداء:** للحصول على أفضل أداء للإدخال/الإخراج، احتفظ بملفات المشروع داخل نظام ملفات WSL (على سبيل المثال `~/projects/stt`) بدلاً من `/mnt/c/...`. يعد الوصول عبر نظام الملفات بين WSL وWindows أبطأ بشكل ملحوظ.

                  ### بيئة بايثون الافتراضية داخل WSL

قم بإنشاء واستخدام بيئة Linux الافتراضية القياسية داخل WSL:

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

سيعمل المسار `PY_EXEC` في الوظيفة (`$PROJECT_ROOT/.venv/bin/python3`) بشكل صحيح كما هو.

                                     ### تشغيل `s` من Windows Terminal

[Windows Terminal](https://aka.ms/terminal) هي الطريقة الموصى بها لاستخدام WSL على نظام التشغيل Windows. وهو يدعم علامات تبويب وأجزاء وملفات تعريف متعددة لكل توزيع WSL. قم بتثبيته من متجر Microsoft أو عبر:

```powershell
winget install Microsoft.WindowsTerminal
```

قم بتعيين توزيع WSL الخاص بك كملف التعريف الافتراضي في إعدادات Windows Terminal للحصول على تجربة أكثر سلاسة.

                                              ### Docker وKiwix داخل WSL

يتطلب البرنامج النصي المساعد Kiwix (`kiwix-docker-start-if-not-running.sh`) وجود Docker. قم بتثبيت Docker Desktop لنظام التشغيل Windows وتمكين تكامل WSL 2:

                                 1. قم بتحميل وتثبيت [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. في Docker Desktop → الإعدادات → الموارد → تكامل WSL، قم بتمكين توزيع WSL الخاص بك.
                                                3. التحقق داخل WSL:
   ```bash
   docker --version
   ```

### استدعاء وظيفة WSL من نظام التشغيل Windows (اختياري)

إذا كنت تريد استدعاء الاختصار s من نافذة Windows CMD أو PowerShell دون فتح محطة WSL، فيمكنك لفه:

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> تقوم العلامة `-i` بتحميل غلاف تفاعلي بحيث يتم الحصول على `~/.bashrc` (والوظيفة `s`) تلقائيًا.

                                                                  ## سمات

- **توافق كامل مع Linux**: تعمل جميع أدوات Unix (`timeout`، `pgrep`، `mktemp`، `grep`) بشكل أصلي - لا حاجة إلى حلول بديلة.
- **المسارات الديناميكية**: يتم العثور على جذر المشروع تلقائيًا عبر المتغير `PROJECT_ROOT` المعين في تكوين الصدفة الخاص بك.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فستحاول تشغيل "start_service" وخدمات Wikipedia المحلية (يجب أن يكون Docker قيد التشغيل).
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.