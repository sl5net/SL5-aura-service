# Prezentacja funkcji: Integracja z interfejsem wiersza poleceń (CLI).

**Dedykowane mojemu bardzo ważnemu przyjacielowi, Lub.**

Nowy interfejs wiersza poleceń (CLI) oparty na FastAPI zapewnia czysty, synchroniczny sposób interakcji z naszą działającą podstawową usługą przetwarzania tekstu z dowolnej powłoki lokalnej lub zdalnej. Jest to solidne rozwiązanie zaprojektowane w celu integracji podstawowej logiki ze środowiskami powłoki.

---

## 1. Architektura i koncepcja synchronicznego CLI

Usługa jest obsługiwana przez serwer **Uvicorn/FastAPI** i wykorzystuje niestandardowy punkt końcowy („/process_cli”) w celu dostarczania synchronicznych (blokujących) wyników z z natury asynchronicznego procesu w tle opartego na plikach.

### Strategia odpytywania „poczekaj i przeczytaj”.

1. **Unikalne zastąpienie danych wyjściowych:** Interfejs API tworzy unikalny katalog tymczasowy dla każdego żądania.
2. **Rozpoczęcie procesu:** Wywołuje `process_text_in_background`, aby uruchomić podstawową logikę w nieblokującym wątku, zapisując wynik do pliku `tts_output_*.txt` w tym unikalnym folderze.
3. **Oczekiwanie synchroniczne:** Funkcja API następnie **blokuje** i odpytuje unikalny folder do czasu utworzenia pliku wyjściowego lub przekroczenia limitu czasu.
4. **Dostarczanie wyników:** API odczytuje zawartość pliku, przeprowadza niezbędne czyszczenie (usuwa plik i katalog tymczasowy) i zwraca ostatecznie przetworzony tekst w polu `result_text` odpowiedzi JSON.

Dzięki temu klient CLI otrzyma odpowiedź dopiero *po* zakończeniu przetwarzania tekstu, co gwarantuje niezawodne działanie powłoki.

## 2. Dostęp zdalny i mapowanie portów sieciowych

Aby umożliwić dostęp ze zdalnych klientów, takich jak terminal Lub, wymagana była następująca konfiguracja sieci, uwzględniająca powszechne ograniczenie ograniczonej dostępności portów zewnętrznych:

### Rozwiązanie: mapowanie portów zewnętrznych

Ponieważ usługa działa wewnętrznie na **Port 8000**, a nasze środowisko sieciowe ogranicza dostęp zewnętrzny do określonego zakresu portów (np. `88__-8831`), wdrożyliśmy **Mapowanie portów** na routerze (Fritz!Box).

| Punkt końcowy | Protokół | Port | Opis |
| :--- | :--- | :--- | :--- |
| **Zewnętrzne/Publiczne** | TCP | `88__` (Przykład) | Port, z którego musi korzystać klient (Lub). |
| **Wewnętrzne/lokalne** | TCP | `8000` | Port, na którym faktycznie nasłuchuje usługa FastAPI (`--port 8000`). |

Router tłumaczy każde połączenie przychodzące na porcie zewnętrznym („88__”) na port wewnętrzny („8000”) hosta, dzięki czemu usługa jest dostępna globalnie bez zmiany konfiguracji serwera podstawowego.

## 3. Użycie klienta CLI

Klient musi mieć skonfigurowany publiczny adres IP, port zewnętrzny i prawidłowy klucz API.

### Składnia końcowego polecenia

__KOD_BLOKU_0__