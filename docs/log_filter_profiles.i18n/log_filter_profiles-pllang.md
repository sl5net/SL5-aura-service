# Profile filtrów dziennika

Aktywnym filtrem dziennika jest zawsze `config/filters/settings_local_log_filter.py`.

## Profile

Predefiniowane profile są przechowywane w `config/filters/.backlock/`:

| Profil | Opis |
|---|---|
| `pierwsze_uruchomienie` | Minimalny wynik — tylko błędy i status. Stosowane automatycznie przy pierwszym uruchomieniu. |
| „normalny” | Standardowy filtr do codziennego użytku. |

## Przełącz profil ręcznie

__KOD_BLOKU_0__

## Dodaj niestandardowy profil

1. Utwórz nowy folder w `config/filters/.backlock/my_profile/`
2. Skopiuj do niego istniejący plik `settings_local_log_filter.py` i edytuj go według swoich potrzeb
3. Zastosuj go za pomocą „cp”, jak pokazano powyżej

## Automatyczne przełączanie profili

Przy pierwszym uruchomieniu Aura wykrywa, że katalog `log/` jeszcze nie istnieje i
automatycznie kopiuje profil `first_run` jako aktywny filtr.