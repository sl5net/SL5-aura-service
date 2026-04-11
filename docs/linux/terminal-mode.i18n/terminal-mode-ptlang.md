# Modo Terminal (exclusão de idioma)

O Modo Terminal é um estado de configuração onde nenhum pacote de idiomas específico é instalado ou configurado para as unidades de processamento de fala/texto.

## Como ativar
Durante a configuração inicial ou o script de seleção de idioma, quando for solicitado o **Idioma principal**, insira:
- `n`
- `nenhum`
- `0`

## Efeitos
- **EXCLUDE_LANGUAGES** está definido como `all`.
- Nenhum modelo específico de idioma (como modelos Whisper ou Vosk) será baixado ou inicializado.
- O sistema opera no modo "Somente Terminal", útil para ambientes com pouco disco ou quando apenas as principais ferramentas CLI são necessárias sem suporte de fala localizada.

## Variáveis de ambiente
Quando ativo, são geradas as seguintes exportações:
__CODE_BLOCK_0__