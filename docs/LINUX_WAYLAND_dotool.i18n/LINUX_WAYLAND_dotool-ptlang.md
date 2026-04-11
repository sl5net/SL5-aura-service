# dotool no Wayland – Configuração e solução de problemas

`dotool` é necessário para que Aura digite texto em outros aplicativos no Wayland.
Ao contrário do `xdotool`, ele se comunica diretamente com o kernel do Linux via `uinput`
e funciona em **X11 e Wayland**.

No X11, `xdotool` é usado por padrão. `dotool` é opcional no X11, mas
recomendado para melhor estabilidade de layout (especialmente com tremas).

---

## 1. Instale o dotool

**Arch/Manjaro/CachyOS (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu/Debian (se disponível em repositórios):**
```bash
sudo apt install dotool
```

**Se não estiver em repositórios — compile a partir do código-fonte:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. Permitir que o dotool seja executado sem root (obrigatório)

`dotool` precisa de acesso a `/dev/uinput`. Sem isso, falhará silenciosamente.

__CODE_BLOCO_3__

**É necessário fazer login novamente** após a mudança de grupo para que ela entre em vigor.

---

## 3. Verifique a instalação

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Se `groups` não mostrar `input`, saia e entre novamente (ou reinicie).

---

## 4. Como Aura usa dotool

`type_watcher.sh` do Aura automaticamente:

- Detecta Wayland via `$WAYLAND_DISPLAY` e seleciona `dotool`
- Inicia o daemon `dotoold` em segundo plano se ele existir e não estiver em execução
- Volta para `xdotool` se `dotool` não estiver instalado (somente X11)
- Define o layout do teclado do seu modelo Vosk ativo (por exemplo, `de` → `XKB_DEFAULT_LAYOUT=de`)

Nenhum gerenciamento manual de daemon é necessário – o Aura cuida disso na inicialização.

---

## 5. Solução de problemas

**Aura transcreve mas nenhum texto aparece:**
__CODE_BLOCO_5__

**Caracteres ausentes ou distorcidos (especialmente tremas):**

Aumente o atraso de digitação em `config/settings_local.py`:
```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

**dotool funciona no terminal, mas não no Aura:**

Verifique se o grupo `input` está ativo na sessão da área de trabalho (não apenas em um novo terminal).
Um novo login completo é necessário após `gpasswd`.

**Force dotool no X11** (opcional, para melhor estabilidade do layout):
```bash
# Check if dotool is installed:
command -v dotool

# Check group membership:
groups | grep input

# Test manually (focus a text field first):
echo "type hello" | dotool

# Check the watcher log:
tail -30 log/type_watcher.log
```

---

## 6. Alternativa se o dotool não puder ser instalado

Se `dotool` não estiver disponível em seu sistema, o Aura volta para `xdotool` no X11.
No Wayland sem `dotool`, a digitação **não é suportada** — este é um Wayland
restrição de segurança, não uma limitação do Aura.

Ferramentas alternativas que podem funcionar em compositores específicos:

| Ferramenta | Funciona em |
|---|---|
| `xdotool` | Somente X11 |
| `dotool` | X11 + Wayland (recomendado) |
| `ydotool` | X11 + Wayland (alternativa) |

Para usar `ydotool` como solução alternativa manual:
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```
Nota: Aura não integra o `ydotool` nativamente — é necessária configuração manual.