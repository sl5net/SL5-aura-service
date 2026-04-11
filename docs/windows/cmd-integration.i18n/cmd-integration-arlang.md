# تكامل موجه الأوامر (CMD) (Windows)

لتسهيل التفاعل مع STT (تحويل الكلام إلى نص) CLI من موجه أوامر Windows، يمكنك إنشاء ملف دفعي `s.bat` ووضعه على `PATH` الخاص بك. يتيح لك ذلك كتابة "سؤالك" ببساطة في أي نافذة CMD.

> **ملاحظة:** CMD (cmd.exe) هو إصدار Windows القديم وله قيود كبيرة مقارنة بأصداف PowerShell أو Unix. للحصول على تجربة أكثر ثراءً، فكر في استخدام [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-arlang.md) أو [WSL Integration](.././wsl-integration.i18n/wsl-integration-arlang.md) بدلاً من ذلك.

                                             ## تعليمات الإعداد

### 1. قم بإنشاء دليل للنصوص البرمجية الشخصية الخاصة بك (إذا لم تكن قد قمت بذلك بالفعل)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. أضف هذا الدليل إلى المسار الخاص بك (إعداد لمرة واحدة)

افتح **خصائص النظام → متغيرات البيئة** وأضف `%USERPROFILE%\bin` إلى متغير المستخدم `PATH`.

بدلاً من ذلك، قم بتشغيل هذا في موجه CMD مرتفع (يصبح ساري المفعول بعد إعادة فتح CMD):

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

                             ### 3. قم بإنشاء الملف الدفعي

افتح "المفكرة" أو أي محرر نصوص واحفظ ما يلي باسم `%USERPROFILE%\bin\s.bat`:

```bat
@echo off
:: --- STT Project Path Resolution ---

setlocal EnableDelayedExpansion

:: Check for arguments
if "%~1"=="" (
    echo question ^<your question^>
    exit /b 1
)

:: Collect all arguments into one string
set "QUERY=%*"

:: Call helper functions (must be defined or available on PATH)
call update_github_ip.bat

set SHORT_TIMEOUT_SECONDS=2
set LONG_TIMEOUT_SECONDS=70

:: Path shortcuts (adjust PROJECT_ROOT to your actual path if not set as env var)
set "PY_EXEC=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "CLI_SCRIPT=%PROJECT_ROOT%\scripts\py\cli_client.py"

:: Create a temp file
set "TEMP_FILE=%TEMP%\stt_output_%RANDOM%.txt"
set "TEMP_FILE_ERR=%TEMP%\stt_err_%RANDOM%.txt"

:: --- 1. First try (short timeout via 'timeout' workaround) ---
:: CMD has no built-in process timeout. We use 'start /wait' with a watchdog approach.
:: For a true timeout, PowerShell is called inline as a helper:
powershell -NoProfile -Command ^
    "$proc = Start-Process -FilePath '%PY_EXEC%' ^
        -ArgumentList '-u','%CLI_SCRIPT%','%QUERY%','--lang','de-DE','--unmasked' ^
        -RedirectStandardOutput '%TEMP_FILE%' ^
        -RedirectStandardError '%TEMP_FILE_ERR%' ^
        -NoNewWindow -PassThru; ^
    $done = $proc.WaitForExit(%SHORT_TIMEOUT_SECONDS%000); ^
    if (-not $done) { $proc.Kill(); exit 124 } else { exit $proc.ExitCode }"

set EXIT_CODE=%ERRORLEVEL%

:: Read output
set "OUTPUT="
if exist "%TEMP_FILE%" (
    set /p OUTPUT=<"%TEMP_FILE%"
    del "%TEMP_FILE%" "%TEMP_FILE_ERR%" 2>nul
)

:: --- Service check ---
findstr /C:"Verbindungsfehler" "%TEMP_FILE%" >nul 2>&1
set CONN_ERR=%ERRORLEVEL%

tasklist /FI "IMAGENAME eq streamlit.exe" 2>nul | find /I "streamlit.exe" >nul
set STREAMLIT_RUNNING=%ERRORLEVEL%

if %CONN_ERR%==0 (goto :restart)
if %STREAMLIT_RUNNING% NEQ 0 (goto :restart)
goto :check_exit

:restart
echo Service-Check: Backend oder Frontend fehlt. Starte neu...
call start_service.bat
echo ++++++++++++++++++++++++++++++++++++++++++++++++++
set "KIWIX_SCRIPT=%PROJECT_ROOT%\config\maps\plugins\standard_actions\wikipedia_local\de-DE\kiwix-docker-start-if-not-running.sh"
if exist "%KIWIX_SCRIPT%" (
    bash "%KIWIX_SCRIPT%"
)
echo ++++++++++++++++++++++++++++++++++++++++++++++++++
echo BITTE ERNEUT EINGEBEN: s %QUERY%
exit /b 1

:check_exit
if %EXIT_CODE%==124 (goto :long_timeout)
if %EXIT_CODE%==0 (
    echo %OUTPUT%
    exit /b 0
)
goto :error

:long_timeout
echo answer ^> %SHORT_TIMEOUT_SECONDS% sec. set Timeout= %LONG_TIMEOUT_SECONDS% s...

set "TEMP_FILE_2=%TEMP%\stt_output2_%RANDOM%.txt"
set "TEMP_FILE_2_ERR=%TEMP%\stt_err2_%RANDOM%.txt"

powershell -NoProfile -Command ^
    "$proc = Start-Process -FilePath '%PY_EXEC%' ^
        -ArgumentList '-u','%CLI_SCRIPT%','%QUERY%','--lang','de-DE','--unmasked' ^
        -RedirectStandardOutput '%TEMP_FILE_2%' ^
        -RedirectStandardError '%TEMP_FILE_2_ERR%' ^
        -NoNewWindow -PassThru; ^
    $done = $proc.WaitForExit(%LONG_TIMEOUT_SECONDS%000); ^
    if (-not $done) { $proc.Kill(); exit 124 } else { exit $proc.ExitCode }"

set EXIT_CODE_2=%ERRORLEVEL%

if exist "%TEMP_FILE_2%" (
    type "%TEMP_FILE_2%"
    del "%TEMP_FILE_2%" "%TEMP_FILE_2_ERR%" 2>nul
)

if %EXIT_CODE_2% NEQ 0 (
    echo WARNUNG: Timeout ^> %LONG_TIMEOUT_SECONDS% Sec.
)
exit /b 0

:error
echo ERROR
echo %OUTPUT%
exit /b %EXIT_CODE%
```

                                                          ### 4. اختبره

