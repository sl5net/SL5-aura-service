# 🧠 SL5 Aura: Zaawansowana integracja LLM offline

**Stan:** Gotowy do produkcji
**Silnik:** Ollama (Lama 3.2 3B)
**Opóźnienie:** Natychmiastowe (<0,1 s przy trafieniu w pamięć podręczną) / ~20 s (generowanie na procesorze)

## 1. Filozofia „architekta i stażysty”.
Aura działa w oparciu o model hybrydowy, aby zrównoważyć **precyzję** i **elastyczność**:
* **Architekt (RegEx/Python):** Deterministyczne, natychmiastowe wykonanie poleceń systemowych (np. „Otwórz przeglądarkę”, „Zwiększ głośność”).
* **Stażysta (lokalny LLM):** Obsługuje niejasne zapytania, podsumowania i wiedzę ogólną. Jest uruchamiany tylko wtedy, gdy nie zastosowano ścisłych dopasowań reguł ani określonych słów kluczowych.

---

## 2. Architektura wydajności

Aby lokalny LLM mógł być używany na standardowych procesorach bez akceleracji GPU, wdrożyliśmy **3-warstwową strategię wydajności**:

### Warstwa 1: „Tryb natychmiastowy” (słowa kluczowe)
* **Wyzwalacz:** Słowa takie jak „Natychmiastowy”, „Schnell”, „Sofort”.
* **Logika:** Całkowicie omija LLM. Porównuje słowa kluczowe wprowadzone przez użytkownika z lokalną bazą danych SQLite przy użyciu przecięcia zestawu.
* **Opóźnienie:** **< 0,05 s**

### Warstwa 2: Inteligentna pamięć podręczna (SQLite)
* **Logika:** każdy monit jest zaszyfrowany (SHA256). Zanim zapytamy Ollamę, sprawdzamy plik `llm_cache.db`.
* **Funkcja „Aktywna odmiana”:** Nawet jeśli istnieje trafienie w pamięci podręcznej, system czasami (20% szans) generuje *nowy* wariant, aby nauczyć się różnych sformułowań tego samego pytania. W idealnym przypadku przechowujemy ~5 wariantów na pytanie.
* **Funkcja „Hashing semantyczny”:** W przypadku długich pytań (> 50 znaków) używamy LLM do wyodrębnienia najpierw słów kluczowych (np. „przewodnik instalacji”) i zahaszowania ich zamiast pełnego zdania. Pasuje do pytania „Jak zainstalować?” z komunikatem „Proszę o instrukcję instalacji”.
* **Opóźnienie:** **~0,1 s**

### Warstwa 3: Generacja interfejsu API (awaryjna)
* **Logika:** Jeśli nie istnieje pamięć podręczna, wywołujemy API Ollama (`http://localhost:11434/api/generate`).
* **Optymalizacja:**
* **Twarde limity:** `num_predict=60` wymusza zatrzymanie modelu po ~40 słowach.
* **Potoki wejściowe:** Duże teksty (README) są przesyłane przez STDIN, aby uniknąć limitów argumentów systemu operacyjnego.
* **Opóźnienie:** **~15-25 s** (zależne od procesora)

---

## 3. Uziemienie systemu (antyhalucynacja)

Ogólne LLM mają tendencję do wymyślania elementów GUI (przyciski, menu). Wstrzykujemy ścisły **`AURA_TECH_PROFILE`** do każdego monitu systemowego:

1. **Brak GUI:** Aura to bezgłowa usługa CLI.
2. **Brak plików konfiguracyjnych:** Logika to kod Pythona, a nie `.json`/`.xml`.
3. **Wyzwalacze:** Kontrola zewnętrzna działa poprzez tworzenie plików („touch /tmp/sl5_record.trigger”), a nie API.
4. **Instalacja:** Trwa 10-20 minut ze względu na pobranie modelu o pojemności 4 GB (zapobiega kłamstwom „Instaluje się w 3 sekundy”).

---

## 4. Most schowka (bezpieczeństwo systemu Linux)

Usługi działające w tle (systemd) nie mogą uzyskać bezpośredniego dostępu do schowka X11/Wayland ze względu na izolację zabezpieczeń.
* **Rozwiązanie:** Skrypt sesji użytkownika (`clipboard_bridge.sh`) odzwierciedla zawartość schowka do pliku na dysku RAM (`/tmp/aura_clipboard.txt`).
* **Aura:** Odczytuje ten plik, pomijając wszystkie problemy z uprawnieniami.

---

## 5. Samokształcenie (ogrzewanie pamięci podręcznej)

Udostępniamy skrypt `warm_up_cache.py`.
1. Odczytuje projekt `README.md`.
2. Prosi LLM o wymyślenie prawdopodobnych pytań użytkowników na temat projektu.
3. Symuluje te pytania względem Aury, aby wstępnie wypełnić bazę danych.