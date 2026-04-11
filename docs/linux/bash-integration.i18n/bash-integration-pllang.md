# Integracja z powłoką Bash

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do pliku `~/.bashrc`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

1. Otwórz konfigurację Bash w edytorze, który lubisz:
__KOD_BLOKU_0__

2. Wklej następujący blok na końcu pliku:

__KOD_BLOKU_1__

3. Załaduj ponownie swoją konfigurację:
__KOD_BLOKU_2__

> **Uwaga:** Jeśli używasz Bash jako powłoki logowania (np. przez SSH), dodaj także ten sam blok do `~/.bash_profile` lub pobierz z niego `~/.bashrc`:
> ```bzdura
> [ -f ~/.bashrc ] && źródło ~/.bashrc
> ```

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.