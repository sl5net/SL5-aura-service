### Część 1: Niemiecka dokumentacja

# dotool – Instalacja i konfiguracja (Manjaro / Arch-basiert)

## Czy to był dotool?
„dotool” jest narzędziem Werkzeug zur Simulation von Tastatureingaben. Im Gegensatz zu `xdotool` kommuniziert es direct mit dem Kernel via `uinput` i funktioniert daher Universell do **X11 i Wayland**.

---

## Instalacja (Manjaro / Arch)

### 1. Zainstaluj pakiet
__KOD_BLOKU_0__

### 2. Zestaw Berechtigungen
Damit `dotool` ohne Root-Rechte tippen darf, muss dein Użytkownik w grupie `input` und eine udev-Regel aktiv sein:

1. **User zur Gruppe:** `sudo gpasswd -a wejście $USER`
2. **udev-Regel:**
__KOD_BLOKU_1__
3. **Regeln neu laden:**
__KOD_BLOKU_2__

**Wichtig:** Danach einmal **aus- und neu einloggen**, damit die Gruppenrechte aktiv werden.

---

## Konfiguracja w Projekcie (`config/settings.py`)

__KOD_BLOKU_3__

---

## Implementacja w skripcie

### Proces trwały (FIFO)
Um den Overhead durch ständiges Neuerstellen des resinllen Keyboards zu vermeiden, nutzt das Skript eine Pipe (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

__KOD_BLOKU_4__

### Funkcja Die Eingabe
__KOD_BLOKU_5__

---

## Pomoc i Fehlerbehebung
- **Fehlende Zeichen:** Wenn Umlaute verschluckt werden, erhöhe `dotool_typedelay` na 5 lub 10.
- **Fallback:** Ist `dotool` nicht korrekt konfiguriert, weicht das System automatisch auf `xdotool` aus.
- **Wsparcie Waylanda:** Dzięki Waylandowi wird `dotool` automatyczna bevorzugt, da `xdotool` dort nicht funktioniert.