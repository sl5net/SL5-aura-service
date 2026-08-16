# Integracja Trino — Przewodnik programisty

## Architektura
Interfejsy Aury:
mowa → INTERFEJS=mowa (domyślny powrót w .py)
terminal → INTERFEJS=terminal (jawnie w s() zshrc)
web → INTERFACE=web (jawnie w start_service)
↓
aura_state.py ← API wysokiego poziomu dla programistów
↓
trino_client.py ← operacje na bazach danych niskiego poziomu
↓
Katalog pamięci Trino
memory.aura.features ← włączanie/wyłączanie tłumaczenia na interfejs
memory.aura.translation_state ← język docelowy na interfejs

## Konfiguracja lokalna

### 1. Okno dokowane

__KOD_BLOKU_0__

### 2. Klient Pythona

__KOD_BLOKU_1__

### 3. Inicjalizacja DB (wywoływana automatycznie przy uruchomieniu Aury)

__KOD_BLOKU_2__

## API programisty — aura_state.py

__KOD_BLOKU_3__

## Interfejs administratora

http://localhost:8084

Start:
__KOD_BLOKU_4__

## Interfejs użytkownika Trino (monitor zapytań)

http://localhost:8083/ui/

skrypty/py/func/db/
├── init.py
├── trino_client.py ← niski poziom: pobierz/ustaw stan_funkcji, język_docelowy
├── init_trino_db.py ← uruchomienie: uruchomienie Dockera + schemat + tabele
└── aura_state.py ← API wysokiego poziomu dla programistów
skrypty/py/chat/
└── streamlit-admin.py ← Interfejs administratora na porcie 8084


## Plan działania

- [x] Trino działające w Dockerze
- [x] Klient Pythona podłączony
- [x] DB zainicjowany przy uruchomieniu Aury
- [x] Stan tłumaczenia obsługujący interfejs
- [x] Sieć (Streamlit) oddzielona od mowy/terminalu
- [x] Interfejs administratora na porcie 8084
- [ ] terminal i mowa w pełni niezależne
- [ ] Zastąpienia specyficzne dla użytkownika (wielu użytkowników)
- [ ] Pamięć trwała (wymień katalog pamięci)