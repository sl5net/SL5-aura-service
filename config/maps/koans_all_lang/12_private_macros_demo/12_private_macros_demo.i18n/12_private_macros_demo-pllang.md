# Koan 12: Demo prywatnych makr

To ćwiczenie pokazuje, jak używać zagnieżdżonych makr prywatnych i ograniczać ich zakres do określonych aktywnych okien przy użyciu konfiguracji „tylko_w_oknach”.

## Wymaganie zabezpieczeń aktywnego okna
Aby zapobiec globalnemu wykonywaniu tych reguł demonstracyjnych (takich jak imię, adres e-mail lub numer telefonu) podczas innych testów systemu, są one ograniczone do aktywnych okien pasujących do wzorca `12_private_macros_demo`.

Aby przetestować te reguły, musisz:
1. Użyj edytora, który wyświetla pełną ścieżkę pliku w tytule okna (np. PyCharm lub VS Code).
2. Zapisz lub zmień nazwę edytowanego pliku tak, aby jego nazwa zawierała `12_private_macros_demo` w twoim edytorze (np. w edytorze Kate).

---

## Instrukcje

1. Podaj nazwę folderu swojego języka (na przykład „de-DE” dla języka niemieckiego, „en-US” dla języka angielskiego, „fr-FR” dla języka francuskiego)
2. Upewnij się, że w folderze językowym znajduje się plik o nazwie `FUZZY_MAP_pre.py`. Jeśli nie istnieje, utwórz go.
3. Skopiuj poniższe reguły szablonu do swojej listy `FUZZY_MAP_pre` znajdującej się w tym pliku.

### Obsługiwane foldery językowe
Jeśli folder dla Twojego języka jeszcze nie istnieje w `config/maps/koans_deutsch/12_private_macros_demo/`, musisz go utworzyć ręcznie. Użyj dokładnych nazw folderów wymienionych poniżej:

- `ar` (arabski)
- `de-DE` (niemiecki)
- `en-US` (angielski)
- `es` (hiszpański)
- `fr` (francuski)
- „cześć” (hindi)
- „ja” (japoński)
- „ko” (koreański)
- `pl` (polski)
- `pt-BR` (portugalski – Brazylia)
- `pt` (portugalski)
- `zh-CN` (chiński – uproszczony)


### Szablon reguły

__KOD_BLOKU_0__