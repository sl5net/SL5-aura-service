# dotool – Instalacja i konfiguracja (Manjaro / Arch-basiert)

## Czy to był dotool?

`dotool` ist ein schnelles Werkzeug zum Simulieren von Tastatureingaben for Linux.
Jest to niemiecki schneller jako `xdotool` i funktioniert sowohl dla X11 również dla Waylanda.

---

## Instalacja (Manjaro / Arch)

### 1. Zainstaluj pakiet

__KOD_BLOKU_0__

### 2. Użytkownik zur `input`-Gruppe hinzufügen

__KOD_BLOKU_1__

### 3. udev-Regel erstellen

__KOD_BLOKU_2__

### 4. udev neu załadowany

__KOD_BLOKU_3__

### 5. Nowy loggen (wichtig!)

Ohne Neu-Login greift die Gruppenzugehörigkeit nicht.

---

## Konfiguracja w projekcie

### `config/settings.py`

__KOD_BLOKU_4__

---

## Zobacz skrypt do narzędzia Verwendet

### Funkcja Eingabe

__KOD_BLOKU_5__

### Konfiguracja auslesen (ohne Seiteneffekte)

Ustawienia zostały w ten sposób ausgelesen, dass `print()`-Ausgaben w `settings.py`
den Wert nicht verfälschen:

__KOD_BLOKU_6__

---

## Hinweise

- **Umlaute und Sonderzeichen:** `wpisz opóźnienie 2` (wykonaj domyślnie narzędzie) ist empfohlen.
Bei `typedelay 0` können Zeichen wie ä, ö, ü, ß verloren gehen.
- **Zu schnell für die Zielanwendung?** Manche Apps (np. B. Electron, dane wejściowe przeglądarki)
verlieren Zeichen bei niedrigem Opóźnienie. W diesem Fall `dotool_typedelay = 5` oder höher verwenden.
- **Wayland:** funkcja dotool auch dla Waylanda, xdotool nie jest dostępna.
- **Zastępczy:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.
---

## Zobacz skrypt do narzędzia Verwendet

Das Skript startet einen permanenten `dotool`-Prozess über ein FIFO,
um den Overhead eines neuen Prozesses bei jedem Tastendruck zu vermeiden.

### Odpowiedni kod (`type_watcher.sh`)

__KOD_BLOKU_7__

### Funkcja Eingabe

__KOD_BLOKU_8__

### Konfiguracja auslesen (ohne Seiteneffekte)

Ustawienia zostały w ten sposób ausgelesen, dass `print()`-Ausgaben w `settings.py`
den Wert nicht verfälschen:

__KOD_BLOKU_9__

---

## Hinweise

- **Zu schnell für die Zielanwendung?** Manche Apps (np. B. Electron, dane wejściowe przeglądarki)
verlieren Zeichen bei `typedelay 0`. W diesem Fall `typedelay 5` lub `typedelay 10` używaj.
- **Wayland:** funkcja dotool auch dla Waylanda, xdotool nie jest dostępna.
- **Zastępczy:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.