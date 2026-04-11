# Integracja skorup ryb

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do konfiguracji Fish. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

Skorupa ryb przechowuje funkcje jako osobne pliki. Zalecanym podejściem jest utworzenie dedykowanego pliku funkcji.

1. Utwórz plik funkcyjny (katalog zostanie utworzony automatycznie, jeśli nie istnieje):
__KOD_BLOKU_0__

2. Wklej do pliku następujący blok:

__KOD_BLOKU_1__

3. Funkcja jest dostępna od razu we wszystkich nowych sesjach Fish. Aby załadować go w bieżącej sesji bez otwierania nowego terminala:
__KOD_BLOKU_2__

## Uwagi dotyczące ryb

- Fish używa „ustawionej wartości VAR” zamiast „VAR=wartość” do przypisania zmiennej.
- Warunki używają bloków `test` i `end` zamiast `[ ]` i `fi`.
- `$argv` zastępuje `$*` / `$@` przy przekazywaniu argumentów.
- `$status` zastępuje `$?` dla kodów wyjścia.
- `lub` / `i` zastępuje `||` / `&&` w wyrażeniach warunkowych.
- Fish **nie** używa słowa `local` — wszystkie zmienne wewnątrz funkcji są domyślnie lokalne.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.