# 🧠 Tryb hybrydowy SL5 Aura: lokalna integracja LLM i schowka

**Stan:** Stabilny
**Technologia:** Ollama (Llama 3.2) + architektura File Bridge
**Prywatność:** 100% offline

## Koncepcja: „Architekt i stażysta”

Tradycyjnie Aura opiera się na regułach deterministycznych (RegEx) – szybko i precyzyjnie. To jest **„Architekt”**.
**Lokalna wtyczka LLM** pełni funkcję **„Stażysty”**: obsługuje niejasne żądania, podsumowuje teksty i odpowiada na ogólne pytania.

## 🛠 Architektura: Most schowka

Ze względu na ograniczenia bezpieczeństwa w systemie Linux (Wayland/X11) procesy działające w tle (takie jak Aura) często nie mogą uzyskać bezpośredniego dostępu do schowka. Rozwiązaliśmy ten problem za pomocą **architektury mostowej**:

1. **Dostawca (sesja użytkownika):** W sesji użytkownika uruchamiany jest mały skrypt powłoki (`clipboard_bridge.sh`). Obserwuje schowek i kopiuje jego zawartość do pliku tymczasowego (`/tmp/aura_clipboard.txt`).
2. **Konsument (Aura):** Wtyczka Pythona odczytuje ten plik. Ponieważ dostęp do plików jest uniwersalny, pomijane są problemy z uprawnieniami.

---

## 🚀 Przewodnik konfiguracji

### 1. Zainstaluj Ollamę
__KOD_BLOKU_0__

### 2. Skonfiguruj skrypt mostu
Utwórz plik `~/clipboard_bridge.sh` i uczyń go wykonywalnym:

__KOD_BLOKU_1__

**Ważne:** Dodaj ten skrypt do autostartu systemu!

### 3. Logika wtyczki (`ask_ollama.py`)

Skrypt znajduje się w `config/maps/plugins/z_fallback_llm/de-DE/`.
* **Wyzwalacz:** Wykrywa słowa takie jak „Komputer”, „Aura”, „Schowek”, „Podsumowanie”.
* **Pamięć:** Przechowuje plik `conversation_history.json` w celu zapamiętania kontekstu (np. „O co ja właśnie zapytałem?”).
* **Szybka inżynieria:** nadaje priorytet bieżącym danym ze schowka w stosunku do historycznego kontekstu rozmowy, aby zapobiec halucynacjom.

---

## 📝 Przykłady użycia

1. **Podsumuj tekst:**
* *Działanie:* Skopiuj długi e-mail lub tekst ze strony internetowej (Ctrl+C).
* *Polecenie głosowe:* „Komputer, podsumuj tekst w schowku.”

2. **Tłumaczenie/Analiza:**
* *Działanie:* Skopiuj fragment kodu.
* *Polecenie głosowe:* „Komputer, co robi kod w schowku?”

3. **Czat ogólny:**
* *Polecenie głosowe:* „Komputer, opowiedz mi dowcip o programistach”.

4. **Zresetuj pamięć:**
* *Polecenie głosowe:* „Komputer, zapomnij o wszystkim”. (Czyści historię JSON).
XSPACEbreakX