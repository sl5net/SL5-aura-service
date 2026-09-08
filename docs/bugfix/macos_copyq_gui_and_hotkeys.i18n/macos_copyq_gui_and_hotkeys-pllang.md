# Rozwiązywanie problemów z systemem CopyQ macOS: niewidoczny interfejs graficzny i ręczna konfiguracja klawiszy skrótu

W tym przewodniku omówiono typowe problemy napotykane w systemie macOS (w szczególności na urządzeniach Apple Silicon z serii M), gdzie interfejs graficzny CopyQ (GUI) nie pojawia się lub trzeba ponownie przypisać skróty globalne (takie jak F10) bez uzyskiwania dostępu do GUI.

---

## 1. Rozwiązywanie problemów z niewidocznym interfejsem graficznym

W systemie macOS CopyQ może działać poprawnie w tle, pozostając wizualnie ukryty z dwóch głównych powodów:
- **Współrzędne okna poza ekranem**: Po zmianie rozdzielczości lub odłączeniu monitora zewnętrznego, CopyQ może zachować współrzędne poza widocznym obszarem wyświetlania.
- **Zablokowanie wycięcia paska menu**: W modelach MacBooka z wycięciem na aparat macOS automatycznie ukrywa nadmiar ikon paska menu za wycięciem, gdy taca jest pełna.

### Rozwiązanie: Zresetuj geometrię i wymuś wyświetlanie

Wykonaj następujące polecenia w terminalu, aby usunąć współrzędne poza ekranem i przenieść okno na pierwszy plan:

__KOD_BLOKU_0__

Jeśli okno nadal się nie wyświetla, przełącz jego stan za pomocą interfejsu CLI:

__KOD_BLOKU_1__

---

## 2. Ręczna zmiana skrótów klawiszowych za pomocą CudaText

Kiedy globalny skrót (taki jak `F10`) zostanie zajęty lub przechwycony przez inną aplikację, skrót można edytować bezpośrednio w pliku konfiguracyjnym za pomocą CudaText bez otwierania GUI CopyQ.

### Krok 1: Zakończ proces CopyQ

CopyQ należy zatrzymać przed edycją pliku konfiguracyjnego, aby zapobiec zastąpieniu zmian po zakończeniu:

__KOD_BLOKU_2__

### Krok 2: Otwórz konfigurację w CudaText

W systemie macOS skróty poleceń CopyQ są przechowywane w pliku `copyq-commands.ini`.

Otwórz plik w CudaText:

__KOD_BLOKU_3__

*Uwaga: Jeśli plik nie istnieje w `Application Support`, otwórz zastępczą lokalizację XDG:*

__KOD_BLOKU_4__

### Krok 3: Przypisz ponownie skrót

1- W CudaText naciśnij `Cmd + F`, aby otworzyć pasek wyszukiwania.
2- Wyszukaj `F10` lub `GlobalShortcut=F10`.
3- Zamień „F10” na dostępny skrót (np. „F9”, „Ctrl+F10” lub „Meta+F10”).
4- Zapisz plik (`Cmd + S`) i zamknij CudaText (`Cmd + Q`).

### Krok 4: Uruchom ponownie CopyQ

Uruchom ponownie CopyQ, aby załadować zaktualizowaną konfigurację skrótu:

__KOD_BLOKU_5__

Nowy globalny skrót będzie teraz aktywny.

(aktualizacja: 8.9.'26 08:01 Wt)