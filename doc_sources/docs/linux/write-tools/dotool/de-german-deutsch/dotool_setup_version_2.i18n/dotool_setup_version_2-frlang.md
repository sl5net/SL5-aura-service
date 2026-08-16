### Partie 1 : Deutsche Dokumentation

# dotool – Installation et configuration (Manjaro / Arch-basiert)

## C'était dotool ?
`dotool` est un outil de simulation de dégustation. Je suis connecté à `xdotool` directement avec le noyau via `uinput` et des fonctions universelles sous **X11 et Wayland**.

---

## Installation (Manjaro / Arch)

### 1. Paquet installé
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. Mises en garde
Damit `dotool` sans Root-Rechte tippen darf, doit être un utilisateur dans le groupe `input` et une activité udev-reglement sein :

1. **Utilisateur du groupe :** `sudo gpasswd -a $USER input`
2. **udev-Regel :**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Regeln neu laden:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Wichtig :** Danach einmal **aus- und neu einloggen**, damit die Gruppenrechte aktiv werden.

---

## Configuration dans le projet (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## Implémentation dans le script

### Processus persistant (FIFO)
Un Overhead par les nouveaux claviers virtuels standard, sans le script d'un tuyau (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### La fonction Eingabe
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
- **Fehlende Zeichen :** Lors d'une introduction, j'ai trouvé `dotool_typedelay` du 5 au 10.
- **Retour :** `dotool` n'est pas correctement configuré, mais le système est automatiquement activé par `xdotool`.
- **Wayland-Support :** Sous Wayland, « dotool » est automatiquement activé, et « xdotool » n'est plus fonctionnel.