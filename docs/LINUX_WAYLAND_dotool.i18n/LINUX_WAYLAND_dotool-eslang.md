# dotool en Wayland: configuración y solución de problemas

Se requiere `dotool` para que Aura escriba texto en otras aplicaciones en Wayland.
A diferencia de `xdotool`, se comunica directamente con el kernel de Linux a través de `uinput`
y funciona tanto en **X11 como en Wayland**.

En X11, `xdotool` se usa de forma predeterminada. `dotool` es opcional en X11 pero
recomendado para una mejor estabilidad del diseño (especialmente con diéresis).

---

## 1. Instalar dotool

**Arco/Manjaro/CachyOS (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu/Debian (si está disponible en repositorios):**
```bash
sudo apt install dotool
```

**Si no está en repositorios, compila desde la fuente:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. Permitir que dotool se ejecute sin root (obligatorio)

`dotool` necesita acceso a `/dev/uinput`. Sin esto, fracasará silenciosamente.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Es necesario volver a iniciar sesión** después del cambio de grupo para que entre en vigor.

---

## 3. Verificar la instalación

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

Si "grupos" no muestra "entrada", cierre sesión y vuelva a iniciarla (o reinicie).

---

## 4. Cómo utiliza Aura dotool

`type_watcher.sh` de Aura automáticamente:

- Detecta Wayland a través de `$WAYLAND_DISPLAY` y selecciona `dotool`
- Inicia el demonio `dotoold` en segundo plano si existe y no se está ejecutando.
- Vuelve a `xdotool` si `dotool` no está instalado (solo X11)
- Establece la distribución del teclado de su modelo Vosk activo (por ejemplo, `de` → `XKB_DEFAULT_LAYOUT=de`)

No se necesita administración manual de demonios: Aura maneja esto al inicio.

---

## 5. Solución de problemas

**El aura se transcribe pero no aparece ningún texto:**
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

**Caracteres faltantes o confusos (especialmente diéresis):**

Aumente el retraso de escritura en `config/settings_local.py`:
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool funciona en la terminal pero no en Aura:**

Verifique que el grupo `input` esté activo en la sesión de escritorio (no solo en una terminal nueva).
Es necesario volver a iniciar sesión por completo después de "gpasswd".

**Forzar dotool en X11** (opcional, para una mejor estabilidad del diseño):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. Alternativa si no se puede instalar dotool

Si `dotool` no está disponible en su sistema, Aura recurre a `xdotool` en X11.
En Wayland sin `dotool`, **no se admite escribir**; este es un Wayland
restricción de seguridad, no una limitación de Aura.

Herramientas alternativas que pueden funcionar en compositores específicos:

| Herramienta | Trabaja en |
|---|---|
| `xdotool` | Sólo X11 |
| `dotool` | X11 + Wayland (recomendado) |
| `ydotool` | X11 + Wayland (alternativa) |

Para utilizar `ydotool` como solución manual:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
Nota: Aura no integra `ydotool` de forma nativa; se requiere configuración manual.