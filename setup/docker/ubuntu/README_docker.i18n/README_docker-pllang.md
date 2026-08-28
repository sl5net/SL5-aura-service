docker build -t stt-service .

docker run -it --rm --name stt-container stt-service

docker exec stt-container touch /tmp/sl5_record.trigger


Próba konteneryzacji aplikacji za pomocą Dockera to fantastyczny „wymyślny” krok. To najlepszy sposób na rozwiązanie problemu „działa na moim komputerze” poprzez spakowanie aplikacji i wszystkich jej zależności w jeden, przenośny obraz.

Jednakże napotkamy kilka podstawowych wyzwań, ponieważ ta aplikacja jest zaprojektowana do interakcji z pulpitem hosta (dźwięk, klawiatura). Jest to coś, czemu Docker ma wyraźnie * zapobiegać*.

### Jak zbudować i uruchomić obraz Dockera

1. **Stwórz obraz:** Otwórz terminal w katalogu głównym projektu i uruchom:
__KOD_BLOKU_0__
2. **Uruchom kontener:**
__KOD_BLOKU_1__

### Wynik: co działa, a co (krytycznie) nie

Przy odrobinie szczęścia kontener zostanie zbudowany i uruchomiony. Powinieneś zobaczyć wynik dziennika z `aura_engine.py` wskazujący, że został uruchomiony, załadował modele i teraz czeka.

**To częściowy sukces!** Podstawowa aplikacja Pythona i jej zależności działają w doskonale izolowanym środowisku.

**JEDNAK aplikacja jest teraz zasadniczo uszkodzona ze względu na projekt Dockera:**

1. **Brak dostępu do mikrofonu:** Kontener jest odizolowany od sprzętu hosta. Biblioteka `sounddevice` zakończy się niepowodzeniem przy próbie znalezienia urządzenia wejściowego.
* *Rozwiązanie (tylko Linux):* Możesz spróbować zamontować urządzenie dźwiękowe hosta w kontenerze, dodając `--device /dev/snd` do polecenia `docker run`. Jest to złożone i specyficzne dla hosta.

2. **Brak wyników wpisywania (`xdotool`):** Kontener nie ma dostępu do środowiska graficznego ani okien Twojego hosta. Nie może „wpisywać” tekstu do innej aplikacji. Ta funkcjonalność jest całkowicie zepsuta z założenia.

3. **Brak powiadomień na pulpicie („powiadom-wyślij”):** Tak jak powyżej. Kontener nie może wysyłać powiadomień na pulpit Twojego hosta.

4. **Brak wyzwalacza pliku (`inotify`):** Wyzwalacz pliku oparty na `inotify` nie będzie działał zgodnie z oczekiwaniami. Nie można po prostu „dotknąć /tmp/sl5_record.trigger” na komputerze głównym. Aby utworzyć plik *wewnątrz* działającego kontenera, musiałbyś użyć osobnego polecenia:
__KOD_BLOKU_2__

### Wniosek: „Wymyślny”, ale zasadniczo niezgodny

Utworzenie tego pliku Dockerfile dowodzi, że **podstawowa logika** aplikacji może zostać spakowana. Jednak dowodzi to również, że obecny projekt aplikacji – opierający się na bezpośredniej interakcji sprzętu (mikrofon) i komputera stacjonarnego (pisanie, powiadomienia) – jest **zasadniczo niezgodny z konteneryzacją.**

Aby to naprawdę działało w Dockerze, aplikacja musiałaby zostać przeprojektowana:
* Zamiast słuchać lokalnego mikrofonu, musiałby akceptować strumień audio przez sieć (np. Za pośrednictwem internetowego interfejsu API).
* Zamiast wpisywać tekst za pomocą `xdotool`, konieczne byłoby zwrócenie transkrybowanego tekstu za pośrednictwem tego samego internetowego interfejsu API.