# Przewodnik konfiguracji DEV_MODE

## Problem

ponieważ jesteśmy kompatybilni z Weylandem, do logowania używamy `threading.Lock`.

Teraz (21.3.'26 sobota) zmieniły się zasady logowania. W Manjaro nie było to żadnym problemem.

Kiedy `DEV_MODE = 1` jest aktywne, Aura tworzy setki wpisów w dzienniku na sekundę
z wielu wątków. Może to spowodować zakleszczenie `SafeStreamToLogger` i wykonanie
Aura zawiesza się po pierwszym uruchomieniu dyktowania.

## Poprawka: użyj filtra LOG_ONLY

Podczas programowania z `DEV_MODE = 1` **musisz** także skonfigurować filtr dziennika w:
`config/filters/settings_local_log_filter.py`

### Minimalny działający filtr dla DEV_MODE:
__KOD_BLOKU_0__

## Jedna linijka dla settings_local.py
Dodaj ten komentarz jako przypomnienie obok ustawienia DEV_MODE:
__KOD_BLOKU_1__

## Główna przyczyna
`SafeStreamToLogger` używa `threading.Lock` do ochrony zapisów na standardowe wyjście.
Przy dużym obciążeniu dziennika (DEV_MODE) rywalizacja o blokady powoduje zakleszczenie systemów
z agresywnym planowaniem wątków (np. CachyOS z nowszymi jądrami/glibc).