# Integracja POSIX sh / Dash

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do swojego profilu powłoki. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

> **Uwaga:** Dash i inne powłoki POSIX (`/bin/sh` w Debianie/Ubuntu domyślnie to Dash) **nie** obsługują słowa kluczowego `local` we wszystkich kontekstach, podstawieniach procesów i tablicach. Poniższa funkcja została napisana tak, aby była w pełni kompatybilna z POSIX.

## Instrukcje konfiguracji

1. Otwórz swój profil powłoki w edytorze, który lubisz:
__KOD_BLOKU_0__

2. Wklej następujący blok na końcu pliku:

__KOD_BLOKU_1__

3. Załaduj ponownie swoją konfigurację:
__KOD_BLOKU_2__

## Uwagi dotyczące POSIX / myślnika

- Słowo „lokalny” **nie** jest tutaj używane w celu zapewnienia maksymalnej kompatybilności. Wszystkie zmienne mają zakres funkcji wyłącznie zgodnie z konwencją; są technicznie globalne w ścisłym POSIX sh.
- `$@` jest preferowane zamiast `$*` przy przekazywaniu argumentów do poleceń, aby zachować prawidłowe dzielenie słów na argumenty w cudzysłowie.
- `bash` zostaje zastąpiony przez `sh` podczas wykonywania skryptu pomocniczego Kiwix, aby pozostać w zestawie narzędzi POSIX.
- Ten plik konfiguracyjny najlepiej umieścić w `~/.profile`, którego źródłem są powłoki logowania. W przypadku interaktywnych powłok niezalogowanych Twoja dystrybucja może używać `~/.shrc` — sprawdź dokumentację systemu.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.