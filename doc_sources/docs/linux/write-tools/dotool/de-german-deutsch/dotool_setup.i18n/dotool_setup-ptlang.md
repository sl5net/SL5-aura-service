# dotool – Instalação e configuração (Manjaro / Arch-basiert)

## Foi dotool?

`dotool` é uma ferramenta útil para simulação de configuração no Linux.
É um schneller alemão como `xdotool` e funciona tão bem no X11 como também no Wayland.

---

## Instalação (Manjaro/Arco)

### 1. Instalação do pacote

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. Usuário do grupo `input`

```bash
sudo gpasswd -a $USER input
```

### 3. udev-Regel erstellen

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

### 4. udev neu carregado

__CODE_BLOCO_3__

### 5. Neu einloggen (wichtig!)

Ohne Neu-Login não aceita o Gruppenzugehörigkeit.

---

## Configuração do projeto

### `config/settings.py`

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

---

## Como usar o Skript na ferramenta

### Função Eingabe

__CODE_BLOCO_5__

### Auslesen de configuração (ohne Seitenefekte)

As configurações foram então aumentadas, como `print()`-ausgaben em `settings.py`
den Wert nicht verfälschen:

```python
# Eingabemethode für X11: "dotool" (schnell) oder "xdotool" (Fallback)
x11_input_method_OVERRIDE = "dotool"

# Delay zwischen Tastenanschlägen in Millisekunden
# 2ms = dotool-Default, zuverlässig auch für Umlaute (ä, ö, ü, ß)
# 0ms = maximal schnell, kann Sonderzeichen verschlucken
dotool_typedelay = 2
```

---

##Hinweise

- **Umlaute und Sonderzeichen:** `type delay 2` (do tool-Default) é empfohlen.
Bei `typedelay 0` pode ser definido como ä, ö, ü, ß verloren gehen.
- **Zu schnell für die Zielanwendung?** Manche Apps (z. B. Electron, entradas de navegador)
verlieren Zeichen bei niedrigem Delay. Nesse caso, `dotool_typedelay = 5` ou mais alto.
- **Wayland:** dotool também funciona no Wayland, xdotool não funciona.
- **Fallback:** Se a ferramenta não for instalada, o Skript será executado automaticamente no `xdotool`.
---

## Como usar o Skript na ferramenta

O Skript startet einen persistenten `dotool`-Prozess über ein FIFO,
um den Overhead eines neuen Prozesses bei jedem Tastendruck zu vermeiden.

### Código relevante (`type_watcher.sh`)

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" | dotool
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

### Função Eingabe

```bash
OVERRIDE=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.x11_input_method_OVERRIDE)
")
[[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"

DOTOOL_TYPEDELAY=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.dotool_typedelay)
")
```

### Auslesen de configuração (ohne Seitenefekte)

As configurações foram então aumentadas, como `print()`-ausgaben em `settings.py`
den Wert nicht verfälschen:

__CODE_BLOCO_9__

---

##Hinweise

- **Zu schnell für die Zielanwendung?** Manche Apps (z. B. Electron, entradas de navegador)
verifique o valor em `typedelay 0`. Neste outono, `typedelay 5` ou `typedelay 10` são usados.
- **Wayland:** dotool também funciona no Wayland, xdotool não funciona.
- **Fallback:** Se a ferramenta não for instalada, o Skript será executado automaticamente no `xdotool`.