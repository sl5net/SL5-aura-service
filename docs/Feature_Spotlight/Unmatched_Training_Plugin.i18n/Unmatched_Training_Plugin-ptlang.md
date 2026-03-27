# Plugin de treinamento incomparável (`a_collect_unmatched_training`)

## Propósito

Este plugin coleta automaticamente entradas de voz não reconhecidas e as adiciona
como novas variantes para o regex do mapa difuso. Isso permite que o sistema se "autotreine"
ao longo do tempo, aprendendo com resultados de reconhecimento incomparáveis.

##Como funciona

1. A regra abrangente `COLLECT_UNMATCHED` em `FUZZY_MAP_pre.py` é acionada quando
nenhuma outra regra correspondeu à entrada de voz.
2. `collect_unmatched.py` é chamado via `on_match_exec` com o texto correspondente.
3. O texto é adicionado a `unmatched_list.txt` (separado por barras verticais).
4. A regex em `FUZZY_MAP_pre.py` é automaticamente estendida com a nova variante.

## Desativando o plugin

Quando você tiver coletado dados de treinamento suficientes, desative este plug-in:

- Desativando nas configurações do Aura
- Removendo a pasta do plugin do diretório `maps`
- Renomear a pasta com um nome inválido (por exemplo, adicionar um espaço: `a_collect unmatched_training`)

## Estrutura do arquivo
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## Observação

O plugin modifica `FUZZY_MAP_pre.py` em tempo de execução. Certifique-se de se comprometer
o arquivo atualizado regularmente para preservar os dados de treinamento coletados.