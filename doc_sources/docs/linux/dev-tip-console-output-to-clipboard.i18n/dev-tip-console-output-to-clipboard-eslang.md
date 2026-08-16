# Consejo de desarrollo: copie automáticamente la salida de la consola al portapapeles

**Categoría:** Linux / Shell Productividad  
**Plataforma:** Linux (zsh + Konsole/KDE)

---

## El problema

Cuando se trabaja con asistentes de IA, a menudo es necesario copiar la salida del terminal y pegarla en el chat. Esto generalmente significa:
1. Ejecutar comando
2. Seleccione la salida con el mouse
3. Copiar
4. Cambiar al navegador
5. Pegar

Son demasiados pasos.

---

## La solución: captura automática mediante `preexec`/`precmd`

Agregue esto a su `~/.zshrc`:

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

Luego recarga:
```bash
source ~/.zshrc
```

### Resultado

Después de cada comando, el resultado se guarda automáticamente en el portapapeles, listo para pegarlo en el chat de IA con **Ctrl+V**.

La salida también siempre se guarda en `~/t.txt` como referencia.

---

## Cómo funciona

| Parte | Qué hace |
|------|-------------|
| `preexec()` | Se ejecuta antes de cada comando, redirige la salida a `~/t.txt` |
| `precmd()` | Se ejecuta después de cada comando, restaura la salida estándar y copia al portapapeles |
| `tee ~/t.txt` | Guarda la salida en un archivo mientras la muestra en la terminal |
| `sed'...'` | Elimina las secuencias de escape de títulos de KDE Konsole (`]2;...` `]1;`) |
| `xclip` | Copia la salida limpia al portapapeles |

---

## Requisitos

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ Qué NO hacer

**No** use `fc -ln -1 | bash` para volver a ejecutar el último comando:

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

Esto vuelve a ejecutar cada comando una vez finalizado, lo que puede causar efectos secundarios destructivos, por ejemplo, sobrescribir archivos, volver a ejecutar `git commit`, volver a ejecutar `sed -i`, etc.

El enfoque `preexec`/`precmd` anterior captura la salida **durante** la ejecución, de forma segura y confiable.