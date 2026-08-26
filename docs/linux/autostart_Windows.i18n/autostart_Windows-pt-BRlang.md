# Inicialização automática do Windows

#start_aura.bat

verifique este arquivo `start_aura.bat` na pasta do projeto SL5net Aura.

**Opção A — Pasta de inicialização (janela de console mais simples e visível)**

1. Crie um arquivo em lote, por exemplo. `C:\Users\<SeuNome>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. Pressione `Win + R`, digite `shell:startup` e pressione Enter. Isso abre:
`C:\Users\<SeuNome>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. Clique com o botão direito dentro dessa pasta → **Novo → Atalho** → aponte para `aura_engine.bat`. Agora ele é executado a cada login.

**Opção B — Agendador de tarefas (recomendado: oculto, sem flash de janela)**

Execute isto uma vez no PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

Isso cria uma tarefa `AuraEngine` que é acionada a cada login, é executada totalmente em segundo plano e grava no mesmo `aura_engine.log` usado nas versões Linux/Mac.

**Teste sem sair:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

Ajuste `Ubuntu` para o nome real da sua distribuição - verifique com:

__CODE_BLOCO_3__

**Verifique se está registrado:**

```powershell
wsl -l -v
```

**Desativar/remover:**

__CODE_BLOCO_5__

Você realmente executa este projeto por meio de WSL nessa máquina Windows ou ele precisa de uma reescrita nativa do Windows/PowerShell de `restart_venv_and_run-server.sh` (sem WSL envolvido)?