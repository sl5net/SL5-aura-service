# Ganchos de ciclo de vida do plug-in

Aura SL5 suporta ganchos de ciclo de vida que permitem que plugins (Mapas) executem lógica específica automaticamente quando seu estado muda.

## O gancho `on_reload()`

A função `on_reload()` é uma função opcional especial que você pode definir dentro de qualquer Mapa de Plugin (`.py`).

### Comportamento
* **Trigger:** Esta função é executada **imediatamente após** o módulo ter sido recarregado com sucesso (mudança de arquivo detectada + disparo de voz).
* **Contexto:** É executado dentro do fluxo principal do aplicativo.
* **Escopo:** **NÃO** é executado durante a inicialização do sistema (inicialização a frio). É estritamente para cenários de *re*-carregamento.

### Casos de uso
* **Segurança:** Criptografe ou compacte novamente arquivos confidenciais automaticamente após a edição.
* **Gerenciamento de estado:** Redefinição de contadores globais ou limpeza de caches específicos.
* **Notificação:** Registrar informações de depuração específicas para verificar se uma alteração foi aplicada.

### Detalhes Técnicos e Segurança
* **Tratamento de erros:** A execução é envolvida em um bloco `try/except`. Se sua função `on_reload` travar (por exemplo, `DivisionByZero`), ela registrará um erro (`❌ Erro ao executar on_reload...`), mas **não travará o Aura**.
* **Desempenho:** A função é executada de forma síncrona. Evite tarefas de longa duração (como downloads grandes) diretamente nesta função, pois elas bloquearão brevemente o processamento do comando de voz. Para tarefas pesadas, crie um tópico.

### Código de exemplo

__CODE_BLOCK_0__