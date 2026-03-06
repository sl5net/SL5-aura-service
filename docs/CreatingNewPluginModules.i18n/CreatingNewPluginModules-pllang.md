## Tworzenie nowych modułów wtyczek

Nasz framework wykorzystuje potężny system automatycznego wykrywania do ładowania modułów reguł. Dzięki temu dodawanie nowych zestawów poleceń jest proste i przejrzyste, bez konieczności ręcznego rejestrowania każdego nowego komponentu. W tym przewodniku wyjaśniono, jak tworzyć, organizować i zarządzać własnymi modułami niestandardowymi.

### Podstawowa koncepcja: moduły oparte na folderach

Moduł to po prostu folder w katalogu `config/maps/`. System automatycznie skanuje ten katalog i traktuje każdy podfolder jako moduł do załadowania.

### Przewodnik krok po kroku dotyczący tworzenia modułu

Wykonaj poniższe kroki, aby utworzyć nowy moduł, na przykład do przechowywania makr dla konkretnej gry.

**1. Przejdź do katalogu Map**
Wszystkie moduły reguł znajdują się w folderze `config/maps/` projektu.

**2. Utwórz folder modułu**
Utwórz nowy folder. Nazwa powinna być opisowa i zawierać podkreślenia zamiast spacji (np. `moja_makro_gry`, `niestandardowa_automatyzacja_domu`).

**3. Dodaj podfoldery języka (krok krytyczny)**
W folderze nowego modułu musisz utworzyć podfoldery dla każdego języka, który chcesz obsługiwać.

* **Konwencja nazewnictwa:** Nazwy tych podfolderów **muszą być prawidłowymi kodami języka i ustawień regionalnych**. System używa tych nazw do załadowania poprawnych reguł dla aktywnego języka.
* **Poprawne przykłady:** `de-DE`, `en-US`, `en-GB`, `pt-BR`
* **Uwaga:** Jeśli użyjesz niestandardowej nazwy, takiej jak `niemiecki` lub `english_rules`, system albo zignoruje folder, albo potraktuje go jako oddzielny moduł niespecyficzny dla języka.

**4. Dodaj swoje pliki reguł**
Umieść pliki reguł (np. `FUZZY_MAP_pre.py`) w podfolderze odpowiedniego języka. Najprostszym sposobem na rozpoczęcie jest skopiowanie zawartości istniejącego folderu modułu językowego w celu użycia go jako szablonu.

### Przykładowa struktura katalogów

__KOD_BLOKU_0__

### Zarządzanie modułami w konfiguracji

System zaprojektowano tak, aby wymagał minimalnej konfiguracji.

#### Włączanie modułów (domyślne)

Moduły są **domyślnie włączone**. Jeśli w `config/maps/` istnieje folder modułu, system go znajdzie i załaduje jego reguły. **Nie musisz dodawać wpisu do pliku ustawień, aby włączyć nowy moduł.**

#### Wyłączanie modułów

Aby wyłączyć moduł, musisz dodać dla niego wpis w słowniku `PLUGINS_ENABLED` w pliku ustawień i ustawić jego wartość na `False`.

**Przykład (`config/settings.py`):**
__KOD_BLOKU_1__
### Ważne uwagi projektowe

* **Zachowanie domyślne: Brak wpisu równa się `True`**
Jeśli moduł nie jest wymieniony w słowniku `PLUGINS_ENABLED`, domyślnie jest uważany za **aktywny**. Dzięki takiemu rozwiązaniu plik konfiguracyjny jest czysty, ponieważ wystarczy jedynie wyświetlić listę wyjątków.

* **Skrót od Włączanie**
Twój system konfiguracyjny rozumie również, że wypisanie klucza modułu bez wartości oznacza, że jest on włączony. Na przykład dodanie „wannweil” do słownika jest równoznaczne z dodaniem „wannweil”: True. Zapewnia to wygodny skrót umożliwiający włączanie modułów.

* **Wyłączanie modułów nadrzędnych:** Zamierzone zachowanie polega na tym, że wyłączenie modułu nadrzędnego powinno XSPACEbreakX
automatycznie wyłącza wszystkie moduły podrzędne i podfoldery językowe. Na przykład ustawienie `"standard_actions": False` powinno uniemożliwić załadowanie zarówno `de-DE`, jak i `en-US`. (27.10.25 pon.)
XSPACEbreakX
*   **bramka**
Celem jest dalsze udoskonalanie tego systemu. Na przykład umożliwienie respektowania ustawień modułu podrzędnego, nawet jeśli moduł nadrzędny jest wyłączony, lub wprowadzenie bardziej złożonych reguł dziedziczenia. (27.10.25 pon.)