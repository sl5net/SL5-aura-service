Ganchos Aura SL5: Adicionados

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'on_reload'
HOOK_UPSTREAM = 'on_folder_change'

on_folder_change() e
on_reload() para acionar a lógica após recarregamentos a quente. Use isso para execução em "cadeia" de scripts pais como secure_packer.py para pacotes complexos.

# Guia do desenvolvedor: ganchos do ciclo de vida do plug-in

Aura SL5 permite que plugins (Mapas) definam "Hooks" específicos que são executados automaticamente quando o estado do módulo muda. Isso é essencial para fluxos de trabalho avançados, como o sistema **Secure Private Map**.

## O gancho `on_folder_change` Gancho

Implementada detecção de gancho `on_folder_change`. O recarregador agora verifica o diretório

## O gancho `on_reload()`

A função `on_reload()` é uma função opcional que você pode definir em qualquer módulo Map.

### Comportamento
* **Trigger:** Executado imediatamente após um módulo ser recarregado com sucesso **hot-reload** (modificação de arquivo + trigger de voz).
* **Contexto:** É executado no thread principal do aplicativo.
* **Segurança:** Envolvido em um bloco `try/except`. Os erros aqui serão registrados, mas **não travarão** o aplicativo.

### Padrão de uso: O "Daisy Chain"
Para pacotes complexos (como Mapas Privados), você geralmente tem muitos subarquivos, mas apenas um script central (`secure_packer.py`) deve lidar com a lógica.

Você pode usar o gancho para delegar a tarefa para cima:

__CODE_BLOCK_0__