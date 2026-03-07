# Dica de desenvolvedor: copie automaticamente a saída do console para a área de transferência

**Categoria:** Produtividade Linux/Shell  
**Plataforma:** Linux (zsh + Konsole/KDE)

---

## O problema

Ao trabalhar com assistentes de IA, muitas vezes você precisa copiar a saída do terminal e colá-la no chat. Isso geralmente significa:
1. Execute o comando
2. Selecione a saída com o mouse
3. Copie
4. Mude para o navegador
5. Cole

São muitos passos.

---

## A solução: captura automática via `preexec` / `precmd`

Adicione isto ao seu `~/.zshrc`:

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}


precmd() {
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        cleaned=$(cat ~/t.txt \
            | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | sed "s|$HOME|~|g" \
            | sed 's/[^[:print:]]//g' \
            | grep -v '^$')
        if [ -n "$cleaned" ]; then
            echo "$cleaned" | xclip -selection clipboard
            echo "[📋 In Zwischenablage kopiert]"
        fi
    fi
}

```

Então recarregue:
```bash
source ~/.zshrc
```

### Resultado

Após cada comando, a saída é automaticamente na sua área de transferência — pronta para ser colada no seu chat de IA com **Ctrl+V**.

A saída também é sempre salva em `~/t.txt` para referência.

---

##Como funciona

| Parte | O que faz |
|------|-------------|
| `preexec()` | Executado antes de cada comando, redireciona a saída para `~/t.txt` |
| `precmd()` | Executa após cada comando, restaura stdout e copia para a área de transferência |
| `tee ~/t.txt` | Salva a saída em um arquivo enquanto ainda a mostra no terminal |
| `sed '...'` | Remove sequências de escape de título do KDE Konsole (`]2;...` `]1;`) |
| `xclip` | Copia a saída limpa para a área de transferência |

---

## Requisitos

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ O que NÃO fazer

**Não** use `fc -ln -1 | bash` para executar novamente o último comando:

__CODE_BLOCO_3__

Isso reexecuta cada comando após sua conclusão, o que pode causar efeitos colaterais destrutivos - por exemplo, sobrescrever arquivos, reexecutar `git commit`, reexecutar `sed -i`, etc.

A abordagem `preexec`/`precmd` acima captura a saída **durante** a execução — segura e confiável.