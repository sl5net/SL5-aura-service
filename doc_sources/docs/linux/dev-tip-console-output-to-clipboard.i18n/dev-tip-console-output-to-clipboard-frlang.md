# Astuce de développement : copiez automatiquement la sortie de la console dans le presse-papiers

**Catégorie :** Productivité Linux / Shell  
**Plateforme :** Linux (zsh + Konsole/KDE)

---

## Le problème

Lorsque vous travaillez avec des assistants IA, vous devez souvent copier la sortie du terminal et la coller dans le chat. Cela signifie généralement :
1. Exécuter la commande
2. Sélectionnez la sortie avec la souris
3. Copier
4. Passer au navigateur
5. Coller

Cela fait trop d'étapes.

---

## La solution : capture automatique via `preexec` / `precmd`

Ajoutez ceci à votre `~/.zshrc` :

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

Puis rechargez :
```bash
source ~/.zshrc
```

### Résultat

Après chaque commande, le résultat est automatiquement dans votre presse-papiers, prêt à être collé dans votre chat AI avec **Ctrl+V**.

La sortie est également toujours enregistrée dans `~/t.txt` pour référence.

---

## Comment ça marche

| Partie | Ce qu'il fait |
|------|-------------|
| `preexec()` | S'exécute avant chaque commande, redirige la sortie vers `~/t.txt` |
| `precmd()` | S'exécute après chaque commande, restaure la sortie standard et copie dans le presse-papiers |
| `tee ~/t.txt` | Enregistre la sortie dans un fichier tout en l'affichant dans le terminal |
| `sed'...'` | Supprime les séquences d'échappement du titre de KDE Konsole (`]2;...` `]1;`) |
| `xclip` | Copie la sortie nettoyée dans le presse-papiers |

---

## Exigences

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ Ce qu'il ne faut PAS faire

Ne **pas** utiliser `fc -ln -1 | bash` pour réexécuter la dernière commande :

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

Cela réexécute chaque commande une fois terminée, ce qui peut provoquer des effets secondaires destructeurs — par exemple l'écrasement de fichiers, la réexécution de `git commit`, la réexécution de `sed -i`, etc.

L'approche `preexec`/`precmd` ci-dessus capture la sortie **pendant** l'exécution — sûre et fiable.