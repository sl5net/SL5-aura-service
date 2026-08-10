# PRZEGLĄD FUNKCJI: Zastępowanie reguł opartych na plikach

W tym dokumencie opisano, jak przechowywać wrażliwe wartości (hasła, klucze API, tokeny)
z kodu źródłowego `FUZZY_MAP_pre` / `FUZZY_MAP` i historii Git, ładując
„zastępowanie” tekstu z osobnego pliku w czasie wykonywania, zamiast kodowania go na stałe.

Jest to szczególnie przydatne podczas transmisji na żywo lub udostępniania ekranu, gdy mapa jest wyświetlana
Sam kod źródłowy może być widoczny, ale plik, do którego się odwołuje, nie.

---

## 1. Koncepcja

Zwykle pole „zastępowania” reguły jest dosłownym tekstem wyjściowym:

__KOD_BLOKU_0__

Po włączeniu zastępowania na podstawie plików wartość „zastępowania” rozpoczynająca się od a
skonfigurowany prefiks (domyślnie `-` lub `.`) jest zamiast tego traktowany jako **nazwa pliku**.
Aura rozpoznaje tę nazwę pliku w odniesieniu do własnego katalogu wtyczki, odczytuje jego
treści i używa tej treści jako tekstu zastępczego.

__KOD_BLOKU_1__

Jeśli plik „api_key.txt” istnieje obok pliku „FUZZY_MAP_pre.py” wtyczki, jego (usunięty)
zawartość jest używana jako zamiennik. Jeśli plik nie istnieje, literał
Zamiast tego zwracany jest ciąg `-api_key.txt` (bezpieczny w przypadku awarii: brak przypadkowego wycieku
„nie znaleziono pliku” jako użyteczny tekst i bez awarii).

---

## 2. Ustawienia

Skonfigurowany w `config/settings.py` (lub `config/settings_local.py` dla lokalnego
zastępuje):

| Ustawienie | Wpisz | Domyślne | Opis |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | `Prawda` | Przełącznik główny dla całej funkcji. Jeśli „Fałsz”, „zastąpienie” jest zawsze używane dosłownie. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `krotka[str]` | `('-', '.')` | Wartości „zastępcze” muszą zaczynać się od jednego z tych przedrostków, aby uruchomić wyszukiwanie pliku. Pusty/`Brak` = każda wartość nie rozpoczynająca się od litery jest traktowana jako potencjalna nazwa pliku. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | `Fałsz` | Jeśli `True`, umożliwia rozpoznawanie plików poza własnym katalogiem wtyczki (np. ścieżki bezwzględne lub sekwencje `../`). Zobacz sekcję Bezpieczeństwo poniżej. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `krotka[str]` | np. `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Program Files')` | Rozwiązane ścieżki bezwzględne rozpoczynające się od którejkolwiek z nich są **zawsze** odrzucane, niezależnie od `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`. Twarda granica bezpieczeństwa względem katalogów systemowych. |

---

## 3. Rozdzielczość ścieżki

Plik jest rozwiązywany w następujący sposób:

1. Ścieżka_źródłowa wtyczki (zapisywana automatycznie przez moduł ładujący mapy) to
połączone z `SL5NET_AURA_PROJECT_ROOT` (czytane z `SL5NET_AURA_PROJECT_ROOT`
zmienna środowiskowa), aby uzyskać katalog wtyczki.
2. Wartość „zamienna” jest dołączana do tego katalogu.
3. Jeśli „FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL” nie ma wartości „True”, rozwiązana ścieżka
musi pozostać w katalogu wtyczki, w przeciwnym razie wyszukiwanie zostanie odrzucone.
4. Niezależnie od powyższego, dowolna wyznaczona ścieżka rozpoczynająca się od wpisu w
`FILE4REPLACEMENT_DENY_PREFIXES` jest zawsze odrzucany.
5. Jeśli plik istnieje, zwracana jest jego usunięta zawartość. W przeciwnym razie
oryginalny ciąg „zastępczy” jest zwracany bez zmian.

---

## 4. Uwagi dotyczące bezpieczeństwa

- Włącz opcję „FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL” tylko wtedy, gdy rozumiesz
implikacje: pozwala każdemu użytkownikowi, który może edytować plik `FUZZY_MAP_pre` (np.
za pośrednictwem edytora map online), aby odczytać dowolne pliki, które może wykonać proces Aura
dostęp i wyświetlanie ich zawartości jako tekstu wyjściowego na żywo.
- `FILE4REPLACEMENT_DENY_PREFIXES` zapewnia podstawową ochronę przed
wspólne katalogi systemowe, nawet jeśli dozwolone jest przechodzenie ścieżek, ale tak jest
nie zastępuje przede wszystkim ograniczania tego, kto może edytować pliki map.
- Pliki odniesienia są zwykłym tekstem na dysku. Połącz z plikiem swojego systemu operacyjnego
uprawnienia, jeśli treść jest poufna.

---

## 5. Przykład

Zobacz `config/maps/plugins/TEST_FILE4REPLACEMENT/`, aby zapoznać się z działającą przykładową wtyczką,
i `tools/tests/TEST_FILE4REPLACEMENT.sh` dla skryptu testowego, który ćwiczy
zarówno wyszukiwanie w katalogu, jak i wyszukiwanie poza katalogiem wtyczki.

__KOD_BLOKU_2__

Następnie utwórz plik .Zebra.txt obok tego pliku z żądanym tekstem zastępczym
powiedz (lub wpisz przez konsolę) „Zebra”, aby ją uruchomić.