# Tryb terminala (wykluczenie języka)

Tryb terminala to stan konfiguracji, w którym nie są instalowane ani konfigurowane żadne określone pakiety językowe dla jednostek przetwarzania mowy/tekstu.

## Jak włączyć
Podczas początkowej konfiguracji lub skryptu wyboru języka, gdy zostaniesz poproszony o podanie **Języka podstawowego**, wpisz:
- `n`
- „żaden”.
- `0`

## Efekty
- **EXCLUDE_LANGUAGES** jest ustawione na „wszystkie”.
- Żadne modele specyficzne dla języka (takie jak modele Whisper lub Vosk) nie zostaną pobrane ani zainicjowane.
— System działa w trybie „Tylko terminal”, przydatnym w środowiskach o małej liczbie dysków lub gdy wymagane są tylko podstawowe narzędzia CLI bez obsługi zlokalizowanej mowy.

## Zmienne środowiskowe
Gdy jest aktywny, generowane są następujące eksporty:
__KOD_BLOKU_0__