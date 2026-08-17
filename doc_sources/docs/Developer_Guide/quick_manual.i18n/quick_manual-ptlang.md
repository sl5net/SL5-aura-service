## Atributos avançados de regras

Além dos campos padrão, as regras podem ser aprimoradas com opções especiais:

### `only_in_windows` (filtro de título da janela)
Apesar do nome, esse atributo é **independente do sistema operacional**. Ele filtra as regras com base no título da janela atualmente ativa.

* **Função:** A regra só é processada se o título da janela ativa corresponder a um dos padrões fornecidos (Regex).
*   **Exemplo:**
    ```python
    (
        '|', 
        r'\b(pipe|symbol)\b', 
        75, 
        {'only_in_windows': ['Terminal', 'Console', 'iTerm']}
    ),
    ```
*Neste caso, a substituição só ocorre se o usuário estiver trabalhando dentro de uma janela de terminal.*

### `on_match_exec` (execução de script)
Permite acionar scripts Python externos quando uma regra corresponde.

* **Sintaxe:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
* **Caso de uso:** Ideal para ações complexas, como chamadas de API, tarefas do sistema de arquivos ou geração de conteúdo dinâmico.