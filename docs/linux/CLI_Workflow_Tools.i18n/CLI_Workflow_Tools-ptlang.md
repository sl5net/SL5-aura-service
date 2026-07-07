# Guia de instalação das ferramentas de fluxo de trabalho CLI

Algumas ações no plugin path navigator dependem de utilitários de linha de comando externos para realizar pesquisas difusas, listar arquivos e manipular a área de transferência. Se essas ferramentas estiverem faltando, você verá um aviso no console do sistema.

Abaixo estão as instruções de instalação para cada sistema operacional compatível.

## Utilitários necessários

* **`fzf`**: Localizador difuso de linha de comando de uso geral.
* **`find`** (ou `fd`): Utilitário padrão de busca de arquivos.
* **Ferramenta de área de transferência**: usada para canalizar a saída diretamente para a área de transferência do sistema.
* **Linux:** `xclip` (requer ambiente X11).
* **macOS:** `pbcopy` (pré-instalado).
* **Windows:** `clip` (pré-instalado).
* **`file`**: Determina os tipos de arquivo para visualizações completas do terminal.

---

## Instruções de instalação

### 1.Linux (Arch/Manjaro)
Como seu sistema roda em Manjaro, você pode instalar os pacotes necessários usando `pacman`:

```bash
sudo pacman -S fzf findutils xclip file
```

### 2.Linux (Debian/Ubuntu/Mint)
Em sistemas baseados em Debian, use `apt`:

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

###3.macOS
Use o gerenciador de pacotes [Homebrew](https://brew.sh/) para instalar as ferramentas ausentes:

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. Janelas
Se você estiver usando Windows, recomendamos instalar `fzf` via [Scoop](https://scoop.sh/) ou [Winget](https://github.com/microsoft/winget-cli):

__CODE_BLOCO_3__
```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```