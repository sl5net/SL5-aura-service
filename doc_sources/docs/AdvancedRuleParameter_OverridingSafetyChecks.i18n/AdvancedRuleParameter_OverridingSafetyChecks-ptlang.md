# Documentação do mecanismo de regras SL5 Aura

## Parâmetro de regra avançada: substituindo verificações de segurança

Em alguns cenários (por exemplo, comandos internos altamente confiáveis ou entradas simples e de alta confiança), os usuários podem querer forçar a execução de etapas de pós-processamento (como `fuzzyRules`), mesmo que a confiança do sistema no reconhecimento de voz inicial seja baixa.

Por padrão, o SL5 Aura emprega uma proteção de segurança: se as alterações nas entradas forem altas (`LT_SKIP_RATIO_THRESHOLD`), as ferramentas de pós-processamento são ignoradas para evitar correções/alucinações não confiáveis e por motivos de desempenho.


Para desabilitar esta verificação de segurança para uma regra específica, adicione o identificador ao parâmetro `skip_list`:

__CODE_BLOCK_0__