افتح نافذة CMD جديدة (حتى يتم تحميل PATH المحدث) واكتب:

```cmd
s your question here
```

                                          ## ملاحظات خاصة بـ CMD

- **لا توجد مهلة للعملية الأصلية**: لا يحتوي CMD على ما يعادل "مهلة" Unix. يقوم هذا البرنامج النصي بتفويض منطق المهلة المضمّن إلى "WaitForExit" الخاص بـ PowerShell. يجب أن يكون PowerShell متاحًا (موجود على جميع أنظمة Windows الحديثة).
- **`PROJECT_ROOT`**: قم بتعيين هذا كمتغير بيئة مستخدم دائم عبر خصائص النظام، أو قم بترميز المسار في ملف `.bat`.
- **البرامج النصية المساعدة**: يجب أن يكون `update_github_ip.bat` و`start_service.bat` موجودين في `PATH` أو في `%USERPROFILE%\bin`. هذه هي مكافئات CMD لوظائف الصدفة `update_github_ip` و`start_service`.
- **`bash` لبرنامج Kiwix النصي**: إذا تم تثبيت WSL، فسيكون `bash` متاحًا في CMD وسيتم تشغيل البرنامج النصي `.sh` مباشرة. بخلاف ذلك، قم بتعديل `kiwix-docker-start-if-not-running.sh` إلى ما يعادل `.bat`.
- **التعامل مع عرض الأسعار**: لدى CMD قواعد عرض أسعار صارمة وهشة. إذا كان استعلامك يحتوي على أحرف خاصة (`&`، `|`، `>`، `<`)، فقم بلف الاستعلام بالكامل بين علامتي اقتباس مزدوجتين: `s "your & question"`.
- **`تحديد set /p`**: يقرأ `set /p` السطر الأول فقط من الملف. بالنسبة للإخراج متعدد الأسطر، استخدم "type" لطباعة الملف مباشرةً (كما هو الحال في فرع المهلة الطويلة).

                                                                  ## سمات

- **المسارات الديناميكية**: تعمل على حل المسارات تلقائيًا عبر متغير البيئة `PROJECT_ROOT`.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فسيتم استدعاء "start_service.bat" ومحاولة بدء تشغيل خدمات ويكيبيديا المحلية.
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.