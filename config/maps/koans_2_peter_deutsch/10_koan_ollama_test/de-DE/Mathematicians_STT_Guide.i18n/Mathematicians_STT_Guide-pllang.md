# Znani matematycy - Przewodnik po korekcie STT

## Problem

Systemy rozpoznawania mowy (STT), takie jak Vosk, często błędnie słyszą lub błędnie zapisują nazwiska znanych matematyków.
Jest to szczególnie częste w przypadku niemieckich nazw zawierających znaki specjalne (ß, ü, ä, ö)
lub nazwy zapożyczone z innych języków.

## Typowe błędy STT

| Wypowiedź mówiona/STT | Poprawna pisownia | Notatki |
|---|---|---|
| gaus, gaus | Gauß | Niemiecki matematyk, ß często brak |
| olejarka, olejarka | Eulera | Szwajcar, imię po niemiecku brzmi jak „olejarka” |
| leibnitz, lipnitz | Leibniza | z na końcu, typowy błąd ortograficzny |
| Riman, Riemann | Riemanna | podwójne n często pomijane |
| hilberta | Hilberta | zwykle poprawne, tylko wielkie litery |
| kantor | Kantor | zwykle poprawne, tylko wielkie litery |
| poincare, poincare | Poincaré | często brakuje akcentu |
| noether, nöter | Nic | umlaut często pomijany |

## Przykładowe zasady

__KOD_BLOKU_0__

## Dlaczego narzędzie do nauki języków obcych?

Te poprawki powinny nastąpić w `FUZZY_MAP_pre.py` (przed LanguageTool),
ponieważ LanguageTool może „poprawić” błędnie wpisaną nazwę na inne niewłaściwe słowo.
Lepiej najpierw to naprawić, a potem pozwolić LanguageTool sprawdzić gramatykę.

## Testowanie

Po dodaniu reguły przetestuj z konsolą Aura:
__KOD_BLOKU_1__
Oczekiwane: „Euler hat die Formel e hoch i pi plus eins gleich null bewiesen”