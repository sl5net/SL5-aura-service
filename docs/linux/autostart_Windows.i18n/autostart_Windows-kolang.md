# 윈도우 자동 시작

# start_aura.bat

SL5net Aura의 프로젝트 폴더에 있는 `start_aura.bat` 파일을 확인하세요.

**옵션 A - 시작 폴더(가장 간단하고 보이는 콘솔 창)**

1. 배치 파일을 만듭니다. `C:\Users\<사용자 이름>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. `Win + R`을 누르고 `shell:startup`을 입력한 후 Enter를 누르세요. 다음과 같이 열립니다.
`C:\Users\<사용자 이름>\AppData\Roaming\Microsoft\Windows\시작 메뉴\프로그램\시작`
3. 해당 폴더 내부를 마우스 오른쪽 버튼으로 클릭하고 → **새로 만들기 → 바로가기** → `aura_engine.bat`를 지정합니다. 이제 로그인할 때마다 실행됩니다.

**옵션 B - 작업 스케줄러(권장: 숨김, 창 플래시 없음)**

PowerShell에서 다음을 한 번 실행합니다.

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

이렇게 하면 로그온할 때마다 실행되고 백그라운드에서 완전히 실행되며 Linux/Mac 버전에서 사용되는 것과 동일한 'aura_engine.log'에 기록하는 'AuraEngine' 작업이 생성됩니다.

**로그아웃하지 않고 테스트:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

'Ubuntu'를 실제 배포판 이름으로 조정하세요. 다음을 확인하세요.

```powershell
wsl -l -v
```

**등록되었는지 확인하세요.**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**비활성화/제거:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

실제로 해당 Windows 시스템에서 WSL을 통해 이 프로젝트를 실행합니까, 아니면 'restart_venv_and_run-server.sh'(WSL이 포함되지 않음)의 기본 Windows/PowerShell 재작성이 필요합니까?