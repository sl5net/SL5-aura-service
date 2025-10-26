## Recurso em destaque: Implementando um modo de tradução ao vivo alternável

Nossa estrutura de assistente de voz plugável foi projetada para máxima flexibilidade. Este guia demonstra um recurso poderoso: um modo de tradução ao vivo que pode ser ativado e desativado com um simples comando de voz. Imagine falar com seu assistente em alemão e ouvir o resultado em português e depois voltar ao comportamento normal instantaneamente.

Isto é conseguido não alterando o mecanismo principal, mas manipulando habilmente o próprio arquivo de configuração de regras.

### Como usá-lo

Configurar isso envolve adicionar duas regras ao seu arquivo `FUZZY_MAP_pre.py` e criar os scripts correspondentes.

**1. A regra de alternância:** Esta regra escuta o comando para ativar ou desativar o modo de tradução.

```python
# Rule to turn the translation mode on or off
    ('', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|einschalten|deaktivieren|ausschalten|toggle|Dogge|doppelt)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
```
Quando você diz "Übersetzung einschalten" (Ativar tradução), o script `toggle_translation_mode.py` é executado.

**2. A Regra de Tradução:** Esta é uma regra "pega-tudo" que, quando ativa, corresponde a qualquer texto e o envia para o script de tradução.

```python
    # ANCHOR: The following line is controlled by the toggle script.
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_german_to_portuguese.py']}),
```
A chave aqui é o comentário `# TRANSLATION_RULE`. Isso atua como uma "âncora" que o script de alternância usa para localizar e modificar a regra abaixo dele.

### Como funciona: a magia por trás da cortina

Em vez de usar um estado interno, esse método edita diretamente o mapa de regras no sistema de arquivos. O script `toggle_translation_mode.py` atua como um gerenciador de configuração.

1. **Encontre a regra:** Quando acionado, o script lê o conteúdo de `FUZZY_MAP_pre.py`. Ele procura o comentário âncora exclusivo `# TRANSLATION_RULE`.

2. **Alternar o estado:**
* **Para desabilitar:** Se a linha de regra abaixo da âncora estiver ativa, o script adiciona um `#` no início da linha, comentando-a efetivamente e desabilitando-a.
* **Para Habilitar:** Se a linha da regra já estiver comentada, o script remove cuidadosamente o `#` inicial, reativando a regra.

3. **Salvar e recarregar:** O script salva o conteúdo modificado de volta em `FUZZY_MAP_pre.py`. Em seguida, ele cria um arquivo de gatilho especial (por exemplo, `RELOAD_RULES.trigger`). O serviço principal monitora constantemente esse arquivo de gatilho. Quando aparece, o serviço sabe que sua configuração foi alterada e recarrega todo o mapa de regras do disco, aplicando a alteração instantaneamente.

### Filosofia de Design: Vantagens e Considerações

Esta abordagem de modificar diretamente o arquivo de configuração foi escolhida por sua clareza e simplicidade para o usuário final.

#### Vantagens:

* **Alta Transparência:** O estado atual do sistema está sempre visível. Uma rápida olhada no arquivo `FUZZY_MAP_pre.py` revela imediatamente se a regra de tradução está ativa ou comentada.
* **Sem alterações no mecanismo principal:** Este poderoso recurso foi implementado sem alterar uma única linha do mecanismo principal de processamento de regras. Isso demonstra a flexibilidade do sistema de plugins.
* **Intuitivo para desenvolvedores:** O conceito de ativar ou desativar uma parte da configuração comentando-a é um padrão familiar, simples e confiável para qualquer pessoa que tenha trabalhado com código ou arquivos de configuração.

#### Considerações:

* **Permissões do sistema de arquivos:** Para que esse método funcione, o processo do assistente deve ter permissões de gravação em seus próprios arquivos de configuração. Em alguns ambientes de alta segurança, isso pode ser levado em consideração.