# Notificações de fluxo de trabalho (alertas de áudio)

Para melhorar a produtividade, você pode configurar um alias local do Git que envia seu código e alerta você automaticamente (por voz ou som) assim que o fluxo de trabalho do GitHub Actions for concluído. Isso evita o "cansaço de assistir ao GitHub" e permite que você se concentre em outras tarefas.

### Pré-requisitos

Você precisa do **GitHub CLI** e de um mecanismo de conversão de texto em fala ou reprodutor de som instalado em seu sistema.

**Para Manjaro/Arch Linux:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### Configurar

Execute o seguinte comando em seu terminal para criar um alias global do Git chamado `pushsound`:

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### Uso

Em vez de `git push`, simplesmente execute:
```bash
git pushsound
```
Seu terminal aguardará a conclusão do fluxo de trabalho e então anunciará: *"todo o fluxo de trabalho do github foi concluído"*.

---

### Personalização e alternativas

Dependendo da sua preferência, talvez você queira usar um nome alternativo ou um método de notificação diferente.

#### 1. Nomes de alias recomendados
Se `pushsound` for muito longo para digitar, considere estas alternativas:
* `git pw` (Push & Watch) — **Recomendado para velocidade.**
* `git sync` (Implica pressionar e esperar pelo "sinal verde")
* `git palert` (Alerta Push)

#### 2. Estilos de notificação
Você pode trocar a parte `espeak-ng` por outros tipos de alertas:

* **Notificação na área de trabalho:**
`... && notify-send "Ação do GitHub" "Fluxo de trabalho concluído!"`
* **Som do sistema (campainha):**
`... && papal /usr/share/sounds/freedesktop/stereo/complete.oga`
* **Combinação (Som + Voz):**
`... && papall /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Concluído"`

#### 3. Avançado: Versão Team-Safe
Se vários desenvolvedores estiverem enviando para o mesmo repositório simultaneamente, o comando padrão poderá rastrear a execução errada. Use esta versão "Branch-Safe" para monitorar apenas sua própria filial atual:

##### verifica apenas o primeiro fluxo de trabalho:

__CODE_BLOCO_3__

##### verifica todos os fluxos de trabalho registrados no GitHub

git config --global alias.pushsound '!f() { git push && echo "Aguardando o GitHub registrar fluxos de trabalho..." && sleep 5 && SHA=$(git rev-parse HEAD) && SUCCESS=0 && for id in $(gh run list --commit $SHA --json databaseId -q ".[].databaseId"); do echo "Assistindo ao fluxo de trabalho $id..." && gh run watch $id --exit-status || SUCESSO=1; feito; [ $SUCCESS -eq 0 ] && espeak-ng "todos os fluxos de trabalho bem-sucedidos" || espeak-ng “pelo menos um fluxo de trabalho falhou”; }; f'


### Solução de problemas
* **"Nenhuma execução encontrada":** Incluímos um `sleep 3` porque o GitHub leva um momento para registrar o push e iniciar o fluxo de trabalho. Se você tiver uma conexão muito lenta, pode ser necessário aumentar para `sleep 5`.
* **Bipes de terminal:** Se `espeak-ng` não funcionar, certifique-se de que seu áudio não esteja silenciado e que o pacote esteja instalado corretamente.