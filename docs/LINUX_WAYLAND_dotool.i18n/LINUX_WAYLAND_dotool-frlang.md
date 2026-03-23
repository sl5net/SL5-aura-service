# Aura sous Wayland (Manjaro / Arch / CachyOS)

Damit Aura Text in andere Fenster schreiben kann, wird unter Wayland `dotool` utilisé.

### Quelles sont les prétentions :
1. **Démon :** `dotoold` doit être lancé à l'arrière-plan (Aura démarre automatiquement).
2. **Rechtigungen :** L'utilisateur doit entrer dans le groupe « input ».
3. **Uinput :** La date `/dev/uinput` doit être indiquée pour le groupe `input`.

### Manuelle Réparation :
Falls das Tippen nicht funktioniert, führe folgende Befehle aus:
__CODE_BLOCK_0__