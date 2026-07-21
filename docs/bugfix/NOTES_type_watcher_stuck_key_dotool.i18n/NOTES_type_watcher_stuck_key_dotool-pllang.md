# Uwagi: problem z zablokowanym klawiszem type_watcher.sh (dotool)

## Objaw
Krótko po ponownym uruchomieniu Manjaro, na pierwszym dyktandzie po `sl5net Aura`
uruchamiał się automatycznie, pojedynczy znak utknął i powtarzał się w nieskończoność
(np. „n” powtórzone setki razy), aż do naciśnięcia klawisza spustowego
ponownie jako ręczne obejście.

Zaobserwowano raz w dniu 21.07.2026 ~09:44 (wtorek), tekst: „Die Ideen niemand wird
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn…”.

## Oś czasu (sprawdzona w logach)
- 09:29:17 - Uruchomiono `type_watcher.sh` (log/type_watcher.log)
- 09:41:56 - otrzymano dyktando „ideen niemand wird mehr gefragt…”
(log/aura_engine.log, wątek-13/14)
- 09:42:03 - zakończenie przetwarzania tekstu (`najlepszy wynik rozmyty: 0%`),
prawdopodobnie zapisane w pliku `tts_output_*.txt`
- ~09:42:04-09:42:09 - `type_watcher.sh` uległ awarii (wywnioskowano: watchdog
interwał odpytywania wynosi 5 sekund, patrz poniżej)
- 09:42:09 - log watchdoga (log/type_watcher_keep_alive.log):
„WATCHDOG: „type_watcher.sh” nie jest uruchomiony. Zaczynam go teraz.”
- 09:42:13 - zrestartowano `type_watcher.sh` (log/type_watcher.log)
- Brak wpisu `wpisanej zawartości...` dla pliku "ideen niemand..."
kiedykolwiek znaleziony w log/type_watcher.log — wpisanie tego konkretnego
tekst nigdy nie został ukończony/zarejestrowany.

## Stan przyczyny głównej
- POTWIERDZONO: `type_watcher.sh` uległ awarii podczas kończenia tekstu
przetwarzanie (09:42:03) i watchdog wykrywający, że nie działa
(09:42:09). Watchdog (`type_watcher_keep_alive.sh`) tylko zabija
i uruchamia się ponownie po zmianie znacznika czasu w pliku konfiguracyjnym (`ts1`/`ts2`,
potwierdzone bez zmian w tym incydencie) lub uruchamia się automatycznie ponownie, gdy
`pgrep -f "type_watcher.sh"` nie znajduje żadnego procesu — tj. było to bardzo
prawdopodobnie samookaleczenie, a nie zabójstwo zewnętrzne.
- HIPOTEZA (niesprawdzona): `set -euo pipefail` (type_watcher.sh linia 5)
spowodował zakończenie skryptu z użyciem niezerowego kodu zakończenia znajdującego się w pliku
potok, prawdopodobnie podczas gdy potok `dotool` `do_type()` (linia 125) był
środkowy strumień. Jeśli proces bash zakończy się podczas przesyłania strumieniowego do `dotool`,
oddzielny demon `dotoold` (który działa niezależnie)
można pozostawić klucz w stanie „w dół” bez dopasowania „w górę”.
odebrany, powodując powtórzenie klucza na poziomie systemu operacyjnego.
- JESZCZE NIE POTWIERDZONO: dokładne polecenie/wiersz, które spowodowało wartość różną od zera
wyjdź pod `set -euo pipefail`. Brak stderr z powodu awarii
Przechwycono proces `type_watcher.sh` (watchdog nazywa go
bez przekierowania wyjścia, `type_watcher_keep_alive.sh` linia 79).
- Kluczem, którego dotyczył problem, NIE zawsze był ten sam znak w różnych
wystąpienia tego błędu (zgłoszenie użytkownika: poprzednio również „t”).

## Już zbadano i wykluczono
— Nie jest to restart wywołany zmianą konfiguracji (potwierdzony przez użytkownika: config
niezmienione, a sprawdzenie `ts1_old != ts1_new` spowoduje zarejestrowanie „Zmieniona konfiguracja”).
- Nie jest to duplikat autostartu `type_watcher.sh` nakładającego się na
sam (tylko jeden wpis „Witajcie od Obserwatora” poprzedzał awarię).
- Wywołanie typu dotool w `do_type()` jest niepodzielne w każdym wywołaniu i tak jest
sam nie wysyła klucza znaków w dół/w górę — wykluczając `type_watcher.sh`
logika aplikacji jako bezpośrednie źródło zablokowanego klawisza w normalnych warunkach
(bez awarii).

## Poprawka już zastosowana (awaryjna/łagodząca, a nie naprawiająca przyczynę główną)
Zarówno `cleanup()` w `type_watcher.sh` jak i `do_cleanup()` w
`keep-keys-up.sh` wcześniej wydano tylko klawisze modyfikujące (shift, ctrl,
alt itp.) poprzez `dotool`/`xdotool`. To nie pomogło utkniętemu regularnie
klucz (litera, cyfra, znak interpunkcyjny).

- `type_watcher.sh`: `cleanup()` wysyła teraz `dotool klucz <nazwa>:up` dla
wszystkie litery, cyfry i popularne klawisze interpunkcyjne/białe znaki, nie
tylko modyfikatory.
- `type_watcher.sh`: `INPUT_METHOD` jest teraz eksportowany po wykryciu, więc
inne skrypty mogą zobaczyć, który backend („dotool” / „xdotool”) jest aktywny.
- `keep-keys-up.sh`: `do_cleanup()` zyskało gałąź `dotool` (używając
Czasownik „keyup”, brak opóźnienia dla każdego klawisza, ze względu na wydajność) aktywny tylko wtedy, gdy
`INPUT_METHOD=dotool`, odzwierciedlające istniejące wywołanie `xdotool keyup`
dla modyfikatorów.

Nie naprawia to podstawowej awarii `type_watcher.sh`; to tylko
gwarantuje, że jeśli awaria powtórzy się, zacięty klawisz zostanie zwolniony
następny przebieg czyszczenia („--cleanup”, wywoływany po każdym „do_type()” i
poprzez procedurę obsługi `czyszczenie pułapek EXIT INT TERM`) zamiast powtarzania
na czas nieokreślony, aż do ręcznego naciśnięcia klawisza wyzwalającego.

## Dalsze kroki, jeśli sytuacja się powtórzy
- Przechwyć stderr `type_watcher.sh` w przypadku awarii. Obecnie
Linia 79 `type_watcher_keep_alive.sh` wywołuje to bez przekierowania, więc
każdy komunikat o błędzie bash zostanie utracony (przechodzi do własnego pliku watchdog
stdout/stderr, gdziekolwiek jest to wskazane przez mechanizm autostartu).
- Rozważ tryb debugowania, np. `bash -x scripts/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`, przełączany za pomocą zmiennej env, takiej jak
`TYPE_WATCHER_DEBUG=1`, aby przechwycić dokładnie wadliwą linię w następnej
rozbić się.
- Sprawdź, co uruchamia `type_watcher_keep_alive.sh` podczas uruchamiania Manjaro
(plik autostart `.desktop`, jednostka systemowa `--user` itp.) i czy
jego stdout/stderr są przechwytywane w dowolnym miejscu.
- Jeśli jest to powtarzalne, sprawdź, czy awaria ma związek z
`dotoold` nadal się inicjuje zaraz po uruchomieniu (patrz instrukcja `sleep 0.1`
w type_watcher.sh linia 8 i pętla startowa `dotoold` w liniach
102-110).