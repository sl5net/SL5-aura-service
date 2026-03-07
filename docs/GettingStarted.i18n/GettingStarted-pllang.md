# Pierwsze kroki z SL5 Aura

## Czym jest aura SL5?

SL5 Aura to asystent głosowy działający w trybie offline, który konwertuje mowę na tekst (STT) i stosuje konfigurowalne reguły w celu czyszczenia, poprawiania i przekształcania danych wyjściowych.

Działa bez GUI – wszystko działa poprzez CLI lub konsolę.

## Jak to działa

__KOD_BLOKU_0__

1. **Vosk** konwertuje mowę na surowy tekst
2. **Wstępne mapy** oczyść i popraw tekst przed sprawdzeniem pisowni
3. **LanguageTool** poprawia gramatykę i pisownię
4. **Post-Mapy** stosują ostateczne transformacje
5. **Wyjście** to ostateczny czysty tekst (i opcjonalnie TTS)

## Twoje pierwsze kroki

### 1. Uruchom Aurę
__KOD_BLOKU_1__

### 2. Przetestuj za pomocą danych wejściowych z konsoli
Wpisz „s”, a następnie swój tekst:
__KOD_BLOKU_2__

### 3. Zobacz regułę w działaniu
Otwórz `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

Odkomentuj regułę w środku i przetestuj ponownie. Co się dzieje?

## Zrozumienie zasad

Reguły znajdują się w `config/maps/` w plikach Pythona o nazwie `FUZZY_MAP_pre.py` lub `FUZZY_MAP.py`.

Reguła wygląda następująco:
__KOD_BLOKU_3__

**Wyjście** jest najważniejsze – od razu widzisz, co daje reguła.

Reguły są przetwarzane **od góry do dołu**. Pierwszy pełny mecz (`^...$`) zatrzymuje wszystko.

## Koany – nauka przez działanie

Koany to małe ćwiczenia w `config/maps/koans_deutsch/` i `config/maps/koans_english/`.

Każdy koan uczy jednej koncepcji:

| Koan | Temat |
|---|---|
| 01_koan_erste_schritte | Pierwsza zasada, pełny mecz, zatrzymanie rurociągu |
| 02_koan_słuchaj | Listy, wiele reguł |
| 03_koan_schwierige_namen | Trudne nazwy, dopasowanie fonetyczne |

Zacznij od Koana 01 i pnij się w górę.

## Porady

- Reguły w `FUZZY_MAP_pre.py` uruchamiają się **przed** sprawdzaniem pisowni – dobre do naprawiania błędów STT
- Reguły w `FUZZY_MAP.py` działają **po** sprawdzeniu pisowni – dobre do formatowania
- Pliki kopii zapasowych (`.peter_backup`) są tworzone automatycznie przed jakąkolwiek zmianą
- Użyj `peter.py`, aby sztuczna inteligencja automatycznie przeglądała koany