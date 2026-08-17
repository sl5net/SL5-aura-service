### Parte 1: Documentación alemana

# dotool – Instalación y configuración (Manjaro / Arch-basiert)

## ¿Era dotool?
`dotool` es una herramienta para la simulación de tareas de tatuaje. Im Gegensatz zu `xdotool` se comunica directamente con el Kernel a través de `uinput` y funciona en todo el mundo bajo **X11 y Wayland**.

---

##Instalación (Manjaro/Arco)

### 1. Instalación del paquete
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. Setzen de Berechtigungen
Damit `dotool` sin Root-Rechte tippen darf, debe tener el usuario en el grupo `input` y un udev-Regel activo sein:

1. **Usuario del grupo:** `sudo gpasswd -a $entrada de USUARIO`
2. **udev-Regel:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Regeln neu laden:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Wichtig:** Danach einmal **aus- und neu einloggen**, damit die Gruppenrechte aktiv werden.

---

## Configuración en el proyecto (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## Implementación de Skript

### Proceso persistente (FIFO)
Um den Overhead durch ständiges Neuerstellen des virtual Keyboards zu vermeiden, nutzt das Skript a Pipe (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### La función Eingabe
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Sendet Befehle direkt an den wartenden Prozess
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

---

## Hinweise & Fehlerbehebung
- **Fehlende Zeichen:** Cuando Umlaute verschluckt werden, erhöhe `dotool_typedelay` en 5 o 10.
- **Retroceso:** `dotool` no está configurado correctamente, pero el sistema está automáticamente en `xdotool`.
- **Soporte de Wayland:** Cuando Wayland activa `dotool` automáticamente, `xdotool` no funciona.