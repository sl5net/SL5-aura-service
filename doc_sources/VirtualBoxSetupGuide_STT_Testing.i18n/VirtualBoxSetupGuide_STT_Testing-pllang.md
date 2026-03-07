# Przewodnik konfiguracji VirtualBox do testowania projektów STT

Ten przewodnik zawiera zalecane kroki dotyczące konfigurowania stabilnej i wydajnej maszyny wirtualnej Ubuntu 24.04 w VirtualBox. Postępowanie zgodnie z tymi instrukcjami stworzy spójne środowisko do testowania aplikacji STT i pozwoli uniknąć typowych problemów, takich jak powolna instalacja, zawieszanie się systemu i brak funkcjonalności schowka.

## Warunki wstępne

- VirtualBox zainstalowany na komputerze hosta.
- Pobrano plik ISO systemu Ubuntu 24.04 Desktop.

## Referencyjny sprzęt hosta

Ta konfiguracja została przetestowana i sprawdzona w następującym systemie hosta. Wydajność może się różnić na innym sprzęcie, ale ustawienia stabilności powinny mieć zastosowanie uniwersalne.

- **System operacyjny:** Manjaro Linux
- **Jądro:** 6.6.94
- **Procesor:** 16 × AMD Ryzen 7 3700X
- **Pamięć:** 31,3 GiB pamięci RAM
- **Procesor graficzny:** NVIDIA GeForce GTX 1050 Ti

---

## Część 1: Tworzenie i konfiguracja maszyny wirtualnej

Te ustawienia są krytyczne dla wydajności i stabilności.

### Krok 1.1: Utwórz nową maszynę wirtualną

1. W VirtualBox kliknij **Nowy**.
2. **Nazwa:** `Tester Ubuntu STT` (lub podobny).
3. **Obraz ISO:** Pozostaw to pole puste.
4. Zaznacz pole: **„Pomiń instalację nienadzorowaną”**.
5. Kliknij **Dalej**.
6. **Sprzęt:**
- **Pamięć podstawowa:** `4096 MB` lub więcej.
- **Procesory:** `4` lub więcej.
7. Kliknij **Dalej**.

### Krok 1.2: Utwórz wirtualny dysk twardy (KRYTYCZNY)

Jest to najważniejszy krok zapewniający szybką instalację i wydajność.

1. Wybierz **„Utwórz teraz wirtualny dysk twardy”**.
2. Ustaw rozmiar dysku na **40 GB** lub więcej.
3. Na następnym ekranie zmień typ przechowywania na **„Stały rozmiar”**.
> **Dlaczego?** Dysk o stałym rozmiarze jest wstępnie przydzielany, co zapobiega powstawaniu ogromnych wąskich gardeł we/wy, które powstają, gdy rozmiar dysku „alokowanego dynamicznie” stale zmienia się podczas instalacji.
4. Kliknij **Utwórz** i poczekaj na zakończenie procesu.

### Krok 1.3: Ostateczne ustawienia maszyny wirtualnej

Wybierz nowo utworzoną maszynę wirtualną i kliknij **Ustawienia**. Skonfiguruj następujące elementy:

- **System -> Płyta główna:**
- **Chipset:** `ICH9`
- Zaznacz **„Włącz EFI (tylko specjalne systemy operacyjne)”**.

- **Wyświetlacz -> Ekran:**
- **Kontroler grafiki:** `VMSVGA`
- **Odznacz opcję „Włącz akcelerację 3D”**.
> **Dlaczego?** Akceleracja 3D jest częstą przyczyną zawieszania się i zawieszania systemu u gości z systemem Linux. Wyłączenie tej opcji znacząco poprawia stabilność.

-   **Składowanie:**
- Wybierz **Kontroler SATA**. Zaznacz pole **„Użyj pamięci podręcznej we/wy hosta”**.
- Wybierz plik dysku wirtualnego (`.vdi`). Zaznacz pole **„Dysk półprzewodnikowy”**.
- Wybierz **Pusty** napęd optyczny. Kliknij ikonę CD po prawej stronie i **„Wybierz plik dyskowy…”**, aby załączyć obraz ISO systemu Ubuntu 24.04.

Kliknij **OK**, aby zapisać wszystkie ustawienia.

---

## Część 2: Instalacja systemu operacyjnego Ubuntu

1. Uruchom maszynę wirtualną.
2. Przejdź przez konfigurację języka i klawiatury.
3. Po dotarciu do „Aktualizacje i inne oprogramowanie” wybierz:
- **Minimalna instalacja**.
- **Odznacz** „Pobierz aktualizacje podczas instalacji Ubuntu”.
4. Kontynuuj instalację aż do jej zakończenia.
5. Po zakończeniu uruchom ponownie maszynę wirtualną. Po wyświetleniu monitu usuń nośnik instalacyjny (naciśnij Enter).

---

## Część 3: Poinstalacja (dodatki gościnne)

Ten krok umożliwia udostępnianie schowka, przeciąganie i upuszczanie oraz automatyczną zmianę rozmiaru ekranu.

### Krok 3.1: Zainstaluj dodatki ISO na hoście (w razie potrzeby)

Upewnij się, że na **maszynie hosta** jest zainstalowany pakiet ISO dodatków dla gości.

- **Na Arch / Manjaro:**
__KOD_BLOKU_0__
- **W Debianie/Ubuntu:**
__KOD_BLOKU_1__

### Krok 3.2: Zainstaluj dodatki gościnne na maszynie wirtualnej Ubuntu

Wykonaj te kroki **w działającej maszynie wirtualnej Ubuntu**.

1. **Przygotuj Ubuntu:** Otwórz terminal i uruchom następujące polecenia, aby zainstalować zależności kompilacji.
__KOD_BLOKU_2__
2. **Włóż płytę CD:** Z górnego menu VirtualBox przejdź do **Urządzenia -> Włóż obraz płyty CD z dodatkami dla gości...**.
3. **Uruchom instalator:**
- Może pojawić się okno dialogowe z prośbą o uruchomienie oprogramowania. Kliknij **Uruchom**.
- Jeśli nie pojawi się żadne okno dialogowe, otwórz Menedżera plików, kliknij prawym przyciskiem myszy płytę CD `VBox_GAs...`, wybierz **"Otwórz w terminalu"** i uruchom polecenie:
__KOD_BLOKU_3__
4. **Uruchom ponownie:** Po zakończeniu instalacji uruchom ponownie maszynę wirtualną.
__KOD_BLOKU_4__
5. **Włącz funkcje:** Po ponownym uruchomieniu przejdź do menu **Urządzenia** i włącz **Udostępniony schowek -> Dwukierunkowy** oraz **Przeciągnij i upuść -> Dwukierunkowy**.

Twoje stabilne i wydajne środowisko testowe jest już gotowe.