# Comandos de voz específicos do usuário

Aura permite que você defina comandos personalizados que estão **ativos apenas para você** (ou membros específicos da equipe). Isso evita que atalhos pessoais ou recursos experimentais sejam acionados por outros usuários.

## Configurar

Você pode aplicar essas regras em qualquer arquivo de mapeamento, como `FUZZY_MAP_pre.py` (entrada bruta) ou `FUZZY_MAP.py` (após correção).

Arquivo de destino: `config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py`

### Exemplo de código

Adicione este bloco ao final do arquivo:

__CODE_BLOCK_0__