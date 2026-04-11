# تكامل PowerShell (Windows)

لتسهيل التفاعل مع STT (تحويل الكلام إلى نص) CLI، يمكنك إضافة وظيفة اختصار إلى ملف تعريف PowerShell الخاص بك. يتيح لك ذلك كتابة "سؤالك" ببساطة في أي نافذة PowerShell.

> **ينطبق على:** Windows PowerShell 5.1 وPowerShell 7+ (مستحسن). يمكن تثبيت PowerShell 7 من [Microsoft Store](https://aka.ms/powershell) أو عبر "winget install Microsoft.PowerShell".

                                             ## تعليمات الإعداد

### 1. السماح بتنفيذ البرنامج النصي (الإعداد لمرة واحدة)

يقوم PowerShell بحظر البرامج النصية بشكل افتراضي. افتح PowerShell ** كمسؤول ** وقم بتشغيل:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

                 ### 2. افتح ملف تعريف PowerShell الخاص بك

```powershell
notepad $PROFILE
```

إذا لم يكن الملف موجودًا بعد، فقم بإنشائه أولاً:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

       ### 3. الصق الكتلة التالية في نهاية الملف

```powershell
# --- STT Project Path Resolution ---
function s {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Query
    )

    if ($Query.Count -eq 0) {
        Write-Host "question <your question>"
        return
    }

    $QueryString = $Query -join " "

    Update-GithubIp   # equivalent of update_github_ip

    $SHORT_TIMEOUT_SECONDS = 2
    $LONG_TIMEOUT_SECONDS  = 70

    # Path shortcuts
    $PY_EXEC   = "$env:PROJECT_ROOT\.venv\Scripts\python.exe"
    $CLI_SCRIPT = "$env:PROJECT_ROOT\scripts\py\cli_client.py"

    $TempFile = [System.IO.Path]::GetTempFileName()

    # --- 1. First try (short timeout) ---
    $proc = Start-Process -FilePath $PY_EXEC `
        -ArgumentList "-u", "`"$CLI_SCRIPT`"", "`"$QueryString`"", "--lang", "de-DE", "--unmasked" `
        -RedirectStandardOutput $TempFile `
        -RedirectStandardError  "$TempFile.err" `
        -NoNewWindow -PassThru

    $finished = $proc.WaitForExit($SHORT_TIMEOUT_SECONDS * 1000)
    $Output   = Get-Content $TempFile -Raw -ErrorAction SilentlyContinue

    if (-not $finished) {
        # Still running — this is the timeout case
        $ExitCode = 124
    } else {
        $ExitCode = $proc.ExitCode
    }

    Remove-Item $TempFile, "$TempFile.err" -ErrorAction SilentlyContinue

    # --- Service check ---
    $streamlitRunning = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
    if (($Output -match "Verbindungsfehler") -or (-not $streamlitRunning)) {
        Write-Host "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        Start-Service-STT   # equivalent of start_service
        Write-Host "++++++++++++++++++++++++++++++++++++++++++++++++++"

        $KiwixScript = "$env:PROJECT_ROOT\config\maps\plugins\standard_actions\wikipedia_local\de-DE\kiwix-docker-start-if-not-running.sh"
        if (Test-Path $KiwixScript) {
            bash $KiwixScript
        }

        Write-Host "++++++++++++++++++++++++++++++++++++++++++++++++++"
        Write-Host "BITTE ERNEUT EINGEBEN: s $QueryString"
        return
    }

    # --- 2. Timeout OR immediate success ---
    if ($ExitCode -eq 124 -or $ExitCode -eq 0) {
        if ($ExitCode -eq 0) {
            Write-Host $Output
            return
        }

        Write-Host "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."

        $TempFile2 = [System.IO.Path]::GetTempFileName()
        $proc2 = Start-Process -FilePath $PY_EXEC `
            -ArgumentList "-u", "`"$CLI_SCRIPT`"", "`"$QueryString`"", "--lang", "de-DE", "--unmasked" `
            -RedirectStandardOutput $TempFile2 `
            -RedirectStandardError  "$TempFile2.err" `
            -NoNewWindow -PassThru

        $finished2 = $proc2.WaitForExit($LONG_TIMEOUT_SECONDS * 1000)
        $Output2   = Get-Content $TempFile2 -Raw -ErrorAction SilentlyContinue
        $ExitCode2 = if ($finished2) { $proc2.ExitCode } else { 124 }

        Remove-Item $TempFile2, "$TempFile2.err" -ErrorAction SilentlyContinue

        Write-Host $Output2

        if ($ExitCode2 -ne 0) {
            Write-Host "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec."
        }
        return
    }

    # --- Unexpected error ---
    Write-Host "ERROR"
    Write-Host $Output
}
```

    ### 4. قم بإعادة تحميل ملف التعريف الخاص بك

```powershell
. $PROFILE
```

                 ## ملاحظات خاصة بنظام التشغيل Windows

- **مسار بايثون**: في نظام التشغيل Windows، يكون الملف الثنائي للبيئة الافتراضية هو `.venv\Scripts\python.exe` بدلاً من `.venv/bin/python3`. اضبط `$PY_EXEC` إذا كان الإعداد الخاص بك مختلفًا.
- **`PROJECT_ROOT` متغير البيئة**: قم بتعيين هذا في متغيرات بيئة النظام لديك، أو قم بإضافة السطر التالي أعلى الوظيفة في ملف التعريف الخاص بك:
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: أدوات Unix هذه غير متوفرة محليًا. يستخدم البرنامج النصي أعلاه مكافئات PowerShell الأصلية (`WaitForExit` مع مهلة بالمللي ثانية و`GetTempFileName()`).
   - **`pgrep`**: تم استبداله بـ `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`**: يجب تعريفها على أنها وظائف PowerShell (`Start-Service-STT`، `Update-GithubIp`) في نفس ملف التعريف، قبل وظيفة `s`.
- **برنامج WSL Kiwix النصي**: إذا كان `bash` متاحًا (عبر WSL)، فسيتم تشغيل البرنامج النصي المساعد `.sh` كما هو. بخلاف ذلك، قم بتكييفه مع ما يعادل `.ps1` أو `.bat`.
- **إصدارات PowerShell المتعددة**: يشير `$PROFILE` إلى ملفات مختلفة لـ Windows PowerShell 5.1 وPowerShell 7. للتحقق من ملف التعريف النشط، قم بتشغيل `$PROFILE` في كل إصدار.

                                                                  ## سمات

- **المسارات الديناميكية**: يتم العثور على جذر المشروع تلقائيًا عبر متغير البيئة `PROJECT_ROOT`.
- **إعادة التشغيل التلقائي**: إذا كانت الواجهة الخلفية معطلة، فإنها تحاول تشغيل "Start-Service-STT" وخدمات ويكيبيديا المحلية.
- **المهلات الذكية**: حاول الاستجابة السريعة لمدة ثانيتين أولاً، ثم ارجع إلى وضع المعالجة العميقة لمدة 70 ثانية.