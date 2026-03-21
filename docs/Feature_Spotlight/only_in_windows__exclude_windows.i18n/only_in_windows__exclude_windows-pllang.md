# Atrybuty reguły: `only_in_windows` i `exclude_windows`

Te dwa atrybuty kontrolują **w których aktywnych oknach reguła może zostać uruchomiona**.
Są one zdefiniowane w dyktacie „opcji” reguły i akceptują **listę wzorców wyrażeń regularnych**
które są dopasowane do bieżącego aktywnego tytułu okna (`_active_window_title`).

---

## `tylko_w_oknach`

Reguła uruchamia się **tylko wtedy, gdy** tytuł aktywnego okna pasuje do **co najmniej jednego** z podanych wzorców.
Wszystkie pozostałe okna są ignorowane.

**Przykład użycia:** Ogranicz regułę do określonej aplikacji.


> Reguła zostanie uruchomiona **tylko**, gdy aktywnym oknem będzie Firefox lub Chromium.

---

## `wyklucz_okna`

Reguła zostanie uruchomiona, **chyba że** tytuł aktywnego okna pasuje do **co najmniej jednego** z podanych wzorców.
Pasujące okna są pomijane.

**Przypadek użycia:** wyłącz regułę dla określonych aplikacji.

Przykłady

__KOD_BLOKU_0__



Dopasowywanie **nie uwzględnia wielkości liter** i wykorzystuje **wyrażenia regularne** języka Python.

---

## Streszczenie

| Atrybut | Pali, gdy... |
|--------------------------------|--------------------------------------------|
| `tylko_w_oknach` | tytuł okna **pasuje** do jednego ze wzorców |
| `wyklucz_okna` | tytuł okna **NIE pasuje** do żadnego wzorca |

---

## Zobacz także

- `scripts/py/func/process_text_in_background.py` — linie ~1866 i ~1908
- `scripts/py/func/get_active_window_title.py` — sposób pobierania tytułu okna