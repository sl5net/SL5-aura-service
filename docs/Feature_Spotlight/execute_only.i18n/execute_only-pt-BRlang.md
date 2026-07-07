# Atributo de regra: `execute_only` (Experimental, 7.7.'26 Ter)

O atributo `execute_only` é uma opção de configuração experimental projetada para regras que acionam apenas scripts externos sem modificar ou substituir o texto de entrada.

## Visão geral
- **Tipo:** `bool` (por exemplo, `True` ou `False`)
- **Caso de uso principal:** Normalmente usado em combinação com `on_match_exec` para executar scripts externos.

## Como funciona e comportamento atual
- **Otimização de velocidade:** (apenas alguns milissegundos) Ignora o pós-processamento de texto e as rotinas de substituição de texto, acelerando a execução imediata da ação acionada.
- **Sem efeito colateral de exclusão/falta:** Definir `execute_only` como `True` **não** impede que outras regras correspondentes avaliem o mesmo texto de entrada.
- **Interrupção do fluxo:** Se você precisar impedir que regras subsequentes processem o mesmo texto de entrada, atualmente será necessário encerrar o fluxo de execução manualmente (por exemplo, lançando uma exceção no final do script acionado ou do manipulador do conjunto de regras).

## Exemplo de configuração

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```