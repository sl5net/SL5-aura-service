Oprócz wielu opcji wyszukiwania, prawdopodobnie w Twoim środowisku programistycznym istnieje wyszukiwanie pełnotekstowe. Możesz także użyć:

scripts/search_rules/search_rules.sh

Umożliwia to wyszukiwanie w istniejących mapach lub w kodzie źródłowym lub dokumentacji. a następnie możesz otworzyć pokój, który znalazłeś w swoim ulubionym edytorze lub otworzyć go na githubie lub... skonfiguruj skrypt tak, jak potrzebujesz.

MAPS_DIR można konfigurować za pomocą arg pozycyjnego lub zmiennej środowiskowej

skrypt zachowuje zakodowane na stałe ustawienia domyślne, ale umożliwia zastąpienie:

- Priorytet: 1) pierwszy parametr pozycyjny ($1), 2) istniejący MAPS_DIR env var,
3) zakodowana na stałe wartość domyślna „$SL5NET_AURA_PROJECT_ROOT/config/maps”.
— Poprawia elastyczność CI, lokalnych zastąpień i testowania bez edytowania skryptu.
- Dodaje cytowanie i sprawdzanie istnienia katalogu, aby zapobiec wcześniejszemu niepowodzeniu, jeśli ścieżka jest nieprawidłowa.

Przykładowe użycie:
- ./search_rules.sh używa wartości domyślnej
- ./search_rules.sh ./docs używa podanej ścieżki
- MAPS_DIR=/env/maps ./search_rules.sh

Zachowuje to kompatybilność wsteczną, jednocześnie określając konfigurację.

Istnieje również wersja na komputer z systemem Windows (w tym folderze), która potrafi nieco mniej: search_rules.ps1


(s, 28.3.'26 23:07 sob)