# dotool – Installation et configuration (Manjaro / Arch-basiert)

## C'était dotool ?

`dotool` est une méthode de travail pour une simulation de dégustation sous Linux.
Il s'agit d'un outil vraiment efficace comme "xdotool" et fonctionnel sous X11 comme Wayland.

---

## Installation (Manjaro / Arch)

### 1. Paquet installé

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. User zur `input`-Gruppe Hinzufügen

```bash
sudo gpasswd -a $USER input
```

### 3. udev-Regel ersstellen

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

### 4. udev nouveau chargé

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 5. Nouveaux journaux (wichtig !)

Sans Neu-Login, le Gruppenzugehörigkeit nicht.

---

## Configuration dans le projet

### `config/settings.py`

```python
# Eingabemethode für X11: "dotool" (schnell) oder "xdotool" (Fallback)
x11_input_method_OVERRIDE = "dotool"

# Delay zwischen Tastenanschlägen in Millisekunden
# 2ms = dotool-Default, zuverlässig auch für Umlaute (ä, ö, ü, ß)
# 0ms = maximal schnell, kann Sonderzeichen verschlucken
dotool_typedelay = 2
```

---

## Comment utiliser le script dotool

### Fonction Eingabe

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

### Configuration simple (sans effet de site)

Les paramètres sont définis de manière à ce que `print()` soit ajouté dans `settings.py`
den Wert nicht verfälschen:

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

---

## Notes

- **Récapitulatif et réponse :** `type delay 2` (do tool-Default) est utilisé.
Bei `typedelay 0` können Zeichen wie ä, ö, ü, ß verloren gehen.
- **Zu schnell für die Zielanwendung?** Manche Apps (par exemple Electron, Browser-Inputs)
verlieren Zeichen bei niedrigem Delay. Dans ce cas, `dotool_typedelay = 5` ou plus à utiliser.
- **Wayland :** dotool fonctionne également sous Wayland, xdotool n'est pas articulé.
- **Retour :** Si dotool n'est pas installé, le script tombe automatiquement sur `xdotool`.
---

## Comment utiliser le script dotool

Le script démarre un processus `dotool` persistant via un FIFO,
um den Overhead eines neuen Prozesses bei jedem Tastendruck zu vermeiden.

### Code pertinent (`type_watcher.sh`)

```bash
export DOTOOL_DELAY=0

# Alten Listener beenden falls noch läuft
pkill -f "dotool < /tmp/dotool_fifo" 2>/dev/null

DOTOOL_PID=$!

# typedelay direkt nach Start setzen
sleep 0.1
echo "typedelay 0" > /tmp/dotool_fifo

# Cleanup beim Beenden
trap "kill $DOTOOL_PID 2>/dev/null; rm -f /tmp/dotool_fifo" EXIT
```

### Fonction Eingabe

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay 0\ntype %s\n' "$text" | dotool
        # printf 'typedelay 0\ntype %s\n' "$text" > /tmp/dotool_fifo
        # printf 'type %s\n' "$text" | dotool

    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

### Configuration simple (sans effet de site)

Les paramètres sont définis de manière à ce que `print()` soit ajouté dans `settings.py`
den Wert nicht verfälschen:

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
```

---

## Notes

- **Zu schnell für die Zielanwendung?** Manche Apps (par exemple Electron, Browser-Inputs)
verlieren Zeichen bei `typedelay 0`. Dans ce Fall `typedelay 5` ou `typedelay 10` sont utilisés.
- **Wayland :** dotool fonctionne également sous Wayland, xdotool n'est pas articulé.
- **Retour :** Si dotool n'est pas installé, le script tombe automatiquement sur `xdotool`.