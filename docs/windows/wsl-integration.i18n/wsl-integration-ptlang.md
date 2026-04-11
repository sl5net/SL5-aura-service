# Integração WSL (subsistema Windows para Linux)

WSL permite executar um ambiente Linux completo diretamente no Windows. Depois de configurada, a integração do shell STT funciona **de forma idêntica aos guias Linux Bash ou Zsh** — nenhuma adaptação específica do Windows é necessária para a função do shell em si.

> **Recomendado para:** usuários do Windows que estão familiarizados com um terminal Linux ou que já possuem o WSL instalado para trabalho de desenvolvimento. WSL oferece a experiência mais fiel e o menor comprometimento de compatibilidade.

## Pré-requisitos

### Instale WSL (configuração única)

Abra o PowerShell ou CMD **como administrador** e execute:

```powershell
wsl --install
```

Isso instala o WSL2 com Ubuntu por padrão. Reinicie sua máquina quando solicitado.

Para instalar uma distribuição específica:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

Liste todas as distribuições disponíveis:

```powershell
wsl --list --online
```

### Verifique sua versão WSL

__CODE_BLOCO_3__

Certifique-se de que a coluna `VERSION` mostre `2`. Se mostrar `1`, atualize com:

```powershell
wsl --list --verbose
```

## Integração Shell dentro do WSL

Assim que o WSL estiver em execução, abra seu terminal Linux e siga o **guia do shell do Linux** para o seu shell preferido:

| Concha | Guia |
|-------|-------|
| Bash (padrão WSL) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-ptlang.md) |
| Zsh | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-ptlang.md) |
| Peixe | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-ptlang.md) |
| Ksh | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-ptlang.md) |
| POSIX sh / traço | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-ptlang.md) |

Para a configuração padrão do Ubuntu/Debian WSL com Bash, o caminho rápido é:

__CODE_BLOCO_5__

## Considerações específicas da WSL

### Acessando arquivos do Windows pelo WSL

Suas unidades do Windows estão montadas em `/mnt/`:

```powershell
wsl --set-version <DistroName> 2
```

Se o seu projeto reside no sistema de arquivos do Windows (por exemplo, `C:\Projects\stt`), defina `PROJECT_ROOT` como:

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

Adicione esta linha ao seu `~/.bashrc` (ou o equivalente para o seu shell) **acima** da função `s()`.

> **Dica de desempenho:** Para melhor desempenho de E/S, mantenha os arquivos do projeto dentro do sistema de arquivos WSL (por exemplo, `~/projects/stt`) em vez de `/mnt/c/...`. O acesso entre sistemas de arquivos entre WSL e Windows é significativamente mais lento.

### Ambiente virtual Python dentro do WSL

Crie e use um ambiente virtual Linux padrão dentro do WSL:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

O caminho `PY_EXEC` na função (`$PROJECT_ROOT/.venv/bin/python3`) funcionará corretamente como está.

### Executando `s` no Terminal do Windows

[Windows Terminal](https://aka.ms/terminal) é a forma recomendada de usar WSL no Windows. Ele oferece suporte a várias guias, painéis e perfis para cada distribuição WSL. Instale-o na Microsoft Store ou via:

__CODE_BLOCO_9__

Defina sua distribuição WSL como o perfil padrão nas configurações do Terminal do Windows para uma experiência mais perfeita.

### Docker e Kiwix dentro do WSL

O script auxiliar Kiwix (`kiwix-docker-start-if-not-running.sh`) requer Docker. Instale o Docker Desktop para Windows e habilite a integração WSL 2:

1. Baixe e instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Em Docker Desktop → Configurações → Recursos → Integração WSL, habilite sua distribuição WSL.
3. Verifique dentro do WSL:
```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

### Chamando a função WSL `s` do Windows (opcional)

Se quiser invocar o atalho `s` de uma janela CMD do Windows ou PowerShell sem abrir um terminal WSL, você pode envolvê-lo:

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
winget install Microsoft.WindowsTerminal
```

> O sinalizador `-i` carrega um shell interativo para que seu `~/.bashrc` (e a função `s`) seja obtido automaticamente.

## Características

- **Compatibilidade total com Linux**: Todas as ferramentas Unix (`timeout`, `pgrep`, `mktemp`, `grep`) funcionam nativamente — não são necessárias soluções alternativas.
- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através da variável `PROJECT_ROOT` definida na configuração do seu shell.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `start_service` e os serviços locais da Wikipedia (o Docker deve estar em execução).
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.