# dotool na Wayland — konfiguracja i rozwiązywanie problemów

`dotool` jest wymagane, aby Aura mogła wpisywać tekst w innych aplikacjach na Wayland.
W przeciwieństwie do `xdotool`, komunikuje się bezpośrednio z jądrem Linuksa poprzez `uinput`
i działa zarówno na **X11, jak i Waylandzie**.

Na X11 domyślnie używane jest `xdotool`. `dotool` jest opcjonalne na X11, ale
zalecane dla lepszej stabilności układu (szczególnie w przypadku przegłosów).

---

## 1. Zainstaluj dotool

**Arch / Manjaro / CachyOS (AUR):**
__KOD_BLOKU_0__

**Ubuntu / Debian (jeśli jest dostępny w repozytoriach):**
__KOD_BLOKU_1__

**Jeśli nie w repozytoriach — kompilacja ze źródła:**
__KOD_BLOKU_2__

---

## 2. Zezwól na działanie dotool bez rootowania (wymagane)

`dotool` potrzebuje dostępu do `/dev/uinput`. Bez tego zakończy się to po cichu niepowodzeniem.

__KOD_BLOKU_3__

**Wymagane jest ponowne zalogowanie** po zmianie grupy, aby zmiana zaczęła obowiązywać.

---

## 3. Sprawdź instalację

__KOD_BLOKU_4__

Jeżeli `groups` nie wyświetla `wejściowego`, wyloguj się i zaloguj ponownie (lub uruchom ponownie).

---

## 4. Jak Aura używa dotool

`type_watcher.sh` Aury automatycznie:

- Wykrywa Waylanda poprzez `$WAYLAND_DISPLAY` i wybiera `dotool`
- Uruchamia demona `dotoold` w tle, jeśli istnieje i nie jest uruchomiony
- Wraca do `xdotool`, jeśli `dotool` nie jest zainstalowane (tylko X11)
- Ustawia układ klawiatury z aktywnego modelu Vosk (np. `de` → `XKB_DEFAULT_LAYOUT=de`)

Nie jest potrzebne ręczne zarządzanie demonami — Aura zajmuje się tym podczas uruchamiania.

---

## 5. Rozwiązywanie problemów

**Aura dokonuje transkrypcji, ale nie pojawia się żaden tekst:**
__KOD_BLOKU_5__

**Brakujące lub zniekształcone znaki (zwłaszcza przegłosy):**

Zwiększ opóźnienie wpisywania w `config/settings_local.py`:
__KOD_BLOKU_6__

**dotool działa w terminalu, ale nie w Aurze:**

Sprawdź, czy grupa „input” jest aktywna w sesji pulpitu (a nie tylko w nowym terminalu).
Po `gpasswd` wymagane jest pełne ponowne zalogowanie.

**Wymuś dotool na X11** (opcjonalnie, dla lepszej stabilności układu):
__KOD_BLOKU_7__

---

## 6. Rozwiązanie awaryjne, jeśli nie można zainstalować dotool

Jeśli `dotool` jest niedostępne w twoim systemie, Aura powróci do `xdotool` na X11.
Na Waylandzie bez `dotool` pisanie nie jest obsługiwane** — to jest Wayland
ograniczenie bezpieczeństwa, a nie ograniczenie Aury.

Alternatywne narzędzia, które mogą działać na określonych kompozytorach:

| Narzędzie | Działa na |
|---|---|
| `xdotool` | Tylko X11 |
| `do narzędzia` | X11 + Wayland (zalecane) |
| `ydotool` | X11 + Wayland (alternatywa) |

Aby użyć `ydotool` jako ręcznego rozwiązania:
__KOD_BLOKU_8__
Uwaga: Aura nie integruje natywnie `ydotool` — wymagana jest ręczna konfiguracja.