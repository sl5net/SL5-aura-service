# Executando 0 A.D. com Aura Voice Control em sistemas com pouca RAM (Linux Mint)

Este guia documenta a configuração e otimização de memória para executar o controle de voz **sl5net Aura** juntamente com **0 A.D.** em hardware Linux Mint legado ou com memória limitada.

## Hardware alvo e perfil do sistema
**Dispositivo**: Lenovo ThinkPad T520 (laptop)
**CPU**: Intel Core i7 2620M (Dual Core @ 2,70 GHz - 3,40 GHz)
**Memória**: 5,67 GiB de RAM
- **Troca**: troca efetiva de 4 GiB
- **Sistema operacional**: Linux Mint 21.3 Virginia (64 bits)
- **Ambiente de área de trabalho**: Cinnamon 6.0.5 (servidor de exibição X11)
- **Alvo da aplicação**: 0 d.C. (Império Ascendente)

## Gerenciamento e arquitetura de memória
Em sistemas com ≤ 6 GiB de RAM, a execução simultânea de um ambiente de desktop pesado, um jogo RTS 3D (0 A.D.) e reconhecimento de fala requer proteção rigorosa da memória:

1. **Prioridade do modelo de fala Vosk**:
- Usa `vosk-model-small-de` (ou equivalente em idioma) para baixo consumo de memória (~300-500 MB).
- A retenção do modelo Vosk é priorizada para garantir a capacidade de resposta dos comandos em tempo real durante o jogo.

2. **Remoção automática do LanguageTool**:
- O processo Java do LanguageTool pode consumir aproximadamente 1,34 GiB RSS.
- Quando a RAM disponível cai abaixo de `CRITICAL_THRESHOLD_MB` (2,0 GiB), o `model_manager` do Aura encerra imediatamente o LanguageTool para liberar aproximadamente 1,3 GiB de RAM para o jogo.
- Um cooldown de 5 minutos (`set_language_tool_cooldown`) evita que o LanguageTool reinicie e destrua a memória durante o jogo ativo.

## Comandos de verificação
Para inspecionar a memória do sistema e os estados do processo:
# Verifique a memória e o uso de swap
```bash
free -h
```

# Verifique se o processo do LanguageTool foi despejado
```bash
ps aux | grep -i "[l]anguagetool"
```