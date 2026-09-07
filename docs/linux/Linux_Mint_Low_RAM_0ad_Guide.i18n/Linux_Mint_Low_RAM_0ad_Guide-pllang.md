# Running 0 A.D. ze sterowaniem głosowym Aura na systemach z małą ilością pamięci RAM (Linux Mint)

Ten przewodnik dokumentuje konfigurację i optymalizację pamięci do uruchamiania sterowania głosowego **sl5net Aura** wraz z **0 A.D.** na starszym lub ograniczonym sprzęcie Linux Mint.

## Docelowy profil sprzętu i systemu
- **Urządzenie**: Lenovo ThinkPad T520 (Laptop)
- **Procesor**: Intel Core i7-2620M (dwurdzeniowy @ 2,70 GHz - 3,40 GHz)
- **Pamięć**: 5,67 GiB RAM
- **Zamiana**: Efektywna wymiana 4 GiB
- **System operacyjny**: Linux Mint 21.3 Virginia (64-bitowy)
- **Środowisko komputerowe**: Cinnamon 6.0.5 (serwer wyświetlacza X11)
- **Cel zastosowania**: 0 r. n.e. (Imperia Ascendent)

## Zarządzanie pamięcią i architektura
W systemach z ≤ 6 GiB RAM, jednoczesne uruchomienie ciężkiego środowiska graficznego, gry 3D RTS (0 A.D.) i rozpoznawania mowy wymaga ścisłej ochrony pamięci:

1. **Priorytet modelu mowy Vosk**:
- Używa `vosk-model-small-de` (lub odpowiednika w języku) w celu zmniejszenia zużycia pamięci (~300-500 MB).
- Priorytetem jest zachowanie modelu Voska, aby zapewnić reakcję na polecenia w czasie rzeczywistym podczas rozgrywki.

2. **Automatyczne usunięcie narzędzia LanguageTool**:
- Proces Java LanguageTool może zużywać ~1,34 GiB RSS.
- Kiedy dostępna pamięć RAM spadnie poniżej `CRITICAL_THRESHOLD_MB` (2,0 GiB), `model_manager` firmy Aura natychmiast kończy LanguageTool, aby zwolnić ~ 1,3 GiB RAM dla gry.
- 5-minutowy czas odnowienia (`set_language_tool_cooldown`) zapobiega ponownemu uruchomieniu LanguageTool i uszkodzeniu pamięci podczas aktywnej rozgrywki.

## Polecenia weryfikacyjne
Aby sprawdzić stan pamięci systemowej i procesów:
# Sprawdź użycie pamięci i zamiany
__KOD_BLOKU_0__

# Sprawdź, czy proces LanguageTool został wykluczony
__KOD_BLOKU_1__