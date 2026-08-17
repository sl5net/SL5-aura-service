Além das muitas opções de pesquisa, provavelmente existe uma pesquisa de texto completo em seu ambiente de desenvolvimento. Você também pode usar:

scripts/search_rules/search_rules.sh

Isso permite pesquisar nos mapas existentes ou no código-fonte ou na documentação. e então você pode abrir a paz que encontrou em seu editor favorito ou abri-la no github ou… configure o script conforme necessário.

MAPS_DIR é configurável via argumento posicional ou variável de ambiente

script mantém seu padrão codificado, mas permite substituições:

- Prioridade: 1) primeiro parâmetro posicional ($1), 2) MAPS_DIR env var existente,
3) padrão codificado "$SL5NET_AURA_PROJECT_ROOT/config/maps".
- Melhora a flexibilidade para CI, substituições locais e testes sem editar o script.
- Adiciona cotação e uma verificação de existência de diretório para falhar antecipadamente se o caminho for inválido.

Exemplo de uso:
- ./search_rules.sh usa padrão
- ./search_rules.sh ./docs usa o caminho fornecido
- MAPS_DIR=/env/maps ./search_rules.sh

Isso preserva a compatibilidade com versões anteriores enquanto torna a configuração explícita.

Há também uma versão para Windows PC (nesta pasta) que pode fazer um pouco menos: search_rules.ps1


(s, 28.3.'26 23:07 Sábado)