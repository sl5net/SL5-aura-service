# Aura sob Wayland (Manjaro/Arch/CachyOS)

Damit Aura Text in other Fenster schreiben kann, wird unter Wayland `dotool` usado.

### Wichtige Voraussetzungen:
1. **Daemon:** `dotoold` deve estar no Hintergrund laufen (Aura startet diesen automatisch).
2. **Berechtigungen:** Seu usuário deve entrar no grupo `input` sein.
3. **Uinput:** A data `/dev/uinput` deve ser definida para o grupo `input`.

### Manuelle Reparatura:
Falls das Tippen não funciona, mas siga as instruções abaixo:
__CODE_BLOCK_0__