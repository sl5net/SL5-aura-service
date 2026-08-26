# تشغيل تلقائي لنظام التشغيل Windows

                                                              #start_aura.bat

يرجى التحقق من هذا الملف `start_aura.bat` في مجلد مشروع SL5net Aura.

**الخيار أ — مجلد بدء التشغيل (أبسط نافذة وحدة تحكم مرئية)**

1. قم بإنشاء ملف دفعي، على سبيل المثال. `C:\Users\<YourName>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. اضغط على Win + R، واكتب Shell:startup، ثم اضغط على Enter. هذا يفتح:
`C:\Users\<YourName>\AppData\Roaming\Microsoft\Windows\قائمة ابدأ\البرامج\بدء التشغيل`
3. انقر بزر الماوس الأيمن داخل هذا المجلد → **جديد → اختصار** → قم بتوجيهه إلى `aura_engine.bat`. يتم تشغيله الآن عند كل تسجيل دخول.

**الخيار ب — برنامج جدولة المهام (موصى به: مخفي، بدون وميض النافذة)**

                  قم بتشغيل هذا مرة واحدة في PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

يؤدي هذا إلى إنشاء مهمة `AuraEngine` التي يتم تشغيلها عند كل تسجيل دخول، وتعمل بالكامل في الخلفية، وتكتب في نفس `aura_engine.log` المستخدم في إصدارات Linux/Mac.

                             **اختبار دون تسجيل الخروج:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

اضبط "Ubuntu" على اسم التوزيعة الفعلي الخاص بك - تحقق من خلال:

```powershell
wsl -l -v
```

                                              **تأكد من تسجيله:**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

                                                   **تعطيل/إزالة:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

هل تقوم بالفعل بتشغيل هذا المشروع من خلال WSL على هذا الجهاز الذي يعمل بنظام Windows، أم أنه يحتاج إلى إعادة كتابة Windows/PowerShell الأصلي لـ `restart_venv_and_run-server.sh` (لا يتضمن WSL)؟