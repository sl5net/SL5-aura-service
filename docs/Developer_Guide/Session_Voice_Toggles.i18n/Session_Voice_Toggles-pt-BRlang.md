# Manipulação de áudio de sessão e alternância de voz

Aura implementa um loop de processamento de áudio baseado em sessão. Os comandos de voz para gerenciamento de estado só estão ativos dentro de uma sessão de gravação estabelecida.

## Configuração
O comportamento interno da sessão é controlado por:
`ENABLE_WAKE_WORD = Verdadeiro/Falso` (em `config/settings.py`)

## Lógica Operacional
Ao contrário de um ouvinte de fundo persistente, o mecanismo STT do Aura (Vosk) processa áudio apenas quando uma sessão de gravação foi acionada externamente (por exemplo, via Hotkey).

> **Aura é o seu telescópio 🔭 para PC: controle à distância!**


### A alternância na sessão ("Teleskop")
Quando `ENABLE_WAKE_WORD` está definido como **True**:
1. **Acionador:** O usuário inicia uma sessão manualmente.
2. **Alternar:** Dizer "Teleskop" durante a sessão alterna entre os estados **ATIVO** e **SUSPENSO**.
3. **Comportamento:** permite ao usuário "pausar" e "retomar" o processamento de texto usando comandos de voz sem encerrar o fluxo de áudio.

### Privacidade e eficiência
Quando `ENABLE_WAKE_WORD` está definido como **False** (padrão):
- **Supressão STT:** Enquanto estiver em estado suspenso, as chamadas para `AcceptWaveform` e `PartialResult` são completamente ignoradas.
- **Privacidade:** Nenhum dado de áudio é analisado, a menos que o sistema esteja em um estado ativo explícito.
- **Gerenciamento de recursos:** o uso da CPU é minimizado ignorando a análise da rede neural durante a suspensão.

## Latência e desempenho
- **Retomada Instantânea:** Como o `RawInputStream` permanece aberto durante toda a sessão, mudar de SUSPENDED de volta para ACTIVE tem **0ms de latência adicional**.
- **Loop Timing:** O loop de processamento opera em um intervalo de aproximadamente 100 ms (`q.get(timeout=0.1)`), garantindo tempos de resposta quase instantâneos.