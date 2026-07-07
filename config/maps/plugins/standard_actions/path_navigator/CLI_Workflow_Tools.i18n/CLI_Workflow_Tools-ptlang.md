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



## 1. Seleção rápida de arquivo (comando Aura)

A ação `path_navigator` usa o seguinte comando `fzf` compatível com Git. Seu objetivo é gerar um caminho de arquivo diretamente na área de transferência do sistema.

**Lógica de comando:**
- Usa `git ls-files` dentro de um repositório Git (exclui arquivos ignorados).
- Volta para `encontrar . -type f` fora de um repositório Git.
- Produz o caminho selecionado para a área de transferência usando `xclip -selection clipboard`.

## 2. Execução rápida de arquivos (a função 'k')

Para completar o loop, a função shell personalizada `k` é usada. Esta função segue o caminho da área de transferência e abre instantaneamente o arquivo em `kate`.

### Implementação

Adicione a seguinte função ao arquivo de configuração do seu shell (por exemplo, `~/.bashrc`, `~/.zshrc`):

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

### Uso

1. Use o comando `path_navigator` (por exemplo, digite `search file` em sua ferramenta de gatilho).
2. Encontre e selecione o arquivo desejado (por exemplo, `src/main/config.py`).
3. Em seu terminal, digite `k` e pressione **ENTER**.
4. O arquivo abre instantaneamente no Kate.
__CODE_BLOCK_2__