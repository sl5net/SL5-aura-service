# AUDIO_DIAGNOSTICS_EN.md

# Diagnostyka audio systemu Linux dla Aury


### 1. Identyfikacja urządzeń
Lista wszystkich urządzeń audio widzianych przez środowisko Python:
__KOD_BLOKU_0__
* **Na co zwrócić uwagę:** Zanotuj **Numer indeksowy** i **Identyfikator sprzętu (hw:X,Y)** mikrofonu.

### 2. Kto używa sprzętu?
Jeśli pojawi się błąd „Urządzenie zajęte” lub „Przekroczono limit czasu”, sprawdź, który proces (PID) aktualnie blokuje sprzęt audio:
__KOD_BLOKU_1__
* **Wskazówka:** Jeśli widzisz „pipewire” lub „wirehydraulik”, oznacza to, że serwer dźwięku zarządza urządzeniem. Jeśli widzisz PID `python3` lub `obs` bezpośrednio na urządzeniu PCM, mogą one blokować inne.

### 3. Monitorowanie w czasie rzeczywistym (PipeWire)
Jeśli Twój system korzysta z PipeWire (standard we współczesnym Manjaro), jest to najlepsze narzędzie do diagnostyki na żywo:
__KOD_BLOKU_2__
* **Na co zwrócić uwagę:** Sprawdź kolumnę `ERR` pod kątem przerw i sprawdź, czy Aura (16000 Hz) i OBS (48000 Hz) nie powodują przeciążenia procesora podczas ponownego próbkowania.

### 4. Monitorowanie zdarzeń audio
Zobacz aktualizacje na żywo, gdy mikrofony są wyciszone, wyłączone lub utworzone są nowe strumienie:
__KOD_BLOKU_3__
* **Użycie:** Uruchom to, a następnie uruchom Aurę. Jeśli od razu zobaczysz wiele zdarzeń „usuń”, proces ulega awarii lub jest odrzucany.

### 5. Test obejścia sprzętowego
Sprawdź, czy Twój mikrofon działa na surowym poziomie sprzętowym (z pominięciem PulseAudio/PipeWire). Spowoduje to nagranie 5 sekund dźwięku:
__KOD_BLOKU_4__
* **Wynik:** Jeśli to zadziała, ale Aura nie, problem leży w konfiguracji serwera dźwięku, a nie w sprzęcie.

### 6. Reset awaryjny
Jeżeli system audio jest zablokowany:
__KOD_BLOKU_5__


**podpowiedź: łatwiejszy przebieg pracy:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