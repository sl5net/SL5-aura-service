# 🧠 Tryb hybrydowy SL5 Aura: lokalna integracja LLM

**Stan:** Eksperymentalny / Stabilny
**Technologia:** Ollama (Llama 3.2) + podproces Pythona
**Prywatność:** 100% offline

## Koncepcja: „Architekt i stażysta”

Tradycyjnie Aura opiera się na regułach deterministycznych (RegEx) – szybkich, precyzyjnych i przewidywalnych. To jest **„Architekt”**. Czasami jednak użytkownik chce zapytać o coś „niejasnego” lub kreatywnego, na przykład „Opowiedz mi dowcip”* lub *„Podsumuj ten tekst”*.

Tutaj z pomocą przychodzi **Lokalna wtyczka LLM** („Stażysta”**):
1. **Aura (RegEx)** najpierw sprawdza wszystkie ścisłe polecenia („Włącz światła”, „Otwórz aplikację”).
2. Jeśli nic nie pasuje do **AND**/ **LUB** określonego słowa wyzwalającego (np. „Aura ...”), aktywuje się reguła awaryjna.
3. Tekst wysyłany jest do lokalnego modelu AI (Ollama).
4. Odpowiedź jest oczyszczana i wyświetlana za pomocą TTS lub wpisywania tekstu.

---

## 🛠 Warunki wstępne

Wtyczka wymaga działającej instancji [Ollama](https://ollama.com/) działającej lokalnie na komputerze.

__KOD_BLOKU_0__

---

## 📂 Kolejność konstrukcji i obciążenia

Wtyczka została celowo umieszczona w folderze `z_fallback_llm`.
Ponieważ Aura ładuje wtyczki **alfabetycznie**, to nazewnictwo gwarantuje, że reguła LLM zostanie załadowana **ostatni**. Służy jako „siatka bezpieczeństwa” dla nierozpoznanych poleceń.

**Ścieżka:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. Mapa (`FUZZY_MAP_pre.py`)

Używamy **wysokiego wyniku (100)** i słowa wyzwalającego, aby zmusić Aurę do przekazania kontroli scenariuszowi.

__KOD_BLOKU_1__

### 2. Program obsługi (`ask_ollama.py`)

Ten skrypt komunikuje się z interfejsem CLI Ollama.
**Ważne:** Zawiera funkcję „czysty_tekst_do_typowania”. Surowe wyniki LLM często zawierają emoji (😂, 🚀) lub znaki specjalne, które mogą powodować awarie narzędzi takich jak `xdotool` lub starsze systemy TTS.

__KOD_BLOKU_2__

---

## ⚙️ Opcje dostosowywania

### Zmiana wyzwalacza
Zmodyfikuj RegEx w `FUZZY_MAP_pre.py`, jeśli nie chcesz używać „Aura” jako słowa budzącego.
* Przykład prawdziwego Catch-All (wszystko, czego Aura nie wie): `r'^(.*)$'` (Uwaga: dostosuj wynik!)

### Zamiana modelu
Możesz łatwo zamienić model w `ask_ollama.py` (np. na `mistral` w celu uzyskania bardziej złożonej logiki, chociaż wymaga to więcej pamięci RAM).
__KOD_BLOKU_3__

### Podpowiedź systemowa (osoba)
Możesz nadać Aurze osobowość, dostosowując `instrukcję_systemową`:
> „Jesteś sarkastycznym asystentem z filmu science-fiction”.

---

## ⚠️ Znane ograniczenia

1. **Opóźnienie:** Pierwsze żądanie po uruchomieniu może zająć 1–3 sekundy, gdy model ładuje się do pamięci RAM. Kolejne żądania są szybsze.
2. **Konflikty:** Jeśli wyrażenie regularne jest zbyt szerokie (`.*`) bez odpowiedniej struktury folderów, może pochłonąć standardowe polecenia. Kolejność alfabetyczna („z_...”) jest istotna.
3. **Sprzęt:** Wymaga ok. 2 GB wolnej pamięci RAM dla Lamy 3.2.