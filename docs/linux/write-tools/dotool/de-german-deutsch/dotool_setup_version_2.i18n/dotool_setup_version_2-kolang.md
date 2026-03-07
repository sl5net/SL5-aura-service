### 1부: Deutsche Dokumentation

# dotool – 설치 및 구성 (Manjaro / Arch-basiert)

## is dotool이었나?
`dotool`은 Werkzeug zur Simulation von Tastatureingaben에 해당합니다. Im Gegensatz zu `xdotool`은 **X11 및 Wayland**에서 `uinput` 및 기능 제공을 통해 커널에 직접 통신할 수 있습니다.

---

## 설치 (만자로/아치)

### 1. 패키지 설치
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. 베레크티군겐 세트젠
Damit `dotool` ohne Root-Rechtetippen darf, muss dein User in die Gruppe`input` und eine udev-Regel aktiv sein:

1. **사용자 zur 그룹:** `sudo gpasswd -a $USER 입력`
2. **udev-Regel:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Regeln neu laden:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**위치:** Danach einmal **aus- und neu einloggen**, damit die Gruppenrechte aktiv werden.

---

## 프로젝트 구성(`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## Skript 구현

### 지속성 프로세스(FIFO)
Um den Overhead durch ständiges Neuerstellen des Virmeiden, nutzt das Skript eine Pipe (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

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

## 힌바이제 & 펠레르베헤붕
- **Fehlende Zeichen:** Wenn Umlaute verschluckt werden, erhöhe `dotool_typedelay` auf 5 oder 10.
- **폴백:** Ist `dotool` nicht korrekt konfiguriert, weicht das System automatisch auf `xdotool` aus.
- **Wayland 지원:** Unter Wayland wird `dotool` automatisch bevorzugt, da `xdotool` dort nicht funktioniert.