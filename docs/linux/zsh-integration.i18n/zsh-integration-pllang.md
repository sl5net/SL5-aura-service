# Integracja powłoki Zsh

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do pliku `~/.zshrc`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

1. Otwórz konfigurację Zsh w edytorze, który lubisz:
__KOD_BLOKU_0__

2. Wklej następujący blok na końcu pliku:

__KOD_BLOKU_1__

3. Załaduj ponownie swoją konfigurację:
__KOD_BLOKU_2__

## Cechy
- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.
__KOD_BLOKU_3__