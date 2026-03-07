### FAQ (angielski) 3.8.'2025 Niedz

**1. P: Czym jest aura SL5?**
Odp.: Jest to ogólnosystemowy program do zamiany mowy na tekst w trybie offline. Umożliwia dyktowanie w dowolnej aplikacji na komputerze (Windows, macOS, Linux) bez konieczności połączenia z Internetem.

**2. P: Dlaczego powinienem tego używać? Co czyni go wyjątkowym?**
O: **Prywatność.** Twoje dane głosowe są przetwarzane w 100% na Twoim komputerze lokalnym i nigdy nie są wysyłane do chmury. Dzięki temu jest on w pełni prywatny i zgodny z RODO.

**3. P: Czy to jest bezpłatne?**
O: Tak, wersja Community jest całkowicie darmowa i ma otwarte oprogramowanie. Kod i instalator znajdziesz na naszym GitHubie: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. P: Czego potrzebuję, aby z niego korzystać?**
Odp.: Komputer i mikrofon. Aby uzyskać najlepszą dokładność, zdecydowanie zalecamy stosowanie dedykowanego mikrofonu zestawu słuchawkowego zamiast wbudowanego mikrofonu laptopa.

**5. P: Dokładność nie jest doskonała. Jak mogę to ulepszyć?**
Odp.: Staraj się mówić wyraźnie, ze stałą głośnością i tempem. Największą różnicę robi redukcja szumów tła i użycie lepszego mikrofonu.
Personalizacja oprogramowania (zaawansowana moc): Aby uzyskać wyższy poziom dokładności, SL5 Aura wykorzystuje zaawansowaną funkcję zwaną FuzzyMaps. Pomyśl o nich jak o swoim osobistym, inteligentnym słowniku. Możesz tworzyć proste pliki tekstowe z regułami naprawiającymi typowe, powtarzające się błędy rozpoznawania.

Przykład: Jeśli oprogramowanie często słyszy „get hap” zamiast „GitHub”, możesz dodać regułę, która za każdym razem automatycznie to koryguje.

Korzyści: Pozwala to „nauczyć” oprogramowanie określonego żargonu technicznego, nazw produktów, skrótów, a nawet stworzyć zestawy reguł dla unikalnych słowników. Dostosowując te mapy, możesz znacznie poprawić dokładność w konkretnym przypadku użycia.

***

#### **Część 1: Pytania ogólne**

**P: Co to jest SL5 Auro?**
Odp.: SL5 Auro to ogólnosystemowy program do zamiany mowy na tekst w trybie offline. Umożliwia dyktowanie tekstu do dowolnej aplikacji na komputerze (np. klienta poczty e-mail, edytora tekstu, edytora kodu) bez konieczności połączenia z Internetem.

**P: Co oznacza „offline” i dlaczego jest to ważne?**
O: „Offline” oznacza, że całe przetwarzanie głosu odbywa się bezpośrednio na Twoim komputerze. Twoje dane głosowe **nigdy** nie są wysyłane do serwera w chmurze (takiego jak Google, Amazon czy OpenAI). Zapewnia to maksymalną prywatność i bezpieczeństwo, dzięki czemu idealnie nadaje się do przechowywania informacji poufnych (np. dla prawników, lekarzy, dziennikarzy) i jest w pełni zgodny z przepisami o ochronie danych, takimi jak RODO.

