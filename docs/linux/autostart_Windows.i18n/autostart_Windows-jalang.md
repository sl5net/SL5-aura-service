# Windowsの自動起動

#start_aura.bat

SL5net Aura のプロジェクトフォルダーにあるこのファイル `start_aura.bat` を確認してください。

**オプション A — スタートアップ フォルダー (最もシンプルで目に見えるコンソール ウィンドウ)**

1. バッチ ファイルを作成します。 `C:\Users\<あなたの名前>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. 「Win + R」を押し、「shell:startup」と入力して Enter を押します。これで開きます:
`C:\Users\<あなたの名前>\AppData\Roaming\Microsoft\Windows\スタート メニュー\プログラム\スタートアップ`
3. そのフォルダ内を右クリック→**新規→ショートカット**→「aura_engine.bat」をポイントします。ログインするたびに実行されるようになりました。

**オプション B — タスク スケジューラ (推奨: 非表示、ウィンドウ フラッシュなし)**

PowerShell でこれを 1 回実行します。

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

これにより、ログオンのたびに起動され、完全にバックグラウンドで実行され、Linux/Mac バージョンで使用されているのと同じ `aura_engine.log` に書き込まれるタスク `AuraEngine` が作成されます。

**ログアウトせずにテストします:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

「Ubuntu」を実際のディストリビューション名に合わせて調整します。次のように確認してください。

```powershell
wsl -l -v
```

**登録されていることを確認してください:**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**無効化/削除:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

実際にこのプロジェクトを Windows マシン上の WSL 経由で実行しますか、それともネイティブの Windows/PowerShell による「restart_venv_and_run-server.sh」の書き換えが必要ですか (WSL は関係ありません)。