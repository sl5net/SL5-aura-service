# Paleta poleceń i przewodnik wyszukiwania map

Ten przewodnik wyjaśnia, jak skonfigurować i używać ogólnosystemowej, niezależnej od lokalizacji **Palety poleceń** dla SL5 Aura. Umożliwia interaktywne przeszukiwanie reguł mapy, wyświetlanie podglądów wykonania na żywo z lokalnej pamięci podręcznej SQLite i natychmiastowe wpisywanie wybranych wyników w aktywnym kursorze.

## Warunki wstępne

Upewnij się, że następujące usługi i narzędzia działające w tle są zainstalowane i aktywne:
1. **`fzf`** (Wyszukiwarka rozmyta)
2. **CopyQ** (Menedżer schowka, używany do globalnej orkiestracji skrótów klawiszowych)
3. **`type_watcher.sh`** (demon pisania w tle Aury)

---

## Globalna konfiguracja skrótu CopyQ

Aby natychmiast uruchomić paletę poleceń z dowolnego aktywnego okna (np. przeglądarki lub edytora tekstu), skonfiguruj globalny klawisz skrótu w CopyQ:

1. Otwórz **CopyQ** i naciśnij `F6` (lub przejdź do **Polecenia** / **Befehle**).
2. Kliknij **Dodaj** (Hinzufügen) i nadaj mu nazwę `Paleta poleceń Aura`.
3. Ustaw żądany **Skrót globalny** (np. `Meta+S` lub `Ctrl+Alt+S`).
4. Ustaw **Typ** na „Polecenie” (Befehl).
5. Wklej następujący kod JavaScript w polu poleceń:

__KOD_BLOKU_0__