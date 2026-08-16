# Poprawka: zniekształcenia dźwięku i zawieszanie się PipeWire (Linux)

W tym dokumencie opisano, jak rozwiązać problem zniekształceń dźwięku („klirren”), artefaktów głosu robotów i zawieszeń dźwięku systemowego, które mogą wystąpić podczas korzystania z usługi **SL5-aura-service** wraz z innymi aplikacjami multimedialnymi, takimi jak OBS, AnyDesk lub strumienie TTS o wysokiej częstotliwości.

## Objawy
- Dźwięki wejściowe/wyjściowe głosu są zniekształcone, metaliczne lub „brzęczą”.
- Dźwięk systemowy zawiesza się i pojawia się komunikat: „Nawiązywanie połączenia z PulseAudio” lub „Proszę czekać”.
- Całkowita utrata dźwięku po dużym obciążeniu procesora lub jednoczesnym korzystaniu ze strumienia.
- Dzienniki dziennika pokazują: `spa.alsa: hw:X: błąd snd_pcm_status: Nie ma takiego urządzenia`.

## Główna przyczyna
W Manjaro i innych nowoczesnych dystrybucjach Linuksa **PipeWire** zarządza dźwiękiem. Zniekształcenie zwykle wynika z:
1. **Niedopełnienie bufora:** Konflikt pomiędzy równoczesnymi strumieniami (np. AnyDesk przechwytujący dźwięk podczas działania TTS/OBS).
2. **Niedopasowanie częstotliwości próbkowania:** Częste przełączanie pomiędzy 44,1 kHz a 48 kHz.
3. **Problemy z synchronizacją USB:** Duże obciążenie magistrali powoduje tymczasowe rozłączenie zestawów słuchawkowych USB (takich jak Plantronics/Poly).

---

## Rozwiązania

### 1. Natychmiastowe przywrócenie (Reset „nuklearny”)
Jeśli stos audio jest zamrożony lub zniekształcony, zakończ wszystkie procesy związane z dźwiękiem. Natychmiast uruchomią się automatycznie.

__KOD_BLOKU_0__

### 2. Ustawienia zapobiegania i stabilności

#### Wyłącz dźwięk AnyDesk
AnyDesk często próbuje podłączyć się do urządzenia audio, powodując konflikty sprzętowe.
- **Działanie:** Otwórz Ustawienia AnyDesk -> **Dźwięk** -> Wyłącz **„Przesyłaj dźwięk”** i **„Odtwórz dźwięk”**.

#### Napraw częstotliwość próbkowania PipeWire (zalecane)
Wymuś, aby PipeWire pozostał na 48 kHz, aby uniknąć artefaktów ponownego próbkowania podczas odtwarzania TTS.

1. Utwórz katalog konfiguracyjny: `mkdir -p ~/.config/pipewire`
2. Skopiuj domyślną konfigurację: `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. Edytuj `~/.config/pipewire/pipewire.conf` i ustaw:
__KOD_BLOKU_1__
4. Uruchom ponownie usługi:
__KOD_BLOKU_2__

---

## 3. Odzyskiwanie poprodukcyjne (FFmpeg)
Jeśli nagrałeś sesję, a dźwięk jest zniekształcony („klirring”), użyj następującego łańcucha filtrów `ffmpeg`, aby naprawić plik.

### Zalecane polecenie naprawy
To polecenie powoduje zastosowanie narzędzia do usuwania obcinania, redukcji szumów i filtra dolnoprzepustowego w celu usunięcia cyfrowych artefaktów o wysokiej częstotliwości bez ponownego kodowania wideo.

przetestowane i bardzo dobre:

__KOD_BLOKU_3__

może lepiej z (nie testowano):

__KOD_BLOKU_4__



nie testowane:
__KOD_BLOKU_5__




**Podział filtrów:**
- `adeclip`: Zaokrągla cyfrowe skoki obcinania.
- `afftdn`: Redukuje szum cyfrowy oparty na FFT.
- `lowpass=f=3500`: Odcina częstotliwości powyżej 3,5 kHz, gdzie występuje najwięcej „klirowania” (sprawia, że głos staje się wyraźniejszy/cieplejszy).
- `volume=1,8`: Kompensuje utratę objętości podczas filtrowania.
- `-c:v copy`: Zachowuje oryginalną jakość wideo (niezwykle szybko).

---

## Narzędzia do debugowania
Aby monitorować stan dźwięku w czasie rzeczywistym podczas programowania:
- `pw-top`: Pokazuje błędy w czasie rzeczywistym (kolumna ERR) i stan bufora.
- `journalctl --user -u pipewire`: Sprawdza, czy sprzęt nie jest rozłączony.