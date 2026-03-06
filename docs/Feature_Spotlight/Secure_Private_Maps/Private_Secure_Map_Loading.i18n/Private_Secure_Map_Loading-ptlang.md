# RECURSO EM DESTAQUE: Carregamento seguro de mapas privados e embalagem automática

Este documento descreve a arquitetura para gerenciar plug-ins de mapas confidenciais (por exemplo, dados do cliente, comandos proprietários) de uma forma que permite a **edição ao vivo** enquanto aplica as **Práticas recomendadas de segurança** para evitar a exposição acidental do Git.

---

## 1. O conceito: segurança "Matryoshka"

Para garantir o máximo de privacidade ao usar ferramentas padrão, o Aura usa uma estratégia de aninhamento **Matryoshka (boneca russa)** para arquivos criptografados.

1. **Camada Externa:** Um arquivo ZIP padrão criptografado com **AES-256** (por meio do comando `zip` do sistema).
* *Aparência:* Contém apenas **um** arquivo chamado `aura_secure.blob`.
* *Benefício:* Oculta nomes de arquivos e estrutura de diretórios de olhares indiscretos.
2. **Camada Interna (O Blob):** Um contêiner ZIP não criptografado dentro do blob.
* *Conteúdo:* A estrutura de diretórios real e os arquivos Python.
3. **Estado de funcionamento:** Quando desbloqueado, os arquivos são extraídos para uma pasta temporária prefixada com um sublinhado (por exemplo, `_private`).
* *Segurança:* Esta pasta é estritamente ignorada por `.gitignore`.

---

## 2. Fluxo de trabalho técnico

### A. O Portão de Segurança (Inicialização)
Antes de descompactar qualquer coisa, o Aura verifica `scripts/py/func/map_reloader.py` para regras `.gitignore` específicas.
* **Regra 1:** `config/maps/**/.*` (protege arquivos-chave)
* **Regra 2:** `config/maps/**/_*` (protege os diretórios de trabalho)
Se estes estiverem faltando, o sistema **cancela**.

### B. Descompactação (orientada por exceção)
1. O usuário cria um arquivo de chave (por exemplo, `.auth_key.py`) contendo a senha (em texto simples ou comentários).
2. Aura detecta este arquivo e o ZIP correspondente (por exemplo, `private.zip`).
3. Aura descriptografa o ZIP externo usando a chave.
4. Aura detecta `aura_secure.blob`, extrai a camada interna e move os arquivos para o diretório de trabalho `_private`.

### C. Edição ao vivo e embalagem automática (o ciclo)
É aqui que o sistema se torna "Autocurativo":

1. **Editar:** Você modifica um arquivo em `_private/` e o salva.
2. **Acionador:** Aura detecta a alteração e recarrega o módulo.
3. **Lifecycle Hook:** O módulo aciona sua função `on_reload()`.
4. **SecurePacker:** Um script (`secure_packer.py`) na raiz da pasta privada é executado:
* Cria o ZIP interno (estrutura).
* Ele o renomeia para `.blob`.
* Ele chama o comando `zip` do sistema para criptografá-lo no arquivo externo usando a senha do arquivo `.key`.

**Resultado:** Seu `private.zip` está sempre atualizado com suas alterações mais recentes, mas o Git só vê a alteração do arquivo ZIP binário.

---

## 3. Guia de configuração

### Etapa 1: Estrutura de diretório
Crie uma estrutura de pastas como esta:
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### Etapa 2: O arquivo-chave (`.auth_key.py`)
Deve começar com um ponto.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### Etapa 3: O script Packer (`secure_packer.py`)
Coloque este script dentro da sua pasta privada do mapa (antes de compactá-lo inicialmente). Ele lida com a lógica de criptografia. certifique-se de que seus mapas chamem esse script por meio do gancho `on_reload`.

### Etapa 4: implementação do gancho
Em seus arquivos de mapa (`.py`), adicione este gancho para acionar o backup a cada salvamento:

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Status e segurança do Git

Quando configurado corretamente, `git status` irá **apenas** mostrar:
__CODE_BLOCO_3__
A pasta `_private_maps` e o arquivo `.auth_key.py` nunca são rastreados.
```text
modified:   config/maps/private/private_maps.zip
```
# Guia do desenvolvedor: ganchos do ciclo de vida do plug-in

Aura SL5 permite que plugins (Mapas) definam "Hooks" específicos que são executados automaticamente quando o estado do módulo muda. Isso é essencial para fluxos de trabalho avançados, como o sistema **Secure Private Map**.

## O gancho `on_reload()`

A função `on_reload()` é uma função opcional que você pode definir em qualquer módulo Map.

### Comportamento
* **Trigger:** Executado imediatamente após um módulo ser recarregado com sucesso **hot-reload** (modificação de arquivo + trigger de voz).
* **Contexto:** É executado no thread principal do aplicativo.
* **Segurança:** Envolvido em um bloco `try/except`. Os erros aqui serão registrados, mas **não travarão** o aplicativo.

### Padrão de uso: O "Daisy Chain"
Para pacotes complexos (como Mapas Privados), você geralmente tem muitos subarquivos, mas apenas um script central (`secure_packer.py`) deve lidar com a lógica.

Você pode usar o gancho para delegar a tarefa para cima:

__CODE_BLOCO_5__

### Melhores Práticas
1. **Seja rápido:** Não execute tarefas de bloqueio longas (como downloads enormes) no gancho principal. Use fios se necessário.
2. **Idempotência:** Certifique-se de que seu gancho possa ser executado várias vezes sem quebrar as coisas (por exemplo, não anexe a um arquivo indefinidamente, em vez disso reescreva-o).