# Wskazówka dla deweloperów: automatycznie kopiuj dane wyjściowe konsoli do schowka

**Kategoria:** Produktywność w systemie Linux / ShellXSPACEbreakX
**Platforma:** Linux (zsh + Konsola/KDE)

---

## Problem

Podczas pracy z asystentami AI często trzeba kopiować dane wyjściowe terminala i wklejać je na czacie. Zwykle oznacza to:
1. Uruchom polecenie
2. Wybierz wyjście za pomocą myszy
3. Kopiuj
4. Przejdź do przeglądarki
5. Wklej

To za dużo kroków.

---

## Rozwiązanie: Automatyczne przechwytywanie za pomocą `preexec` / `precmd`

Dodaj to do swojego `~/.zshrc`:

__KOD_BLOKU_0__

Następnie załaduj ponownie:
__KOD_BLOKU_1__

### Wynik

Po każdym poleceniu dane wyjściowe są automatycznie umieszczane w schowku — gotowe do wklejenia na czacie AI za pomocą **Ctrl+V**.

Dane wyjściowe są zawsze zapisywane w formacie `~/t.txt` w celach informacyjnych.

---

## Jak to działa

| Część | Co to robi |
|------|------------|
| `preexec()` | Uruchamia się przed każdym poleceniem, przekierowuje dane wyjściowe do `~/t.txt` |
| `precmd()` | Uruchamia się po każdym poleceniu, przywraca standardowe wyjście i kopiuje do schowka |
| `tee ~/t.txt` | Zapisuje dane wyjściowe do pliku, jednocześnie wyświetlając je w terminalu |
| `sed '...'` | Usuwa sekwencje specjalne tytułu Konsoli KDE (`]2;...` `]1;`) |
| `xclip` | Kopiuje wyczyszczone dane wyjściowe do schowka |

---

## Wymagania

__KOD_BLOKU_2__

---

## ⚠️ Czego NIE robić

**Nie** używaj `fc -ln -1 | bash`, aby ponownie wykonać ostatnie polecenie:

__KOD_BLOKU_3__

Spowoduje to ponowne wykonanie każdego polecenia po jego zakończeniu, co może spowodować destrukcyjne skutki uboczne — na przykład nadpisanie plików, ponowne uruchomienie `git commit`, ponowne uruchomienie `sed -i` itp.

Powyższe podejście `preexec`/`precmd` przechwytuje dane wyjściowe **podczas** wykonywania — bezpiecznie i niezawodnie.