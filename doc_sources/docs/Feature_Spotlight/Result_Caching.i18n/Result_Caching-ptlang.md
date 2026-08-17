# Cache de resultados avançado (com reconhecimento de estado)

## Visão geral
O Aura apresenta um cache de resultados persistente e sensível ao contexto, projetado para eliminar processamento redundante. Quando um comando de voz é reconhecido e corresponde a uma regra, o Aura verifica se exatamente o mesmo resultado foi gerado antes nas mesmas circunstâncias. Se uma correspondência for encontrada, o Aura ignora operações caras, como **verificações gramaticais do LanguageTool** ou **geração Ollama LLM**, entregando o resultado com latência quase zero.

## Principais recursos
- **Context-Aware:** O cache é específico para o título da janela ativa. Um comando dito no “LibreOffice” pode ter um resultado em cache diferente do mesmo comando no “Terminal”.
- **Self-Healing (Auto-Invalidation):** O cache expira automaticamente se você modificar o arquivo de regra subjacente (mapa `.py`).
- **Privacidade em primeiro lugar:** Todos os resultados armazenados em cache são armazenados em um banco de dados SQLite local (`data/_aura_result_cache.db`).
- **Manutenção Zero:** Para a maioria dos usuários, isso funciona inteiramente em segundo plano, sem configuração.

## Como funciona
O sistema gera um `cache_id` exclusivo baseado em três variáveis:
1. **A saída da regra:** O texto gerado pelo mapa.
2. **O Idioma:** O código do idioma ativo atual (por exemplo, `de-DE`).
3. **A Janela Ativa:** O título da janela atualmente em foco.

### Lógica de Validade
O cache garante que você nunca receba informações "obsoletas". Ele usa dois tipos de verificações de validade:

| Tipo | Nome | Lógica | Caso de uso |
| :--- | :--- | :--- | :--- |
| **Digite 0** | **Sincronização automática de arquivos** | Usa o horário de modificação (`mtime`) do arquivo de mapa. | **Padrão.** Se você editar seu Sandbox ou Mapa, todas as entradas de cache associadas serão invalidadas instantaneamente. |
| **Tipo 1** | **Carimbo de data e hora manual** | Usa um `timestamp` fixo fornecido nos atributos da regra. | **Desenvolvedor.** Codifique uma versão/carimbo de data/hora para forçar ou manter um estado de resultado específico. |

## Exemplos de configuração de regras

Você pode controlar o comportamento do cache diretamente nos arquivos `FUZZY_MAP_pre.py` ou `FUZZY_MAP.py`.

### 1. Comportamento padrão (cache automático)
Por padrão, o cache está habilitado e usa o horário de modificação do arquivo.
```python
# No extra attributes needed. 
# If this file is saved, the cache for this rule refreshes.
('Bold', r'^make it bold$', 100)
```

### 2. Desativando cache
Se um comando produzir dados dinâmicos (como a hora atual ou uma piada aleatória), você deverá desabilitar o cache.
```python
('Current Time', r'^what time is it$', 100, {
    'cache': False 
})
```

### 3. Carimbo de data/hora manual (versão fixa)
Se você quiser que o cache persista independentemente das edições do arquivo (a menos que você altere a versão), use um carimbo de data/hora manual.
```python
('Stable Command', r'^run complex task$', 100, {
    'timestamp': '2026-05-09-v1'
})
```

## Impacto no desempenho
- **Cache Miss:** Processamento padrão (0,05s - 5,0s dependendo do uso do LLM).
- **Cache Hit:** Processamento instantâneo.

Este mecanismo faz com que comandos ou erros de digitação corrigidos sejam retornados instantaneamente sem sobrecarregar a CPU.