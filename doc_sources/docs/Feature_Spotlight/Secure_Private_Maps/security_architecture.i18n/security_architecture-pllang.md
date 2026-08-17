# Architektura bezpieczeństwa: ochrona danych prywatnych (7.8.'26 13:22 pt)

Kod źródłowy `service_api.py` implementuje trójwarstwową, wzajemnie niezależną architekturę bezpieczeństwa w celu ochrony prywatnych danych.

## Przegląd

| Warstwa | Mechanizm | Składnik | Cel ochrony |
|-------|-----------|-----------|----------------|
| 1 | Oprogramowanie pośredniczące z regułą podkreślenia | `service_api.py` | Blokuj dostęp do ukrytych ścieżek |
| 2 | Uwierzytelnianie kluczem API | `service_api.py` | Kontrola dostępu do punktów końcowych |
| 3 | Maskowanie prywatności i izolacja pamięci podręcznej | `service_api.py`, `aura_cache.py` | Zaciemnianie danych i separacja pamięci podręcznej |

---

## Warstwa 1: Oprogramowanie pośredniczące z regułą podkreślenia

Wszelkie żądania do ścieżek lub folderów z wiodącym podkreśleniem (takie jak `_privat`) są blokowane przez oprogramowanie pośredniczące za pomocą **HTTP 403 Forbidden**.

**Komunikat o błędzie:**
__KOD_BLOKU_0__

Ta reguła działa na poziomie ścieżki/routowania i uniemożliwia dostęp do katalogów oznaczonych jako prywatne.

---

## Warstwa 2: Uwierzytelnianie za pomocą klucza API

Wszystkie punkty końcowe API są chronione przez `Depends(verify_api_key)`.

Żądania bez prawidłowego nagłówka `X-API-Key` są natychmiast odrzucane, zanim osiągną jakąkolwiek logikę biznesową.

---

## Warstwa 3: Maskowanie prywatności i izolacja pamięci podręcznej

### Maskowanie
W interfejsie API ustawieniem domyślnym jest „unmasked = False”. Wrażliwe dane w odpowiedziach API są zatem automatycznie maskowane.

### Izolacja pamięci podręcznej
Hash `cache_id` w `aura_cache.py` jest oddzielony tytułem aktywnego okna (`_active_window_title`).

**Konsekwencja:** Wpisów pamięci podręcznej utworzonych w terminalu lokalnym nie można odczytać przez API, ponieważ mają one inny skrót `cache_id`.

---

## Streszczenie

Twoje poufne dane w `_privat` są w ten sposób chronione na wszystkich trzech poziomach języka i ścieżki przed nieautoryzowanym dostępem API:

1. **Poziom ścieżki** — Dostęp do folderów `_` jest zablokowany
2. **Poziom uwierzytelnienia** — Dostęp mają tylko ważne klucze API
3. **Poziom danych** — Maskowanie i izolacja pamięci podręcznej zapobiegają eksfiltracji danych