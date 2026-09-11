# Nakładka nagrywania (wyświetlanie na ekranie)

Nakładka nagrywania zapewnia natychmiastowy, wieloplatformowy wizualny wskaźnik stanu dyktowania. Działa niezależnie od demonów powiadomień na pulpicie i filtrów „Nie przeszkadzać”, wyświetlając stan bezpośrednio na ekranie głównym.

## Przykłady wizualne

| Lewy dolny róg („bl”) | Prawy górny róg („tr”) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *Wtapia się w ciemne panele i tace systemowe* | *Wysoki kontrast w przypadku jasnych lub skomplikowanych okien* |

## Stany

- **Nagrywanie (`🔴`)**: Żywo czerwone kółko z podświetlonym konturem (`#e62222` na `#181818`) sygnalizuje aktywne nagrywanie dźwięku.
- **Bezczynny**:
- `ukryte` (domyślnie): Okno jest całkowicie wycofane, uwalniając miejsce na pulpicie dla normalnej interakcji.
- `pentagon`: Wyświetla subtelny geometryczny pięciokąt („⬟”) w trybie bezczynności.

## Konfiguracja

Ustawieniami zarządza się w `config/settings.py`:

__KOD_BLOKU_0__

## Architektura

- Zbudowany przy użyciu standardowej biblioteki Pythona (`tkinter`), nie wymagającej żadnych zewnętrznych zależności C.
- Wykonuje się w wątku demona w tle z bezpieczną wątkowo obsługą zdarzeń kolejki.
- Dynamicznie wykrywa główny monitor w środowiskach z wieloma wyświetlaczami.

(s, 10.9.'26 14:41 czw)