# 💡 Prezentacja funkcji: trwałe buforowanie wtyczek

## 💾 Buforowanie zapewniające wydajność, niezawodność i wydajność sieci

System oferuje teraz centralny, trwały mechanizm buforowania („simple_plugin_cache”) zaprojektowany w celu zmniejszenia obciążenia sieci zewnętrznej (np. pogody, interfejsów API tłumaczeń) i przyspieszenia wykonywania. Pamięć podręczna jest **trwała**, co oznacza, że wpisy przetrwają ponowne uruchomienie usługi.

**Cel:** Zmniejszenie ruchu sieciowego, zapobieganie nadużyciom API i zapewnianie szybkich reakcji awaryjnych w przypadku przerw w świadczeniu usług zewnętrznych.

---

### 1. Podstawowa implementacja buforowania (oparta na TTL)

Aby buforować wynik funkcji, musisz zaimplementować podstawową logikę w trzech blokach: **Sprawdź**, **Wykonaj** i **Zapisz**.

#### 1.1 Import i konfiguracja

Dodaj niezbędne importy i zdefiniuj stałą czasu wygaśnięcia (TTL) w skrypcie wtyczki (np. `weather.py`):

__KOD_BLOKU_0__

#### 1.2 Logika buforowania w bloku `execute`

Funkcja „execute” musi najpierw podjąć próbę pobrania wyników z pamięci podręcznej przed wykonaniem jakichkolwiek wywołań sieciowych.

__KOD_BLOKU_1__

---

### 2. Zaawansowane tryby buforowania

#### A. Stałe (wieczne) buforowanie

Jeśli wynik **nigdy nie wygaśnie** (np. wyszukiwanie konfiguracji statycznej), pomiń całkowicie parametr `ttl_sekundy`.

__KOD_BLOKU_2__

#### B. Wymagania dotyczące klucza pamięci podręcznej (`key_args`).

* `argumenty_klucza` musi być **krotką** zawierającą wszystkie zmienne definiujące wynik (np. `(miasto, język, system_jednostek)`).
* Mechanizm buforowania automatycznie konwertuje typowe obiekty Pythona, które nie nadają się do serializacji w formacie JSON, takie jak **`pathlib.Path`**, na ciągi znaków w celu wygenerowania klucza.