# RECURSO EM DESTAQUE: Substituições de regras baseadas em arquivo

Este documento descreve como manter valores confidenciais (senhas, chaves de API, tokens)
do código-fonte `FUZZY_MAP_pre` / `FUZZY_MAP` e do histórico do Git carregando o
texto `replacement` de um arquivo separado em tempo de execução, em vez de codificá-lo.

Isto é especialmente útil durante transmissões ao vivo ou compartilhamentos de tela, onde o mapa
o próprio código-fonte pode estar visível, mas o arquivo referenciado não.

---

## 1. O conceito

Normalmente, o campo `replacement` de uma regra é o texto literal de saída:

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

Com a substituição baseada em arquivo habilitada, um valor `replacement` que começa com um
O prefixo configurado (por padrão `-` ou `.`) é tratado como um **nome de arquivo**.
Aura resolve esse nome de arquivo em relação ao próprio diretório do plugin, lê seu
conteúdo e usa esse conteúdo como texto de substituição.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

Se `api_key.txt` existir próximo ao `FUZZY_MAP_pre.py` do plugin, seu (removido)
o conteúdo é usado como substituto. Se o arquivo não existir, o literal
em vez disso, a string `-api_key.txt` é retornada (à prova de falhas: nenhum vazamento acidental de
"arquivo não encontrado" como texto utilizável e sem travamento).

---

## 2. Configurações

Configurado em `config/settings.py` (ou `config/settings_local.py` para local
substituições):

| Configuração | Tipo | Padrão | Descrição |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | `Verdade` | Chave mestre para todo o recurso. Se `False`, `replacement` é sempre usado literalmente. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `tupla[str]` | `('-', '.')` | Os valores `replacement` devem começar com um desses prefixos para acionar uma pesquisa de arquivo. Vazio/`Nenhum` = qualquer valor que não comece com uma letra é tratado como um nome de arquivo potencial. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | `Falso` | Se `True`, permite resolver arquivos fora do próprio diretório do plugin (por exemplo, caminhos absolutos ou sequências `../`). Consulte a seção Segurança abaixo. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `tupla[str]` | por exemplo `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Arquivos de Programas')` | Caminhos absolutos resolvidos começando com qualquer um deles são **sempre** rejeitados, independentemente de `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`. Limite rígido de segurança em relação aos diretórios do sistema. |

---

## 3. Resolução de caminho

O arquivo é resolvido da seguinte forma:

1. O `source_path` do plugin (gravado automaticamente pelo carregador de mapa) é
juntou-se a `PROJECT_ROOT` (lido em `SL5NET_AURA_PROJECT_ROOT`
variável de ambiente) para obter o diretório do plugin.
2. O valor `replacement` é adicionado a esse diretório.
3. A menos que `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` seja `True`, o caminho resolvido
deve permanecer dentro do diretório do plugin, ou a pesquisa será rejeitada.
4. Independentemente do acima exposto, qualquer caminho resolvido começando com uma entrada em
`FILE4REPLACEMENT_DENY_PREFIXES` é sempre rejeitado.
5. Se o arquivo existir, seu conteúdo removido será retornado. Caso contrário, o
a string `substituta` original é retornada inalterada.

---

## 4. Notas de segurança

- Habilite `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` apenas se você entender o
implicações: permite que qualquer usuário possa editar um arquivo `FUZZY_MAP_pre` (por exemplo
através de um editor de mapas on-line) para ler arquivos arbitrários que o processo Aura pode
acesso e ter seu conteúdo exibido como texto de saída ao vivo.
- `FILE4REPLACEMENT_DENY_PREFIXES` fornece uma proteção básica contra
diretórios comuns do sistema, mesmo quando a passagem de caminho é permitida, mas é
não substitui a restrição de quem pode editar arquivos de mapas.
- Os arquivos referenciados são texto simples no disco. Combine com o arquivo do seu sistema operacional
permissões se o conteúdo for confidencial.

---

## 5. Exemplo

Veja `config/maps/plugins/TEST_FILE4REPLACEMENT/` para um exemplo de plugin funcional,
e `tools/tests/TEST_FILE4REPLACEMENT.sh` para um script de teste que exercita
tanto uma pesquisa no diretório quanto uma pesquisa fora do diretório do plugin.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

Crie `.Zebra.txt` próximo a este arquivo com o texto de substituição desejado e, em seguida,
diga (ou digite através do console) `s Zebra` para ativá-lo.