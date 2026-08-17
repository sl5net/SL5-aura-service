# 🧠 SL5 Aura: Integração LLM offline avançada

**Status:** Produção pronta
**Motor:** Ollama (Lhama 3.2 3B)
**Latência:** Instantâneo (<0,1s no acerto do cache) / ~20s (geração na CPU)

## 1. A Filosofia do "Arquiteto e Estagiário"
Aura opera em um modelo híbrido para equilibrar **precisão** e **flexibilidade**:
* **The Architect (RegEx/Python):** Execução determinística e instantânea para comandos do sistema (por exemplo, "Abrir navegador", "Aumentar volume").
* **O Estagiário (LLM Local):** Lida com consultas difusas, resumos e conhecimento geral. Ele só é acionado se nenhuma correspondência de regra estrita ou palavras-chave específicas forem usadas.

---

## 2. Arquitetura de desempenho

Para tornar um LLM local utilizável em CPUs padrão sem aceleração de GPU, implementamos uma **Estratégia de desempenho de 3 camadas**:

### Camada 1: O "Modo Instantâneo" (palavras-chave)
* **Gatilho:** Palavras como "Instant", "Schnell", "Sofort".
* **Lógica:** Ignora totalmente o LLM. Ele compara palavras-chave de entrada do usuário com o banco de dados SQLite local usando interseção definida.
* **Latência:** **< 0,05s**

### Camada 2: O Cache Inteligente (SQLite)
* **Lógica:** Cada prompt tem hash (SHA256). Antes de perguntar ao Ollama, verificamos `llm_cache.db`.
* **Recurso "Variação Ativa":** Mesmo que exista um acerto no cache, o sistema às vezes (20% de chance) gera uma *nova* variante para aprender frases diferentes para a mesma pergunta. Idealmente, armazenamos cerca de 5 variantes por pergunta.
* **Recurso "Hashing Semântico":** Para perguntas longas (>50 caracteres), usamos o LLM para extrair palavras-chave primeiro (por exemplo, "guia de instalação") e fazer o hash delas em vez da frase completa. Isso corresponde a "Como faço para instalar?" com "Instruções de instalação, por favor".
* **Latência:** **~0,1s**

### Camada 3: A geração da API (fallback)
* **Lógica:** Se não existir cache, chamamos a API Ollama (`http://localhost:11434/api/generate`).
* **Otimização:**
* **Limites rígidos:** `num_predict=60` força o modelo a parar após aproximadamente 40 palavras.
* **Ping de entrada:** Textos grandes (README) são passados via STDIN para evitar limites de argumentos do sistema operacional.
* **Latência:** **~15-25s** (depende da CPU)

---

## 3. Aterramento do Sistema (Anti-Alucinação)

LLMs genéricos tendem a inventar elementos GUI (botões, menus). Injetamos um **`AURA_TECH_PROFILE`** estrito em cada prompt do sistema:

1. **Sem GUI:** Aura é um serviço CLI headless.
2. **Sem arquivos de configuração:** Lógica é código Python, não `.json`/`.xml`.
3. **Gatilhos:** O controle externo funciona por meio da criação de arquivo (`touch /tmp/sl5_record.trigger`), não de APIs.
4. **Instalação:** Leva de 10 a 20 minutos devido aos downloads do modelo de 4 GB (evita mentiras do tipo "Ele é instalado em 3 segundos").

---

## 4. A ponte da área de transferência (segurança Linux)

Os serviços em segundo plano (systemd) não podem acessar a área de transferência do X11/Wayland diretamente devido ao isolamento de segurança.
* **Solução:** Um script de sessão do usuário (`clipboard_bridge.sh`) espelha o conteúdo da área de transferência em um arquivo de disco RAM (`/tmp/aura_clipboard.txt`).
* **Aura:** Lê este arquivo, ignorando todos os problemas de permissão.

---

## 5. Autoaprendizagem (aquecimento de cache)

Fornecemos um script `warm_up_cache.py`.
1. Lê o projeto `README.md`.
2. Pede ao LLM que invente prováveis perguntas dos usuários sobre o projeto.
3. Simula essas questões no Aura para pré-preencher o banco de dados.