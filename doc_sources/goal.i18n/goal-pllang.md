## Cel: model „sesji dyktowania”.

### Unser Ziel (niemiecki): Die „Diktier-Sitzung”

Ein einziger Trigger startet eine **"Diktier-Sitzung"**, die aus drei Phasen besteht:

1. **Faza początkowa (Warten auf Sprache):**
* Nach dem Trigger lauscht das System.
* Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (np. 12 s).

2. **Aktivphase (Kontinuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktywny Modus.
* Immer wenn VOSK eine Sprechpause erkennt und einen Textblockliefert (z.B. einen Satz), wird dieser Block **sofort** zur Verarbeitung (LanguageTool itp.) weitergegeben und als Text ausgegeben.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3. **Faza końcowa (Ende der Sitzung):**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) komplett Still.
* Der Nutzer stoppt die Sitzung manuell per Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Nutzer eine längere Pause macht oder sie manuell bedet.


### **Cel: model „sesji dyktowania”**

Pojedynczy wyzwalacz inicjuje **„Sesję dyktowania”**, która składa się z trzech faz:
1. **Faza uruchamiania (oczekiwanie na mowę):**
* Po uruchomieniu system rozpoczyna nasłuchiwanie.
* Jeśli **nie zostanie wykryta mowa**, cała sesja zakończy się po upływie `PRE_RECORDING_TIMEOUT` (np. 12 s).
2. **Faza aktywna (dyktowanie ciągłe):**
* Po wykryciu pierwszego wejścia głosowego sesja przełącza się w tryb aktywny.
* Ilekroć VOSK wykryje pauzę i dostarczy fragment tekstu (np. zdanie), fragment ten jest **natychmiast** przekazywany do potoku przetwarzania (LanguageTool itp.) i wyprowadzany jako tekst.
* Nagranie trwa **płynnie** w tle w oczekiwaniu na następną wypowiedź.
3. **Faza zakończenia (zakończenie sesji):**
* Cała sesja kończy się dopiero po spełnieniu jednego z dwóch warunków:
* Użytkownik pozostaje całkowicie cichy przez czas `SPEECH_PAUSE_TIMEOUT` (np. 1-2 s).
* Użytkownik ręcznie zatrzymuje sesję za pomocą wyzwalacza.
**W skrócie:** Jedna sesja, wiele natychmiastowych wyników tekstowych. Sesja pozostaje aktywna do czasu, aż użytkownik zrobi długą pauzę lub ręcznie ją zakończy.