# dotool – Installation et configuration (Manjaro / Arch-based)

## Aperçu
`dotool` est un utilitaire de simulation d'entrée de bas niveau. Contrairement à `xdotool`, il interagit directement avec le noyau Linux via `uinput`, ce qui le rend compatible à la fois avec **X11 et Wayland**.

---

## Installation (Manjaro / Arch)

### 1. Installez le package
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. Autorisations et règles udev
Pour permettre à `dotool` de simuler une entrée sans privilèges root, votre utilisateur doit faire partie du groupe `input` et une règle udev doit être active :

1. **Ajouter un utilisateur au groupe :** `sudo gpasswd -a $USER input`
2. **Créer une règle udev :**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Recharger les règles udev :**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Important :** Vous devez **vous déconnecter et vous reconnecter** pour que les modifications du groupe prennent effet.

---

## Configuration du projet (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## Implémentation du script

### Optimisation des performances (FIFO)
Le démarrage d'une nouvelle instance « dotool » pour chaque mot est lent (latence d'environ 100 ms). Pour obtenir une saisie « instantanée », le script utilise un processus d'arrière-plan persistant lisant à partir d'un canal FIFO.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### La fonction de saisie
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

## Dépannage et remarques
- **Caractères manquants :** Si des caractères spéciaux (comme les trémas) sont ignorés, augmentez `dotool_typedelay` à 5 ou 10.
- **Compatibilité des applications :** Certaines applications (Electron, navigateurs) peuvent nécessiter un délai plus élevé pour enregistrer correctement la saisie rapide.
- **Support Wayland :** `dotool` est le backend requis pour Wayland, car `xdotool` ne le prend pas en charge.
- **Repli automatique :** Le script revient automatiquement à `xdotool` si `dotool` n'est pas installé ou configuré correctement.