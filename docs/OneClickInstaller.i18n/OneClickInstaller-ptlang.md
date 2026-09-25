> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# Instalador com 1 Clique (Configuração Zero)

Coloque o **Aura** em funcionamento no seu computador com um único clique. Nenhum conhecimento de programação, comandos no terminal ou configuração manual do Python é necessário.

---

## Zero Pré-requisitos

Você **não** precisa:
- Python pré-instalado
- Repositórios Git ou de código
- Experiência com linha de comando ou terminal

---

## Início Rápido

### Método 1: Linha Única na Web (Mais Rápido e Recomendado para Linux / macOS)
Economiza cerca de 30 segundos de manuseio manual de arquivos e inicia imediatamente no seu terminal:

**Linux e macOS:**
#### Web One-Liner CodeBerg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
ou
#### Web One-Liner GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Web One-Liner CodeBerg

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
ou
#### Web One-Liner github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Método 2: Binário Independente (Windows e Clique na Área de Trabalho)

### 2.1 Baixar o Instalador
Baixe o arquivo único do instalador correspondente ao seu sistema operacional a partir da [Última Versão no GitHub]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Execute o Instalador

renomeie aura-installer-windows.exe.zip para aura-installer-windows.exe

Clique duas vezes no arquivo baixado. Uma janela de instalação aparecerá e preparará automaticamente o ambiente.

### 2.3. Começar a ditar
Uma vez terminado, o Aura cria um atalho na área de trabalho e começa a escutar imediatamente.

---

## O Que Acontece Automaticamente?

Quando você executa o instalador, o Aura automaticamente:
- Configura o mecanismo local e privado de reconhecimento de fala.
- Faz o download dos modelos de voz padrão.
- Configura todos os atalhos de sistema e inicializadores de área de trabalho necessários.

---

## Detalhes de Instalação e Requisitos

- **Duração da Instalação:** Aproximadamente 2–3 minutos.
- **Espaço em Disco Necessário:** Mínimo ~1,5 GB (até 2,5 GB dependendo dos modelos de linguagem selecionados).
- **Diretório de Instalação:**
  - **Linux e macOS:** `~/opt/sl5-aura-service`
  - **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Próximos Passos

- **Modo Vovó:** Digite uma única palavra no seu arquivo de regras e veja o Aura criar regras automaticamente.
- **Aprenda com Koans:** Explore conceitos passo a passo em [Getting Started](../GettingStarted.i18n/GettingStarted-ptlang.md).
