# Integracja Ksh (Korn Shell).

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do pliku `~/.kshrc`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

1. Otwórz konfigurację Ksh w edytorze, który lubisz:
__KOD_BLOKU_0__

2. Wklej następujący blok na końcu pliku:

__KOD_BLOKU_1__

3. Upewnij się, że Ksh ładuje plik konfiguracyjny. Dodaj lub zweryfikuj to w `~/.profile`:
__KOD_BLOKU_2__

4. Załaduj ponownie swoją konfigurację:
__KOD_BLOKU_3__

## Uwagi specyficzne dla Ksh

- Ksh obsługuje zarówno składnię `nazwa funkcji { }`, jak i `nazwa () { }`; dla przejrzystości użyto tutaj słowa kluczowego „funkcja”.
- `local` nie jest** obsługiwane we wszystkich wariantach Ksh (np. `ksh88`). Zmienne w powyższej funkcji są zatem deklarowane bez słowa „local”. Jeśli używasz `mksh` lub `ksh93`, zamiast tego można użyć `typeset`: `typeset TEMP_FILE=$(mktemp)`.
- Zmienna `ENV` kontroluje, które pliki stanowią źródła Ksh dla sesji interaktywnych, podobnie jak `.bashrc`.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.