# dotool – Installation & Konfiguration (Manjaro / Arch-basiert)

## Übersicht
„dotool“ ist ein Low-Level-Eingabesimulationsdienstprogramm. Im Gegensatz zu „xdotool“ interagiert es über „uinput“ direkt mit dem Linux-Kernel, wodurch es sowohl mit **X11 als auch mit Wayland** kompatibel ist.

---

## Installation (Manjaro / Arch)

### 1. Installieren Sie das Paket
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. Berechtigungen und udev-Regeln
Damit „dotool“ Eingaben ohne Root-Rechte simulieren kann, muss Ihr Benutzer Teil der „input“-Gruppe sein und eine udev-Regel muss aktiv sein:

1. **Benutzer zur Gruppe hinzufügen:** `sudo gpasswd -a $USER input`
2. **Udev-Regel erstellen:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Udev-Regeln neu laden:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Wichtig:** Sie müssen sich **abmelden und erneut anmelden**, damit die Gruppenänderungen wirksam werden.

---

## Projektkonfiguration (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## Skriptimplementierung

### Leistungsoptimierung (FIFO)
Das Starten einer neuen „dotool“-Instanz für jedes Wort ist langsam (~100 ms Latenz). Um eine „sofortige“ Eingabe zu erreichen, verwendet das Skript einen dauerhaften Hintergrundprozess, der aus einer FIFO-Pipe liest.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### Die Tippfunktion
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

## Fehlerbehebung und Hinweise
- **Fehlende Zeichen:** Wenn Sonderzeichen (wie Umlaute) übersprungen werden, erhöhen Sie „dotool_typedelay“ auf 5 oder 10.
- **Anwendungskompatibilität:** Einige Apps (Electron, Browser) erfordern möglicherweise eine höhere Verzögerung, um schnelle Eingaben korrekt zu registrieren.
- **Wayland-Unterstützung:** „dotool“ ist das erforderliche Backend für Wayland, da „xdotool“ es nicht unterstützt.
- **Automatischer Fallback:** Das Skript greift automatisch auf „xdotool“ zurück, wenn „dotool“ nicht richtig installiert oder konfiguriert ist.