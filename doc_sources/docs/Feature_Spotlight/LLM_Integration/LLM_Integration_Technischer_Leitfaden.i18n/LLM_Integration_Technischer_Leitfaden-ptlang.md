# 🧠 SL5 Aura: Integração LLM Offline Erweiterte

**Status:** Número de produção
**Motor:** Ollama (Lhama 3.2 3B)
**Latência:** Sofort (<0,1s bei Cache Hit) / ~20s (Generierung auf CPU)

## 1. A filosofia "Architekt & Praktikant"
Aura nutzt ein Hybrid-Modell, um **Präzision** und **Flexibilität** zu vereinen:
* **Der Architekt (RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle ("Browser öffnen", "Lauter").
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. Wird nur active, wenn keine strikte Regel greift.

---

## 2. Arquitetura de desempenho

Um LLM local em CPUs normais (sem GPU) é essencial para a máquina, e é definido como uma **3-Stufen-Strategie**:

### Stufe 1: Der "Modo Instantâneo" (Schlagworte)
* **Trigger:** Wörter como "Instant", "Schnell", "Sofort".
* **Lógica:** Umgeht do LLM komplett. Vergleicht Schlagworte der Eingabe diretamente com o SQLite-Datenbank.
* **Latência:** **< 0,05s**

### Material 2: O Cache Inteligente (SQLite)
* **Lógica:** O prompt de comando será enviado (SHA256). Para uma transferência e uma chamada, o arquivo `llm_cache.db` será gerado.
* **Recurso "Variação Ativa":** Auch bei einem Cache-Treffer gerado como System manchmal (20% Chance) ativa uma *nova* Antwort-Variante. Ziel: ~5 Variantes para Frage für mehr Lebendigkeit.
* **Recurso "Hashing Semântico":** Bei langen Fragen (>50 Zeichen) extrahiert das LLM zuerst Keywords (z.B. "installation anleitung") e hasht este. Então nós perguntamos "O que eu instalei?" e "Installationshilfe bitte" como idêntico.
* **Latência:** **~0,1s**

### Stufe 3: A API-Generierung (Fallback)
* **Lógica:** Se o cache não existir, use a API original (`http://localhost:11434/api/generate`).
* **Otimização:**
* **Limites rígidos:** `num_predict=60` desde o modelo, nach ca. 40 Wörtern zu stoppen.
* **Tubulação de entrada:** Grande Texto (README) foi definido sobre STDIN, um limite de argumentos para sistemas de apostas.
* **Latência:** **~15-25s** (utilização da CPU)

---

## 3. Aterramento do Sistema (Anti-Alucinação)

LLMs genéricos geralmente contêm GUIs (botões, menus). Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**:

1. **Keine GUI:** Aura é um interface CLI Headless.
2. **Keine Config-Files:** Logik ist reiner Python-Code, não `.json`/`.xml`.
3. **Trigger:** A configuração externa é preenchida em eventos do sistema de dados (`touch /tmp/sl5_record.trigger`), não em APIs.
4. **Instalação:** Duração real de 10 a 20 minutos após o download do modelo de 4 GB (verhindert falsche Versprechen).

---

## 4. Ponte da área de transferência (segurança Linux)

O Hintergrunddienste (systemd) pode ser usado em sistemas de segurança muitas vezes não no Zwischenablage (X11/Wayland) zugreifen.
* **Leitura:** Um script na sessão do usuário (`clipboard_bridge.sh`) espiou a inserção em uma data de disco RAM (`/tmp/aura_clipboard.txt`).
* **Aura:** Liest diese Datei und umgeht so alle Rechte-Probleme.

---

## 5. Selbst-Lernen (aquecimento de cache)

Digite o script `warm_up_cache.py`:
1. É o `README.md` dos projetos.
2. É beauftragt do LLM, sich wahrscheinliche User-Fragen auszudenken.
3. Essa Fragen and Aura foi criada para que o Datenbank seja preenchido automaticamente.