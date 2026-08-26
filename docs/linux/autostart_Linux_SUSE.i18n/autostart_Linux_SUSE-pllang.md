# openUŻYJ autostartu XDG

W openSUSE mechanizm autostartu XDG jest taki sam jak w Mint — `~/.config/autostart/` — więc nie jest tu potrzebna żadna osobna koncepcja, taka jak LaunchAgents w systemie macOS.

## środowisko graficzne

Różnica polega na środowisku graficznym: domyślnym/flagowym pulpitem openSUSE jest w rzeczywistości **KDE Plasma** (w przeciwieństwie do Minta), więc podejście oparte na „konsoli” z oryginalnej dokumentacji jest znacznie bardziej prawdopodobne, że będzie działać tak, jak jest. openSUSE oferuje również edycję GNOME, więc dam ci oba warianty oraz opcję bez terminala, która działa niezależnie od komputera.

**Najpierw potwierdź ścieżkę skryptu** (dostosuj `linus`, jeśli komputer SUSE używa innej nazwy użytkownika):

### znajdować

__KOD_BLOKU_0__

### Plazma KDE

**Opcja A — KDE Plasma** (domyślny pulpit openSUSE):

__KOD_BLOKU_1__

### Wersja openSUSE w środowisku GNOME

**Opcja B — openSUSE w wersji GNOME:** po prostu zamień linię `Exec`, ponieważ `konsole` zwykle nie jest instalowana w GNOME:

__KOD_BLOKU_2__

### brak widocznego terminala

**Opcja C — Zalecana: brak widocznego terminala, tło + dziennik** (działa identycznie na Plazmie, GNOME, Xfce, czymkolwiek — pozwala całkowicie uniknąć pytania „który terminal jest zainstalowany”, tak samo jak solidny wariant, który dałem ci dla Minta):

__KOD_BLOKU_3__

## Sprawdź dziennik

Sprawdź dziennik później za pomocą:

__KOD_BLOKU_4__

**Test bez wylogowywania się:** uruchom ręcznie część `bash -c '...'` najpierw w terminalu, aby potwierdzić, że faktycznie uruchamia usługę, a następnie wyloguj się/zaloguj, aby sprawdzić rzeczywisty wyzwalacz autostartu. Ustawienia systemowe openSUSE (Plasma: *Autostart*; GNOME: *Aplikacje startowe* za pomocą `gnome-tweaks`) również wyświetlą później ten wpis, jeśli chcesz go przełączyć z GUI.