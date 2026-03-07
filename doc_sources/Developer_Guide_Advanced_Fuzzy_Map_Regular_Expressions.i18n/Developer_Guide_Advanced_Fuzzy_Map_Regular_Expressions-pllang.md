## Przewodnik programisty: Zaawansowane wyrażenia regularne mapy rozmytej

System Fuzzy Mapping wykorzystuje standardowe wyrażenia regularne Pythona, umożliwiając tworzenie skutecznych wzorców dopasowywania i wykluczania, w szczególności poprzez **Negative Lookaheads (`(?!...)`)**.

### Używanie negatywnych przewidywań do umieszczania na białej liście

Ten wzorzec pozwala zdefiniować regułę mającą zastosowanie do **wszystkiego Z WYJĄTKIEM** określonej listy słów lub wyrażeń. Jest to szczególnie przydatne w połączeniu ze wzorcem „empty_all” do tworzenia skumulowanych, ograniczonych zestawów reguł.

| Cel | Przykładowa reguła (`FUZZY_MAP`) | Wyjaśnienie |
| :--- | :--- | :--- |
| **Zastosuj do wszystkich z wyjątkiem jednego słowa** | `('', r'^(?!Haus).*$', 5, {'flagi': re.IGNORECASE})` | Ta reguła zastosuje zamianę (lub pominie logikę, tutaj ``'`) do **dowolnego tekstu**, który *nie* jest dokładnie „Haus”. `(?!Haus)` to negatywne spojrzenie naprzód, gwarantujące, że tekst nie zaczyna się od „Haus”. |
| **Zastosuj do wszystkich z wyjątkiem wielu słów** | `('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flagi': re.IGNORECASE})` | Ta zasada dotyczy **wszystko**, co nie zaczyna się od „Schach”, „Matt”, „bad” lub „Haus”. Użyj potoku OR (`|`) w grupie lookahead `(?!...)`, aby umieścić wiele terminów na białej liście. |

***

### Używanie pozytywnych przewidywań w przypadku ograniczonych reguł

Standardowe podejście wykorzystuje pozytywne przewidywania lub proste grupy przechwytujące, aby ograniczyć regułę do *tylko* określonej listy słów.

| Cel | Przykładowa reguła (`FUZZY_MAP`) | Wyjaśnienie |
| :--- | :--- | :--- |
| **Zastosuj tylko do określonej listy** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flagi': re.IGNORECASE})` | Ta zasada ma zastosowanie tylko wtedy, gdy tekst zaczyna się od jednego z wymienionych słów (Schach, Matt, bad lub Haus). Dopasowany tekst jest następnie zastępowany wartością docelową („Schachmatt”) w oparciu o próg. |