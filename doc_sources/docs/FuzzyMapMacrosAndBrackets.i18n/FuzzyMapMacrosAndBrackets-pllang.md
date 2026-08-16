# Rozmyte makra mapy i logika nawiasów

Aura obsługuje grupowanie wielu reguł przetwarzania wstępnego w plikach `FUZZY_MAP_pre.py` w celu wykonania ich sekwencyjnie w spójny potok po uruchomieniu „Reguły początkowej”. W tym dokumencie opisano filozofię projektowania, składnię i przebieg wykonywania tej funkcji.

## Podstawowe zasady projektowania

1. **Zero redundancji**: Reguły wewnątrz grupy pozostają standardowymi krotkami Pythona:
`('tekst_zastępczy', r'wzorzec_regex', próg, flagi_i_opcje)`
2. **Podwójna użyteczność**: Poszczególne reguły w grupie są w pełni funkcjonalnymi, samodzielnymi regułami. Jeśli grupa nie zostanie wyzwolona, są one normalnie oceniane w pętli nadrzędnej.
3. **Pasywny znacznik końca**: Koniec grupy jest zdefiniowany przez pasywny wpis reguły, który nigdy nie jest dopasowywany samodzielnie. Działa wyłącznie jako znacznik granic dla parsera.
4. **Hybrydowy powrót awaryjny (dołączanie przy braku dopasowania)**: Gdy grupa jest aktywna, każda wewnętrzna reguła musi mieć wpływ na wynik. Jeśli wyrażenie regularne reguły wewnętrznej pasuje do tekstu, następuje normalne podstawienie. Jeśli nie pasuje, tekst zastępczy jest dołączany do bieżącego tekstu ze spacją.

---

## Składnia i struktura

Grupę makr definiuje się poprzez zawinięcie serii standardowych reguł pomiędzy **Regułą początkową** i **Regułą końcową** w pliku `FUZZY_MAP_pre.py`.

### 1. Zasada startu
Reguła początkowa to standardowa reguła, która po dopasowaniu uruchamia makro. Zawiera klucz „group_start” w swoim słowniku opcji:
__KOD_BLOKU_0__

### 2. Zasady wewnętrzne
Zasady wewnętrzne to standardowe zasady umieszczane sekwencyjnie po regule początkowej. Nie wymagają żadnych specjalnych metadanych:
__KOD_BLOKU_1__

### 3. Zasada końcowa (znacznik pasywny)
Reguła końcowa ma zamiennik „Brak”, pusty wzorzec i klucz „koniec_grupy” w swoim słowniku opcji:
__KOD_BLOKU_2__

---

## Konkretny przykład

Oto praktyczny przypadek testowy zdefiniowany w pliku `FUZZY_MAP_pre.py`:

__KOD_BLOKU_3__

### Scenariusze przebiegu wykonania:

* **Scenariusz A (makro wyzwalane)**:
* Dane wejściowe: `"uruchom piaskownicę mit apfel"`
* Oczekiwany przepływ:
1. Reguła startowa dopasowuje `"start sandbox"` i zastępuje ją `"Sandbox:"` -> bieżący tekst: `"Sandbox: mit apfel"`.
2. Uruchamiana jest grupa ``test_sandbox'`.
3. Uruchamiamy rekurencyjnie wewnętrzne reguły w ``Sandbox: mit apfel'`:
- Wewnętrzna reguła 1 pasuje do ``apfel'' i zastępuje ``birne'` -> bieżący tekst: ``Piaskownica: mit birne'`.
- Wewnętrzna zasada 2 nie pasuje do „banana”. Ponieważ grupa jest aktywna, powraca do dodawania `"banane"` -> Bieżący tekst: `"Sandbox: mit birne banane"`.
4. Ostateczny tekst ``Sandbox: mit birne banane'` został zwrócony i poprawiony przez LanguageTool.
* Dane wyjściowe: ``Piaskownica: mit Birne Banane'`

* **Scenariusz B (Makro niewywołane – podwójna użyteczność)**:
* Dane wejściowe: `"ein apfel und eine kirsche"`
* Oczekiwany przepływ:
1. Zasada startu nie pasuje. Grupa ``sandbox_test'` pozostaje nieaktywna.
2. Pętla przechodzi do następnej reguły.
3. **Zasada wewnętrzna 1**: Dopasowuje „apfel” i zastępuje je „birne”` -> Bieżący tekst: „ein birne und eine kirsche””.
4. **Zasada wewnętrzna 2**: Nie pasuje. Ponieważ grupa nie została uruchomiona, reguła zachowuje się jak zwykła samodzielna reguła i **nic nie jest dołączane**.
5. Reguła końcowa jest ignorowana.
* Wynik: `„ein birne und eine kirsche”`

---

## Szczegóły techniczne (pod maską)

* **Izolowana rekursja**: Kiedy grupa jest wyzwalana, silnik rekurencyjnie wywołuje `process_text_in_background` z `custom_rules=[inner_rule]`. Dzięki temu każda reguła wewnętrzna może zostać wykonana w ramach pełnego, synchronicznego przebiegu potoku.
* **Zabezpieczenia wydajności i stabilności**:
* **Ominięcie sekwencji**: Wewnętrzne przebiegi rekurencyjne omijają kolejkę sekwencji `chunk_id`, aby zapobiec zakleszczeniom i opóźnieniom w wykonywaniu.
* **Tłumienie wejść/wyjść i TTS**: Przebiegi rekurencyjne tłumią pośrednie zapisywanie plików i wyjścia mowy TTS, zapewniając, że pisany i wypowiadany jest tylko końcowy, ustabilizowany tekst.
* **Zabezpieczenie stabilności**: Przebiegi rekurencyjne są ściśle przerywane po jednej iteracji, aby zapobiec nieskończonym pętlom stabilności podczas dołączania awaryjnego.
* **Bezpieczne zakończenie**: Kontrola stabilności opiera się wyłącznie na maksymalnej liczbie iteracji („MAX_ITERATIONS_FOR_SAFETY”), aby zapobiec nieskończonym pętlom i ominąć ograniczanie oparte na czasie, które mogłoby przedwcześnie przerwać prawidłowe, wolniejsze wykonania makr.
__KOD_BLOKU_4__