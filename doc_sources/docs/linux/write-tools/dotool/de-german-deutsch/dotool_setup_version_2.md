### Teil 1: Deutsche Dokumentation

# dotool – Installation & Konfiguration (Manjaro / Arch-basiert)

## Was ist dotool?
`dotool` ist ein Werkzeug zur Simulation von Tastatureingaben. Im Gegensatz zu `xdotool` kommuniziert es direkt mit dem Kernel via `uinput` und funktioniert daher universell unter **X11 und Wayland**.

---

## Installation (Manjaro / Arch)

### 1. Paket installieren
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. Berechtigungen setzen
Damit `dotool` ohne Root-Rechte tippen darf, muss dein User in die Gruppe `input` und eine udev-Regel aktiv sein:

1. **User zur Gruppe:** `sudo gpasswd -a $USER input`
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

## Konfiguration im Projekt (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## Implementierung im Skript

### Persistenter Prozess (FIFO)
Um den Overhead durch ständiges Neuerstellen des virtuellen Keyboards zu vermeiden, nutzt das Skript eine Pipe (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### Die Eingabe-Funktion
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
- **Fehlende Zeichen:** Wenn Umlaute verschluckt werden, erhöhe `dotool_typedelay` auf 5 oder 10.
- **Fallback:** Ist `dotool` nicht korrekt konfiguriert, weicht das System automatisch auf `xdotool` aus.
- **Wayland-Support:** Unter Wayland wird `dotool` automatisch bevorzugt, da `xdotool` dort nicht funktioniert.

