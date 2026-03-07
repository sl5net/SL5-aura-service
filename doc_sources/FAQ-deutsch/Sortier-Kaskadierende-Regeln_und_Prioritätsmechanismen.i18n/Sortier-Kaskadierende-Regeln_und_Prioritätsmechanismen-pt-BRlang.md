# Kaskadierende Regelausführung e Mecanismo de Prioridade

Todos os detalhes notwendigen, um dos complexos jogos de prioridade, modo e substituto para erklären.

---

# Kaskadierende Regelausführung e Mecanismo de Prioridade

Nosso sistema de regras é baseado em uma configuração sequencial, antes da posição de um regra na lista `fuzzy_map_pre` em sua prioridade definida (Modul-Lade-Reihenfolge > Zeilennummer).

Seguindo o princípio de **Kaskadierenden Regelausführung** (`default_mode_is_all = True`), todas as regras passadas serão alteradas, sendo um critério de parada específico preenchido.

## 1. Die Hohe Priorität: Der Deterministische Durchlauf

A Verarbeitung começou com o Durchlauf der Regeln no geladenen Reihenfolge. Aqui estão dois tipos de anwendungen, a lista de prioridades:

### A. Absolutes Stopp-Kriterium (Höchste Priorität)
A regra com a maior prioridade, uma **vollständigen Match** (de `^` até `$`) no Token erzielt, foi alterada e recebeu a mesma Verarbeitung para este Token sofort (**Primeira vitória na partida**). Dies stellt sicher, dass die spezifischste und deterministischste Regel Vorrang hat.

### B. Kumulation (Transformaçõesreihenfolge)
Quando uma regra for feita, mas nenhuma partida correspondente (`^...$`) for executada, a configuração será alterada. Die Verarbeitung geht jedoch zur nächsten Regel über. Da jede Regel auf dem **bereits modifizierten** Text arbeitet, ist die Listenreihenfolge entscheidend für die **Kaskadierung** der Transformationen.

## 2. Die Niedrige Priorität: Der Fuzzy-Fallback

A lógica fuzzy (pontuação 0–100) foi adicionada ao Fallback, um Tippfehler em Rohtext zu korrigieren.

Aus Performance- and Stabilitätsgründen wird die Fuzzy-Logik **nur dann** active, wenn der gesamte deterministische Durchlauf (Punkt 1) **keine einzige Regel** angewendet hat. Uma regra determinística altamente definida define o sinalizador atual e ** bloqueia ** o uso do Fuzzy-Fallback para o Token atual.

## 3. A validação externa (LanguageTool)

Nach Abschluss aller Regel-basierten Ersetzungen wird eine zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um estilístico ou oder gramatical Fehler zu beheben.

Esta ferramenta foi totalmente alterada, quando o ajuste da configuração padrão foi definido para a extensão de texto correta (`LT_SKIP_RATIO_THRESHOLD`). Dies stellt sicher, dass LT nicht auf Texte angewendet wird, die durch unsere Kaskade bereits so stark transformiert wurden, dass die Korrektur durch LT fehleranfällig wäre.