**P: Czy to naprawdę jest darmowe? Jaki jest haczyk?**
Odp.: „Wersja społecznościowa” jest w 100% bezpłatna i ma otwarte oprogramowanie. Nie ma żadnego haczyka. Wierzymy w siłę narzędzi open source. Jeśli uznasz oprogramowanie za wartościowe i chcesz wesprzeć jego dalszy rozwój, możesz to zrobić za pośrednictwem naszego [Ko-fi page](https://ko-fi.com/sl5).

**P: Dla kogo jest to oprogramowanie?**
O: Jest przeznaczony dla każdego, kto dużo pisze i chce zwiększyć swoją efektywność: pisarzy, studentów, programistów, prawników i lekarzy, osób z ograniczeniami fizycznymi lub każdego, kto po prostu woli mówić niż pisać.

#### **Część 2: Instalacja i konfiguracja**

**P: Jakie systemy operacyjne są obsługiwane?**
Odp.: Oprogramowanie zostało przetestowane i potwierdzone, że działa w systemach Windows 11, Manjaro Linux, Ubuntu i macOS.

**P: Jak zainstalować go w systemie Windows?**
Odp.: Zapewniamy prosty instalator jednym kliknięciem. Jest to skrypt .Bat, który wymaga uprawnień administratora do skonfigurowania środowiska i pobrania niezbędnych modeli. Po uruchomieniu zajmie się wszystkim za Ciebie.

**P: Plik do pobrania dla modeli jest bardzo duży. Dlaczego?**
Odp.: Modele rozpoznawania mowy umożliwiają oprogramowaniu pracę w trybie offline. Zawierają wszystkie dane niezbędne, aby sztuczna inteligencja zrozumiała Twój język. Większe, bardziej precyzyjne modele mogą mieć rozmiar kilku gigabajtów. Nasz nowy moduł pobierania dzieli je na mniejsze, weryfikowalne części, aby zapewnić niezawodne pobieranie.

** P: Korzystam z Linuksa. Jak wygląda proces?**
O: W systemie Linux zazwyczaj klonujesz repozytorium z GitHuba i uruchamiasz skrypt instalacyjny. Ten skrypt tworzy wirtualne środowisko Python, instaluje zależności i uruchamia usługę dyktowania.

**P: Po dwukrotnym kliknięciu pliku `.py` w systemie Windows otwiera się on w edytorze tekstu. Jak to uruchomić?**
O: Jest to częsty problem w systemie Windows, polegający na tym, że pliki `.py` nie są powiązane z interpreterem Pythona. Nie powinieneś bezpośrednio uruchamiać poszczególnych skryptów Pythona. Zawsze używaj dostarczonego głównego skryptu startowego (np. pliku .bat), ponieważ dzięki temu najpierw zostanie aktywowane odpowiednie środowisko.

#### **Część 3: Użycie i funkcje**

**P: Jak właściwie mogę go używać do dyktowania?**
O: Najpierw uruchamiasz „usługę dyktowania”, uruchamiając odpowiedni skrypt. Będzie działać w tle. Następnie używasz wyzwalacza (takiego jak klawisz skrótu lub dedykowany skrypt), aby rozpocząć i zatrzymać nagrywanie. Rozpoznany tekst zostanie następnie automatycznie wpisany w dowolnym aktualnie aktywnym oknie.

**P: Jak poprawić dokładność?**
O: 1. **Użyj dobrego mikrofonu:** Mikrofon zestawu słuchawkowego jest znacznie lepszy niż mikrofon wbudowany w laptopie. 2. **Zminimalizuj hałas w tle:** Kluczem jest ciche otoczenie. 3. **Mów wyraźnie:** Mów w stałym tempie i głośności. Nie mamrocz i nie spiesz się.
Personalizacja oprogramowania (zaawansowana moc): Aby uzyskać wyższy poziom dokładności, SL5 Auro wykorzystuje zaawansowaną funkcję zwaną FuzzyMaps. Pomyśl o nich jak o swoim osobistym, inteligentnym słowniku. Możesz tworzyć proste pliki tekstowe z regułami naprawiającymi typowe, powtarzające się błędy rozpoznawania.

Przykład: Jeśli oprogramowanie często słyszy „get hap” zamiast „GitHub”, możesz dodać regułę, która za każdym razem automatycznie to koryguje.

Korzyści: Pozwala to „nauczyć” oprogramowanie określonego żargonu technicznego, nazw produktów, skrótów, a nawet stworzyć zestawy reguł dla unikalnych słowników. Dostosowując te mapy, możesz znacznie poprawić dokładność w konkretnym przypadku użycia.

**P: Czy mogę zmieniać języki?**
O: Tak. System obsługuje „przeładowywanie na gorąco” plików konfiguracyjnych na żywo. Możesz zmienić model języka w konfiguracji, a usługa przełączy się na niego natychmiast, bez konieczności ponownego uruchamiania.

**P: Co to jest „LanguageTool”?**
Odp.: LanguageTool to zintegrowany przez nas narzędzie do sprawdzania gramatyki i stylu o otwartym kodzie źródłowym. Gdy Twoja mowa zostanie zamieniona na tekst, LanguageTool automatycznie koryguje typowe błędy w transkrypcji (np. „prawo” vs. „pisz”) i naprawia interpunkcję, znacznie poprawiając wynik końcowy.

#### **Część 4: Rozwiązywanie problemów i wsparcie**

**P: Uruchomiłem usługę, ale nic się nie dzieje, gdy próbuję dyktować.**
Odp.: Sprawdź następujące elementy:
1. Czy usługa nadal działa na Twoim terminalu/konsoli? Poszukaj komunikatów o błędach.
2. Czy mikrofon został prawidłowo wybrany jako domyślne urządzenie wejściowe w systemie operacyjnym?
3. Czy mikrofon jest wyciszony lub czy głośność jest ustawiona zbyt nisko?

** P: Znalazłem błąd lub mam pomysł na nową funkcję. Co mam zrobić?**
Odp.: To świetnie! Najlepszym miejscem do zgłaszania błędów lub sugerowania funkcji jest otwarcie „Problemu” na naszym [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. P: Dokładność nie jest doskonała. Jak mogę to ulepszyć?**
Odp.: Dokładność zależy zarówno od konfiguracji, jak i dostosowania oprogramowania.

* **Twoja konfiguracja (podstawy):** Staraj się mówić wyraźnie, ze stałą głośnością i tempem. Redukcja szumów tła i używanie dobrego mikrofonu zestawu słuchawkowego zamiast wbudowanego mikrofonu laptopa robi ogromną różnicę.

* **Dostosowanie oprogramowania (zaawansowana moc):** Aby uzyskać wyższy poziom dokładności, SL5 Auro wykorzystuje zaawansowaną funkcję zwaną **FuzzyMaps**. Pomyśl o nich jak o swoim osobistym, inteligentnym słowniku. Możesz tworzyć proste pliki tekstowe z regułami naprawiającymi typowe, powtarzające się błędy rozpoznawania.

* **Przykład:** Jeśli oprogramowanie często słyszy „get hap” zamiast „GitHub”, możesz dodać regułę, która za każdym razem automatycznie to koryguje.
* **Korzyść:** Pozwala to „nauczyć” oprogramowanie określonego żargonu technicznego, nazw produktów i skrótów, a nawet stworzyć zestawy reguł dla unikalnych słowników. Dostosowując te mapy, możesz znacznie poprawić dokładność w konkretnym przypadku użycia.




### Głębokie zanurzenie się w architekturze: ciągłe nagrywanie w stylu „Walkie-Talkie”.

Nasza usługa dyktowania wykorzystuje solidną, sterowaną stanem architekturę, aby zapewnić płynne, ciągłe nagrywanie, podobne do używania krótkofalówki. System jest zawsze gotowy do przechwytywania dźwięku, ale przetwarza go tylko po wyraźnym uruchomieniu, zapewniając wysoką responsywność i niskie zużycie zasobów.

Osiąga się to poprzez oddzielenie pętli nasłuchiwania audio od wątku przetwarzającego i zarządzanie stanem systemu za pomocą dwóch kluczowych komponentów: flagi zdarzenia `active_session` i naszego `audio_manager` do sterowania mikrofonem na poziomie systemu operacyjnego.

**Logika maszyny stanowej:**

System działa w ciągłej pętli, zarządzanej za pomocą jednego klawisza skrótu, który przełącza pomiędzy dwoma stanami podstawowymi:

1. **Stan słuchania (domyślny/gotowy):**
* **Warunek:** Flaga `aktywna_sesja` ma wartość `False`.
* **Stan mikrofonu:** Mikrofon jest **wyciszony**, aby „wyłączyć wyciszenie mikrofonu()”. Odbiornik Vosk jest aktywny i oczekuje na wejście audio.
* **Działanie:** Gdy użytkownik naciśnie klawisz skrótu, stan się zmieni. Flaga `aktywna_sesja` jest ustawiona na `True`, sygnalizując rozpoczęcie „prawdziwego” dyktowania.

2. **Stan PRZETWARZANIA (Użytkownik zakończył mówienie):**
* **Warunek:** Użytkownik naciśnie klawisz skrótu, gdy flaga `aktywna_sesja` ma wartość `True`.
* **Stan mikrofonu:** **Pierwsza akcja** polega na natychmiastowym **wyciszeniu** mikrofonu za pomocą `mute_microphone()`. Spowoduje to natychmiastowe zatrzymanie strumienia audio do silnika Vosk.
*   **Działanie:**
* Flaga `active_session` jest ustawiona na `False`.
* Ostatni rozpoznany fragment audio jest pobierany z Voska.
* Wątek przetwarzający zostaje uruchomiony wraz z ostatecznym tekstem.
* Co najważniejsze, w bloku „w końcu” wątek przetwarzający po zakończeniu wykonuje funkcję „unmute_microphone()”.

** „Magia” sygnału wyłączenia wyciszenia: **

Kluczem do niekończącej się pętli jest ostatnie wywołanie `unmute_microphone()`. Po zakończeniu przetwarzania dyktowania „A” i wyłączeniu wyciszenia mikrofonu system automatycznie i natychmiast powraca do stanu **SŁUCHANIE**. Słuchacz Voska, który cierpliwie czekał, natychmiast zaczyna ponownie odbierać dźwięk, gotowy do przechwycenia dyktanda „B”.

Tworzy to wysoce responsywny cykl:
`Naciśnij -> Mów -> Naciśnij -> (Wycisz i przetwarzaj) -> (Włącz wyciszenie i słuchaj)`

Taka architektura zapewnia, że mikrofon jest wyciszony tylko na krótki czas przetwarzania tekstu, dzięki czemu użytkownik czuje, że system działa natychmiastowo, zachowując przy tym solidną kontrolę i zapobiegając niekontrolowanym nagraniom.