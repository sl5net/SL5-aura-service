## Configuration de la méthode de saisie de texte

### Options pour `dotool` (également comme xdotool)

1. Installer : `pamac build dotool` ou `yay -S dotool`
2. L'utilisateur a ajouté le groupe d'entrée : `sudo gpasswd -a $USER input`
3. udev-Regel ersstellen :
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Nouvelle charge : `sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **Nouveau enregistrement**

### Configuration

Dans `config/settings.py` :
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### Notes

- `dotool` est un outil allemand comme `xdotool` – si votre outil peut être utilisé de la même manière, le processus de mise en œuvre du temps est disponible
- L'analyse des paramètres est effectuée avant l'impression au niveau de `settings.py` lors des importations – c'est le cas
- Le dotool-Listener fonctionne comme un processus d'arrière-plan via un FIFO (`/tmp/dotool_fifo`) avec `typedelay 0`

---