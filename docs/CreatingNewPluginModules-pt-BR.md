## Criando novos módulos de plug-in

Nossa estrutura usa um poderoso sistema de descoberta automática para carregar módulos de regras. Isso torna a adição de novos conjuntos de comandos simples e limpa, sem a necessidade de registrar manualmente cada novo componente. Este guia explica como criar, estruturar e gerenciar seus próprios módulos personalizados.

### O conceito central: módulos baseados em pastas

Um módulo é simplesmente uma pasta dentro do diretório `config/maps/`. O sistema verifica automaticamente esse diretório e trata cada subpasta como um módulo carregável.

### Guia passo a passo para criar um módulo

Siga estas etapas para criar um novo módulo, por exemplo, para armazenar macros de um jogo específico.

**1. Navegue até o Diretório de Mapas**
Todos os módulos de regras residem na pasta `config/maps/` do projeto.

**2. Crie a pasta do seu módulo **
Crie uma nova pasta. O nome deve ser descritivo e usar sublinhados em vez de espaços (por exemplo, `my_game_macros`, `custom_home_automation`).

**3. Adicionar subpastas de idiomas (etapa crítica)**
Dentro da pasta do novo módulo, você deve criar subpastas para cada idioma que pretende oferecer suporte.

* **Convenção de nomenclatura:** Os nomes dessas subpastas **devem ser códigos de localidade de idioma válidos**. O sistema utiliza esses nomes para carregar as regras corretas para o idioma ativo.
* **Exemplos corretos:** `de-DE`, `en-US`, `en-GB`, `pt-BR`
* **Aviso:** Se você usar um nome não padrão como `german` ou `english_rules`, o sistema irá ignorar a pasta ou tratá-la como um módulo separado, não específico do idioma.

**4. Adicione seus arquivos de regras**
Coloque seus arquivos de regras (por exemplo, `FUZZY_MAP_pre.py`) dentro da subpasta de idioma apropriada. A maneira mais fácil de começar é copiar o conteúdo de uma pasta de módulo de idioma existente para usar como modelo.

### Exemplo de estrutura de diretório

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### Gerenciando Módulos na Configuração

O sistema foi projetado para exigir configuração mínima.

#### Habilitando Módulos (O Padrão)

Os módulos estão **ativados por padrão**. Enquanto existir uma pasta de módulo em `config/maps/`, o sistema irá encontrá-la e carregar suas regras. **Você não precisa adicionar uma entrada ao seu arquivo de configurações para ativar um novo módulo.**

#### Desativando Módulos

Para desabilitar um módulo, você deve adicionar uma entrada para ele no dicionário `PLUGINS_ENABLED` em seu arquivo de configurações e definir seu valor como `False`.

**Exemplo (`config/settings.py`):**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True
    "wannweil",

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### Notas importantes de design

* **Comportamento padrão: Nenhuma entrada é igual a `True`**
Se um módulo não estiver listado no dicionário `PLUGINS_ENABLED`, ele será considerado **ativo** por padrão. Este design mantém o arquivo de configuração limpo, pois você só precisa listar as exceções.

* **Abreviação de Habilitação**
Seu sistema de configuração também entende que listar uma chave de módulo sem valor implica que ela está habilitada. Por exemplo, adicionar `"wannweil"` ao dicionário é o mesmo que adicionar `"wannweil": True`. Isso fornece um atalho conveniente para habilitar módulos.

* **Desabilitando Módulos Pai (Aprimoramento Futuro):** O comportamento pretendido é que desabilitar um módulo pai deve   
desabilita automaticamente todos os seus módulos filhos e subpastas de idioma. Por exemplo, definir `"standard_actions": False` deve impedir o carregamento de `de-DE` e `en-US`. *Observe que a implementação desta desativação recursiva ainda está planejada.* (27.10.25 Seg)
  
* **Aprimoramento futuro**
*(Observação: este é um recurso planejado)*
O objetivo é aprimorar ainda mais esse sistema. Por exemplo, fornecer uma maneira de respeitar as configurações do módulo filho mesmo se o pai estiver desabilitado ou introduzir regras de herança mais complexas. (27.10.'25 seg)