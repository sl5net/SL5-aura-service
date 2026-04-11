# dotool auf Wayland – Einrichtung und Fehlerbehebung

„dotool“ ist erforderlich, damit Aura Text in andere Anwendungen auf Wayland eingeben kann.
Im Gegensatz zu „xdotool“ kommuniziert es direkt über „uinput“ mit dem Linux-Kernel
und funktioniert sowohl auf **X11 als auch auf Wayland**.

Unter X11 wird standardmäßig „xdotool“ verwendet. „dotool“ ist unter X11 jedoch optional
Empfohlen für eine bessere Layoutstabilität (insbesondere bei Umlauten).

---

## 1. Dotool installieren

**Arch / Manjaro / CachyOS (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu / Debian (falls in Repos verfügbar):**
```bash
sudo apt install dotool
```

**Wenn nicht in Repos – aus dem Quellcode erstellen:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. Dotool ohne Root ausführen lassen (erforderlich)

„dotool“ benötigt Zugriff auf „/dev/uinput“. Ohne dies wird es stillschweigend scheitern.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Nach der Gruppenänderung ist eine erneute Anmeldung erforderlich**, damit sie wirksam wird.

---

## 3. Überprüfen Sie die Installation

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

Wenn „Gruppen“ nicht „Eingabe“ anzeigt, melden Sie sich ab und wieder an (oder starten Sie neu).

---

## 4. Wie Aura dotool verwendet

Auras „type_watcher.sh“ automatisch:

- Erkennt Wayland über „$WAYLAND_DISPLAY“ und wählt „dotool“ aus
– Startet den „dotoold“-Daemon im Hintergrund, falls er vorhanden ist und nicht ausgeführt wird
- Fällt auf „xdotool“ zurück, wenn „dotool“ nicht installiert ist (nur X11)
- Legt das Tastaturlayout Ihres aktiven Vosk-Modells fest (z. B. „de“ → „XKB_DEFAULT_LAYOUT=de“)

Es ist keine manuelle Daemon-Verwaltung erforderlich – Aura erledigt dies beim Start.

---

## 5. Fehlerbehebung

**Aura transkribiert, aber es erscheint kein Text:**
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

**Fehlende oder verstümmelte Zeichen (insbesondere Umlaute):**

Erhöhen Sie die Tippverzögerung in „config/settings_local.py“:
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool funktioniert im Terminal, aber nicht in Aura:**

Überprüfen Sie, ob die Gruppe „Eingabe“ in der Desktop-Sitzung aktiv ist (nicht nur ein neues Terminal).
Nach „gpasswd“ ist eine vollständige Neuanmeldung erforderlich.

**Dotool auf X11 erzwingen** (optional, für bessere Layoutstabilität):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. Fallback, wenn dotool nicht installiert werden kann

Wenn „dotool“ auf Ihrem System nicht verfügbar ist, greift Aura unter X11 auf „xdotool“ zurück.
Auf Wayland ohne „dotool“ wird die Eingabe **nicht unterstützt** – das ist ein Wayland
Sicherheitsbeschränkung, keine Aura-Einschränkung.

Alternative Tools, die möglicherweise mit bestimmten Compositoren funktionieren:

| Werkzeug | Funktioniert auf |
|---|---|
| `xdotool` | Nur X11 |
| `dotool` | X11 + Wayland (empfohlen) |
| `ydotool` | X11 + Wayland (alternativ) |

So verwenden Sie „ydotool“ als manuelle Problemumgehung:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
Hinweis: Aura integriert „ydotool“ nicht nativ – manuelle Konfiguration erforderlich.