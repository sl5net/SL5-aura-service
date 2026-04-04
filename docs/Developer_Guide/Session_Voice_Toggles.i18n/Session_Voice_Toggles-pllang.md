# Obsługa dźwięku sesji i przełączanie głosu

Aura implementuje pętlę przetwarzania dźwięku opartą na sesji. Polecenia głosowe do zarządzania stanem są aktywne tylko w ramach ustanowionej sesji nagrywania.

## Konfiguracja
Zachowanie wewnętrzne sesji jest kontrolowane przez:
`ENABLE_WAKE_WORD = Prawda/Fałsz` (w `config/settings.py`)

## Logika operacyjna
W przeciwieństwie do stałego słuchacza w tle, silnik STT (Vosk) Aury przetwarza dźwięk tylko wtedy, gdy sesja nagrywania została wyzwolona zewnętrznie (np. za pomocą klawisza skrótu).

### Przełącznik w trakcie sesji („Teleskop”)
Gdy `ENABLE_WAKE_WORD` jest ustawione na **True**:
1. **Wyzwalacz:** Użytkownik rozpoczyna sesję ręcznie.
2. **Przełączanie:** Wypowiedzenie „Teleskop” podczas sesji przełącza pomiędzy stanami **AKTYWNY** i **ZAWIESZONY**.
3. **Zachowanie:** Umożliwia użytkownikowi „wstrzymanie” i „wznowienie” przetwarzania tekstu za pomocą poleceń głosowych bez przerywania strumienia audio.

### Prywatność i wydajność
Gdy `ENABLE_WAKE_WORD` jest ustawione na **False** (domyślnie):
- **Tłumienie STT:** W stanie zawieszenia wywołania `AcceptWaveform` i `PartialResult` są całkowicie pomijane.
- **Prywatność:** Żadne dane audio nie są analizowane, chyba że system jest w wyraźnie aktywnym stanie.
- **Zarządzanie zasobami:** użycie procesora jest zminimalizowane poprzez pominięcie analizy sieci neuronowej podczas zawieszenia.

## Opóźnienie i wydajność
- **Natychmiastowe wznowienie:** Ponieważ „RawInputStream” pozostaje otwarty przez całą sesję, przełączenie z ZAWIESZONEGO z powrotem na AKTYWNE powoduje **dodatkowe opóźnienie 0 ms**.
- **Czas pętli:** Pętla przetwarzania działa z interwałem ~100 ms („q.get(timeout=0.1)”), zapewniając niemal natychmiastowy czas reakcji.