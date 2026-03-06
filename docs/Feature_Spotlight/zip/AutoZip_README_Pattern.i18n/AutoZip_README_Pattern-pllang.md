planuję nie działać w tej chwili bez hasła do folderów gdzieś w górze. pliki haseł muszą zaczynać się od kropki „.”


# Automatyczny przepływ pracy i osadzona dokumentacja

## Koncepcja
SL5 Aura automatycznie monitoruje foldery zaczynające się od `_` (np. `_moja_aplikacja`). Po wykryciu zmian Aura automatycznie kompresuje folder do archiwum ZIP.

**Ograniczenie krytyczne:**
System „Hot-Reload” i system monitorowania firmy Aura specjalnie nasłuchuje zmian w **prawidłowych plikach Pythona**. Prosta aktualizacja pliku tekstowego (`.txt`) **nie** uruchomi procesu automatycznego zipowania.

## Wzorzec „Osadzone dokumenty”.
Aby dołączyć instrukcje dla odbiorców nietechnicznych (np. HR, klientów), jednocześnie zapewniając, że Aura wykryje zmianę i zaktualizuje plik ZIP, używamy **pliku Python Docstring**.

Ten plik jest technicznie poprawnym skryptem Pythona (spełniającym wymagania parsera Aury), ale wizualnie wygląda jak standardowy dokument tekstowy dla użytkownika.

### Implementacja
Utwórz plik o nazwie `README_AUTOZIP.py` w monitorowanym folderze.

**Przewodnik po stylu:**
1. Użyj `# Dokumentacja` jako pierwszej linii (zamiast nazwy skryptu technicznego), aby być gościnnym.
2. Użyj dokumentu z potrójnym cudzysłowem („””) dla treści.
3. Żaden inny kod nie jest wymagany.

### Przykładowy kod

__KOD_BLOKU_0__