# Zaawansowane buforowanie wyników (z uwzględnieniem stanu)

## Przegląd
Aura posiada trwałą, kontekstową pamięć podręczną wyników, zaprojektowaną w celu wyeliminowania zbędnego przetwarzania. Kiedy polecenie głosowe zostanie rozpoznane i pasuje do reguły, Aura sprawdza, czy w tych samych okolicznościach wygenerowano wcześniej dokładnie taki sam wynik. Jeśli zostanie znalezione dopasowanie, Aura omija kosztowne operacje, takie jak **sprawdzanie gramatyki LanguageTool** lub **generowanie Ollama LLM**, dostarczając wynik z niemal zerowym opóźnieniem.

## Kluczowe funkcje
- **Uwzględnianie kontekstu:** Pamięć podręczna jest specyficzna dla tytułu aktywnego okna. Polecenie wydane w „LibreOffice” może mieć inny wynik w pamięci podręcznej niż to samo polecenie w „Terminalu”.
- **Samonaprawa (automatyczne unieważnianie):** Pamięć podręczna automatycznie wygasa, jeśli zmodyfikujesz podstawowy plik reguł (mapa `.py`).
- **Prywatność przede wszystkim:** Wszystkie wyniki w pamięci podręcznej są przechowywane w lokalnej bazie danych SQLite (`data/_aura_result_cache.db`).
- ** Zero konserwacji:** W przypadku większości użytkowników działa to całkowicie w tle, bez konfiguracji.

## Jak to działa
System generuje unikalny `cache_id` na podstawie trzech zmiennych:
1. **Wyjście reguły:** Tekst wygenerowany przez mapę.
2. **Język:** aktualny kod aktywnego języka (np. `de-DE`).
3. **Aktywne okno:** Tytuł aktualnie aktywnego okna.

### Logika ważności
Pamięć podręczna gwarantuje, że nigdy nie otrzymasz „nieaktualnych” informacji. Wykorzystuje dwa rodzaje kontroli ważności:

| Wpisz | Imię | Logika | Przypadek użycia |
| :--- | :--- | :--- | :--- |
| **Typ 0** | **Automatyczna synchronizacja plików** | Wykorzystuje czas modyfikacji („mtime”) pliku mapy. | **Standard.** Jeśli edytujesz piaskownicę lub mapę, wszystkie powiązane wpisy w pamięci podręcznej zostaną natychmiast unieważnione. |
| **Typ 1** | **Ręczny znacznik czasu** | Używa stałego „znacznika czasu” podanego w atrybutach reguły. | **Programista.** Zakoduj na stałe wersję/sygnaturę czasową, aby wymusić lub utrzymać określony stan wyniku. |

## Przykłady konfiguracji reguł

Możesz kontrolować zachowanie buforowania bezpośrednio w plikach `FUZZY_MAP_pre.py` lub `FUZZY_MAP.py`.

### 1. Zachowanie domyślne (automatyczne buforowanie)
Domyślnie buforowanie jest włączone i wykorzystuje czas modyfikacji pliku.
__KOD_BLOKU_0__

### 2. Wyłączanie pamięci podręcznej
Jeśli polecenie generuje dane dynamiczne (takie jak bieżący czas lub losowy żart), powinieneś wyłączyć pamięć podręczną.
__KOD_BLOKU_1__

### 3. Ręczny znacznik czasu (stała wersja)
Jeśli chcesz, aby pamięć podręczna trwała niezależnie od edycji pliku (chyba że zmienisz wersję), użyj ręcznego znacznika czasu.
__KOD_BLOKU_2__

## Wpływ na wydajność
- **Brak pamięci podręcznej:** Przetwarzanie standardowe (0,05 s – 5,0 s w zależności od wykorzystania LLM).
- **Hit pamięci podręcznej:** Natychmiastowe przetwarzanie.

Dzięki temu mechanizmowi polecenia lub poprawione literówki są natychmiast zwracane, bez obciążania procesora.