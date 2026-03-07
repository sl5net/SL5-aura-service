# dotool – Instalación y configuración (Manjaro / basado en Arch)

## Descripción general
`dotool` es una utilidad de simulación de entrada de bajo nivel. A diferencia de `xdotool`, interactúa directamente con el kernel de Linux a través de `uinput`, lo que lo hace compatible tanto con **X11 como con Wayland**.

---

##Instalación (Manjaro/Arco)

### 1. Instalar el paquete
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. Permisos y reglas de udev
Para permitir que `dotool` simule la entrada sin privilegios de root, su usuario debe ser parte del grupo `input` y una regla udev debe estar activa:

1. **Agregar usuario al grupo:** `sudo gpasswd -a $USER input`
2. **Crear regla udev:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Recargar reglas de udev:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Importante:** Debe **cerrar sesión y volver a iniciarla** para que los cambios del grupo surtan efecto.

---

## Configuración del proyecto (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## Implementación de secuencias de comandos

### Optimización del rendimiento (FIFO)
Iniciar una nueva instancia de `dotool` para cada palabra es lento (latencia de ~100 ms). Para lograr una escritura "instantánea", el script utiliza un proceso en segundo plano persistente que lee desde una tubería FIFO.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### La función de escritura
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Pipe commands directly into the running background process
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

---

## Solución de problemas y notas
- **Caracteres faltantes:** Si se omiten caracteres especiales (como diéresis), aumente `dotool_typedelay` a 5 o 10.
- **Compatibilidad de aplicaciones:** Algunas aplicaciones (Electron, navegadores) pueden requerir un retraso mayor para registrar correctamente la entrada rápida.
- **Soporte de Wayland:** `dotool` es el backend requerido para Wayland, ya que `xdotool` no lo admite.
- **Retroceso automático:** El script vuelve automáticamente a `xdotool` si `dotool` no está instalado o configurado correctamente.