# Bezpieczne automatyczne zamykanie i wbudowana dokumentacja

## Koncepcja
SL5 Aura monitoruje foldery prywatne zaczynające się od `_` (np. `_moje_poufne_dane`).
Po wykryciu zmian Aura automatycznie tworzy **szyfrowane** archiwum ZIP.

## Krytyczny warunek wstępny: klucz szyfrujący
**Szyfrowanie jest obowiązkowe.** Proces automatycznego zipowania wymaga obecności pliku haseł w hierarchii katalogów (foldery bieżące lub nadrzędne).

* **Wymagania dotyczące pliku:** Plik haseł musi zaczynać się od kropki `.` (np. `.archive_pass`, `.secret`).
* **Zachowanie:** Jeśli nie zostanie znaleziony plik z hasłem, proces zip zostanie **zablokowany**. To zabezpieczenie gwarantuje, że niezaszyfrowane dane nigdy nie zostaną spakowane.

## Wzorzec „Osadzone dokumenty”.
Ponieważ system ponownego ładowania na gorąco Aury nasłuchuje **prawidłowych plików Pythona**, aktualizacja prostego pliku Readme `.txt` nie spowoduje ponownego zip.

Aby dołączyć instrukcje dla odbiorców (np. „Jak rozpakować”), jednocześnie zapewniając uruchomienie wyzwalacza, użyj **pliku Python Docstring**.

### Implementacja
Utwórz plik o nazwie `README_AUTOZIP.py` w monitorowanym folderze.

__KOD_BLOKU_0__