# Macros de mapa difuso e lógica de colchetes

Aura suporta o agrupamento de múltiplas regras de pré-processamento em arquivos `FUZZY_MAP_pre.py` para executá-los sequencialmente como um pipeline coeso assim que uma "Regra inicial" for acionada. Este documento descreve a filosofia de design, a sintaxe e o fluxo de execução deste recurso.

## Princípios Básicos de Design

1. **Redundância zero**: as regras dentro de um grupo permanecem tuplas padrão do Python:
`('replacement_text', r'regex_pattern', limite, flags_and_options)`
2. **Dupla usabilidade**: regras individuais dentro de um grupo são regras independentes totalmente funcionais. Se o grupo não for acionado, eles serão avaliados normalmente no loop pai.
3. **Marcador de final passivo**: O final de um grupo é definido por uma entrada de regra passiva que nunca é correspondida por si só. Ele atua puramente como um marcador de limite para o analisador.
4. **Fallback híbrido (anexar em não correspondência)**: quando um grupo está ativo, cada regra interna deve contribuir para a saída. Se a regex de uma regra interna corresponder ao texto, a substituição normal ocorrerá. Se não corresponder, o texto substituto será anexado ao texto atual com um espaço.

---

## Sintaxe e Estrutura

Um grupo de macros é definido agrupando uma série de regras padrão entre uma **Regra inicial** e uma **Regra final** em `FUZZY_MAP_pre.py`.

### 1. A regra inicial
A regra inicial é uma regra padrão que aciona a macro quando correspondida. Inclui uma chave `'group_start'` em seu dicionário de opções:
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. Regras Internas
Regras internas são regras padrão colocadas sequencialmente após a Regra Inicial. Eles não requerem nenhum metadado especial:
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. A regra final (marcador passivo)
A regra final tem uma substituição `None`, um padrão vazio e uma chave `'group_end'` em seu dicionário de opções:
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## Exemplo concreto

Aqui está um caso de teste prático definido em um arquivo `FUZZY_MAP_pre.py`:

__CODE_BLOCO_3__

### Cenários de fluxo de execução:

* **Cenário A (Macro acionada)**:
* Entrada: `"iniciar sandbox com apfel"`
* Fluxo esperado:
1. A regra inicial corresponde a `"start sandbox"` e a substitui por `"Sandbox:"` -> texto atual: `"Sandbox: mit apfel"`.
2. O grupo `'sandbox_test'` é acionado.
3. Executamos as regras internas recursivamente em `"Sandbox: mit apfel"`:
- A regra interna 1 corresponde a `"apfel"` e substitui por `"birne"` -> texto atual: `"Sandbox: mit birne"`.
- A regra interna 2 não corresponde a `"banane"`. Como o grupo está ativo, ele volta a anexar `"banane"` -> Texto atual: `"Sandbox: mit birne banane"`.
4. O texto final `"Sandbox: mit birne banane"` é retornado e corrigido pelo LanguageTool.
* Saída: `"Sandbox: com Birne Banane"`

* **Cenário B (Macro não acionada - Dupla usabilidade)**:
* Entrada: `"ein apfel und eine kirsche"`
* Fluxo esperado:
1. A regra inicial não corresponde. O grupo `'sandbox_test'` permanece inativo.
2. O loop prossegue para a próxima regra.
3. **Regra interna 1**: Corresponde a `"apfel"` e substitui-o por `"birne"` -> Texto atual: `"ein birne und eine kirsche"`.
4. **Regra Interna 2**: Não corresponde. Como o grupo não foi acionado, a regra se comporta como uma regra autônoma normal e **nada é anexado**.
5. A Regra Final é ignorada.
* Saída: `"ein birne und eine kirsche"`

---

## Detalhes técnicos (sob o capô)

* **Recursão isolada**: Quando um grupo é acionado, o mecanismo invoca recursivamente `process_text_in_background` com `custom_rules=[inner_rule]`. Isso permite que cada regra interna seja executada em uma passagem de pipeline síncrona e completa.
* **Proteções de desempenho e estabilidade**:
* **Sequence Bypass**: execuções recursivas internas ignoram a fila de sequência `chunk_id` para evitar conflitos e atrasos de execução.
* **Supressão de E/S e TTS**: execuções recursivas suprimem a gravação de arquivos intermediários e as saídas de fala TTS, garantindo que apenas o texto final estabilizado seja escrito e falado.
* **Proteção de estabilidade**: execuções recursivas são interrompidas estritamente após uma iteração para evitar loops infinitos de estabilidade durante acréscimos de fallback.
* **Terminação Segura**: A verificação de estabilidade depende estritamente da contagem máxima de iterações (`MAX_ITERATIONS_FOR_SAFETY`) para evitar loops infinitos, ignorando a limitação baseada em tempo que poderia abortar prematuramente execuções de macros legítimas e mais lentas.
```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```