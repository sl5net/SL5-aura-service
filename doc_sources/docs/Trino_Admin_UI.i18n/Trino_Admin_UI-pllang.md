# Interfejs administratora Aury

Interfejs administratora pozwala przeglądać i zmieniać ustawienia Aury w przeglądarce przy zerowym koszcie bezczynnych zasobów. Serwer panelu kontrolnego nie działa podczas rozruchu; jest uruchamiany na żądanie, tylko na żądanie.

## Jak otworzyć (na żądanie)

Panel administracyjny można uruchamiać i otwierać dynamicznie, korzystając z dowolnej z następujących trzech metod:

### 1. Polecenie głosowe
Po prostu mów do mikrofonu:
* *"administracja aurą"

### 2. Polecenie terminala/konsoli
Jeśli pracujesz w terminalu, uruchom to polecenie, aby bezpośrednio uruchomić program uruchamiający:
__KOD_BLOKU_0__

*⚠️ **Uwaga dotycząca platformy dla użytkowników systemu Windows/macOS:** Opakowanie poleceń w postaci krótkiej litery „s” jest skonfigurowane głównie dla środowisk Linux. Przeczytaj w tym celu dokument. Jeśli używasz systemu Windows lub macOS, polecenie `s` może nie działać od razu po wyjęciu z pudełka. Zapoznaj się z naszą oficjalną dokumentacją konfiguracyjną CLI, aby dowiedzieć się, jak skonfigurować i wdrożyć alias polecenia `s` w swoim systemie operacyjnym.*


### 3. Skrót na pulpicie
Aby utworzyć ikonę pulpitu specyficzną dla platformy, uruchom raz ten skrypt instalacyjny:
__KOD_BLOKU_1__
Następnie po prostu kliknij dwukrotnie ikonę **Panel administracyjny Aura** na pulpicie.

---

## Bezpośredni dostęp przez przeglądarkę
Po uruchomieniu serwera za pomocą którejkolwiek z powyższych metod na żądanie, w dowolnym momencie możesz uzyskać dostęp do interfejsu bezpośrednio w przeglądarce:

http://localhost:8084

*(Możesz dodać ten link do zakładek w swojej przeglądarce!)*

---

## Co możesz zrobić

- Zobacz status tłumaczenia dla każdego interfejsu (mowa, terminal, internet).
- Włącz lub wyłącz tłumaczenie na interfejs.
- Wybierz język docelowy (angielski, francuski, hiszpański itp.).

## Interfejsy

| Interfejs | Opis |
|----------|--------------------------------------|
| przemówienie | Wejście głosowe (mikrofon) |
| terminal | Wiersz poleceń (polecenie `s`) |
| sieć | Usprawniony czat internetowy (port 8831) |

## Przykład

Aby przetłumaczyć tylko użytkowników sieci na angielski — zostaw mowę i terminal wyłączone, włącz przeglądarkę z językiem „en”.