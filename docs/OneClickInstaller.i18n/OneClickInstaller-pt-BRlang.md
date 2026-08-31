# Instalador com 1 clique (configuração zero)

Coloque o **Aura** em funcionamento em sua máquina com um único clique. Não é necessário conhecimento de programação, comandos de terminal ou configuração manual do Python.

---

## Zero Pré-requisitos

Você **não** precisa de:
- Python pré-instalado
- Git ou repositórios de código
- Experiência em linha de comando ou terminal

---

## Início rápido

### Método 1: Web One-Liner (mais rápido e recomendado para Linux/macOS)
Economiza cerca de 30 segundos de manipulação manual de arquivos e inicia imediatamente em seu terminal:

**Linux e macOS:**

```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
```bash

# In development - please use Method 2 (standalone binary) for Windows

irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Método 2: binário independente (clique no Windows e na área de trabalho)

### 2.1 Baixe o instalador
Baixe o arquivo do instalador único correspondente ao seu sistema operacional na [versão mais recente do GitHub]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Execute o instalador

renomeie aura-installer-windows.exe.zip para aura-installer-windows.exe

Clique duas vezes no arquivo baixado. Uma janela de configuração aparecerá e preparará automaticamente o ambiente.

###2.3. Comece a ditar
Depois de terminar, o Aura cria um atalho na área de trabalho e começa a ouvir imediatamente.

---

## O que acontece automaticamente?

Ao executar o instalador, o Aura automaticamente:
- Configura o mecanismo de reconhecimento de fala local e privado.
- Baixa os modelos de voz padrão.
- Configura todos os atalhos de sistema e iniciadores de área de trabalho necessários.

---

## Detalhes e requisitos de instalação

- **Duração da instalação:** Aproximadamente 2–3 minutos.
- **Espaço em disco necessário:** Mínimo de aproximadamente 1,5 GB (até 2,5 GB dependendo dos modelos de idioma selecionados).
- **Diretório de instalação:**
- **Linux e macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Próximas etapas

- **Modo Vovó:** Digite uma única palavra em seu arquivo de regras e observe a criação automática de regras do Aura.
- **Aprenda com Koans:** Explore conceitos passo a passo no [Getting Started](../GettingStarted.i18n/GettingStarted-pt-BRlang.md).