# dotool sur Wayland — Configuration et dépannage

`dotool` est requis pour qu'Aura puisse saisir du texte dans d'autres applications sur Wayland.
Contrairement à `xdotool`, il communique directement avec le noyau Linux via `uinput`
et fonctionne à la fois sur **X11 et Wayland**.

Sur X11, `xdotool` est utilisé par défaut. `dotool` est facultatif sur X11 mais
recommandé pour une meilleure stabilité de la mise en page (en particulier avec les Umlauts).

---

## 1. Installer dotool

**Arch/Manjaro/CachyOS (AUR) :**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu / Debian (si disponible dans les dépôts) :**
```bash
sudo apt install dotool
```

**Si ce n'est pas dans les dépôts, construisez à partir des sources :**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. Autoriser dotool à s'exécuter sans root (obligatoire)

`dotool` doit accéder à `/dev/uinput`. Sans cela, il échouera silencieusement.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Reconnexion requise** après le changement de groupe pour que celui-ci prenne effet.

---

## 3. Vérifiez l'installation

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

Si « groupes » n'affiche pas « entrée », déconnectez-vous et reconnectez-vous (ou redémarrez).

---

## 4. Comment Aura utilise dotool

Le `type_watcher.sh` d'Aura automatiquement :

- Détecte Wayland via `$WAYLAND_DISPLAY` et sélectionne `dotool`
- Démarre le démon `dotoold` en arrière-plan s'il existe et n'est pas en cours d'exécution
- Revient à `xdotool` si `dotool` n'est pas installé (X11 uniquement)
- Définit la disposition du clavier à partir de votre modèle Vosk actif (par exemple `de` → `XKB_DEFAULT_LAYOUT=de`)

Aucune gestion manuelle des démons n'est nécessaire : Aura s'en charge au démarrage.

---

## 5. Dépannage

**Aura transcrit mais aucun texte n'apparaît :**
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

**Caractères manquants ou tronqués (en particulier les trémas) :**

Augmentez le délai de saisie dans `config/settings_local.py` :
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool fonctionne dans le terminal mais pas dans Aura :**

Vérifiez que le groupe `input` est actif dans la session de bureau (pas seulement dans un nouveau terminal).
Une reconnexion complète est requise après `gpasswd`.

**Forcer dotool sur X11** (facultatif, pour une meilleure stabilité de la mise en page) :
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. Solution de secours si dotool ne peut pas être installé

Si « dotool » n'est pas disponible sur votre système, Aura revient à « xdotool » sur X11.
Sur Wayland sans « dotool », la saisie n'est **pas prise en charge** — c'est un Wayland
restriction de sécurité, pas une limitation d'Aura.

Outils alternatifs pouvant fonctionner sur des compositeurs spécifiques :

| Outil | Fonctionne sur |
|---|---|
| `xdotool` | X11 uniquement |
| `dotool` | X11 + Wayland (recommandé) |
| `ydotool` | X11 + Wayland (alternative) |

Pour utiliser « ydotool » comme solution de contournement manuelle :
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
Remarque : Aura n'intègre pas `ydotool` de manière native — configuration manuelle requise.