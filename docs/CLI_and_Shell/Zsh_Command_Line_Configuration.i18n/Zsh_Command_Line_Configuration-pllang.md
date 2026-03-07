Ten dokument podsumowuje ostateczną i zweryfikowaną konfigurację Zsh do interakcji z usługą Pythona za pośrednictwem wiersza poleceń.

Konfiguracja zapewnia trzy różne metody dostępu do usługi, od bezpiecznego wyjścia do natychmiastowego wykonania.

## Podsumowanie konfiguracji wiersza poleceń Zsh

### 1. Plik konfiguracyjny

Cały poniższy kod należy wkleić do pliku **`~/.zshrc`**. Pamiętaj o **`source ~/.zshrc`** lub otwarciu nowej sesji terminala po dokonaniu zmian.

### 2. Ostatni blok kodu

Blok ten definiuje trzy wymagane funkcje. Zawiera niezbędne polecenia „unalias”, aby zapobiec błędowi konfliktu, który napotkaliśmy wcześniej.

__KOD_BLOKU_0__

---

### 3. Użycie trzech poleceń

| Polecenie | Funkcjonalność | Poziom bezpieczeństwa | Przykład |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Wyjście standardowe:** Wykonuje usługę i drukuje cały wynik bezpośrednio na konsoli. | **BEZPIECZNY** | `sl Czym jest dom` (Wydruki: "Dom to...") |
| **`slz`** | **Przygotowanie do bezpiecznego wykonania:** Wykonuje usługę i wkleja dane wyjściowe (np. polecenie powłoki) do linii wejściowej Zsh, gotowe do przeglądu lub wykonania. | **BEZPIECZNY/PRZYGOTOWANIE** | `slz git` (Wkleja: `git add . && git commit...` **ale go nie uruchamia**.) |
| **`slxXsoidfuasdzof`** | **Natychmiastowe wykonanie:** Wykonuje usługę i natychmiast uruchamia dane wyjściowe jako polecenie powłoki. Użyj tajemniczej nazwy jako środka bezpieczeństwa. | **NIEBEZPIECZNE** | `slxXsoidfuasdzof git` (Natychmiast uruchamia polecenie `git add...`.) |