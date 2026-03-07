## Konfiguracja metody wprowadzania tekstu

### Voraussetzungen für `dotool` (schneller als xdotool)

1. Zainstaluj: `pamac build dotool` lub `yay -S dotool`
2. Dodaj grupę danych użytkownika: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
__KOD_BLOKU_0__
4. Regeln neu laden: `sudo udevadm control --reload-rules && sudo udevadm wyzwalacz`
5. **Nowy wpis**

### Konfiguracja

W `config/settings.py`:
__KOD_BLOKU_1__

### Hinweise

- `dotool` ist deutlich schneller als `xdotool` – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- Das Auslesen der Settings unterdrückt bewusst alle Print-Ausgaben aus `settings.py` während des Imports – das ist gewollt
- Der dotool-Listener läuft als Hintergrundprozess über ein FIFO (`/tmp/dotool_fifo`) z `typedelay 0`

---