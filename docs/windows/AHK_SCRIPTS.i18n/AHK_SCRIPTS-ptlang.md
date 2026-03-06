### Documentação de Markdown (`docs/AHK_SCRIPTS.md`)

# Infraestrutura AutoHotkey para SL5-Aura-Service

Como o Windows lida com bloqueios de arquivos e teclas de atalho do sistema de maneira diferente do Linux, este projeto usa um conjunto de scripts AutoHotkey (v2) para preencher a lacuna entre o mecanismo Python STT e a interface do usuário do Windows.

## Visão geral dos scripts

### 1. `trigger-hotkeys.ahk`
* **Objetivo:** A interface de usuário principal para controlar o serviço.
* **Principais recursos:**
* Intercepta **F10** e **F11** para iniciar/parar o ditado.
* Usa um `Keyboard Hook` para substituir o comportamento padrão do sistema Windows (por exemplo, F10 ativando a barra de menu).
* **Implantação:** Projetado para ser registrado através do Agendador de Tarefas do Windows com "Privilégios Mais Altos" para que possa capturar teclas de atalho mesmo quando o usuário estiver trabalhando em um aplicativo de nível Administrador.

### 2. `type_watcher.ahk`
* **Objetivo:** Atuar como o "Consumidor" no pipeline STT.
* **Principais recursos:**
* Observa um diretório temporário para arquivos `.txt` recebidos gerados pelo mecanismo Python.
* **Máquina de Estado (Mapa Zumbi):** Implementa um mapa baseado em memória para garantir que cada arquivo seja digitado exatamente uma vez. Isso evita a "digitação dupla" causada por eventos redundantes do sistema de arquivos do Windows (Adicionado/Modificado).
* **Digitação Segura:** Usa `SendText` para garantir que caracteres especiais sejam tratados corretamente em qualquer editor ativo.
* **Limpeza confiável:** Gerencia a exclusão de arquivos com uma lógica de repetição para lidar com bloqueios de acesso a arquivos do Windows.

### 3. `scripts/ahk/sync_editor.ahk`
* **Objetivo:** Garante a sincronização perfeita entre o disco e o editor de texto (por exemplo, Notepad++).
* **Principais recursos:**
* **Salvar sob demanda:** Pode ser acionado pelo Python para forçar um `Ctrl+S` no editor antes que o mecanismo leia o arquivo.
* **Dialog Automator:** Detecta e confirma automaticamente caixas de diálogo de recarga de "Arquivo modificado por outro programa", criando uma experiência de atualização fluida em tempo real.
* **Feedback visual:** Fornece caixas de notificação de curta duração para informar ao usuário que as correções estão sendo aplicadas.

### 4. `scripts/notification_watcher.ahk`
* **Objetivo:** Fornece feedback da UI para processos em segundo plano.
* **Principais recursos:**
* Monitora arquivos ou eventos de status específicos para exibir notificações ao usuário.
* Desacopla a lógica de "calcular" uma mensagem (Python) da "exibição" dela (AHK), garantindo que o mecanismo STT principal não seja bloqueado pelas interações da UI.


---

### Fallback não administrativo
Se o aplicativo for executado sem privilégios de administrador:
- **Funcionalidade:** O serviço permanece totalmente funcional.
- **Limitações das teclas de atalho:** Teclas reservadas pelo sistema, como **F10**, ainda podem acionar o menu do Windows. Neste caso, é recomendado alterar as teclas de atalho para teclas que não sejam do sistema (por exemplo, `F9` ou `Insert`).
- **Agendador de tarefas:** Se a tarefa "AuraDictation_Hotkeys" foi criada durante uma instalação de administrador, o script será executado com privilégios elevados, mesmo para um usuário padrão. Caso contrário, `start_dictation.bat` iniciará uma instância local de nível de usuário silenciosamente.

---

### 3. Warum "nervige Meldungen" erscheinen e wie man sie im AHK-Code stoppt
Uma segurança, dass Skript selbst niemals den Nutzer mit Popups stört, füge dieses "Silent-Flags" oben in deine `.ahk` Dateien ein:

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. Estratégia para as teclas de atalho (alternativa F10)
Da F10, ohne Admin-Rechte unter Windows fast unmöglich sauber fangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Zusammenfassung der Verbesserungen:
1. **Batch-Data:** Por favor, `start "" /b`, um das janelas pretas zu vermeiden, und prüft vorher, ob der Admin-Task schon läuft.
2. **Transparência:** O documento erklärt nun ofen: "Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10".
3. **Skript AHK:** Digite `#SingleInstance Force`, e a caixa de diálogo "Uma instância mais antiga está em execução" é exibida.

Damit wirkt die Software viel professioneller ("Smooth"), da sie im Hintergrund startet, ohne dass der Nutzer mit technischen Details ou Bestätigungsfenstern konfrontiert wird.
  
  
---

### Por que esta documentação é importante:
Ao documentar o requisito **"Mapa Zumbi"** e **"Agendador de Tarefas/Administrador"**, você explica a outros desenvolvedores (e a você mesmo no futuro) por que o código é mais complexo do que um simples script Linux. Ele transforma "soluções alternativas estranhas" em "soluções projetadas para as limitações do Windows".

(s,29.1.'26 11:02 qui)