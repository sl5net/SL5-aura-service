# Solução de problemas de áudio (Linux)

## Problema: Espeak / Fallback é silencioso
Se o áudio substituto (espeak) não for audível, provavelmente está silenciado no mixer de som do sistema (por exemplo, PulseAudio ou PipeWire).

### O "truque de string longa" para ativar o som
Pequenos fragmentos de áudio geralmente desaparecem muito rapidamente da GUI do mixer para serem ativados manualmente. Para corrigir isso, force um longo fluxo de áudio:

__CODE_BLOCK_0__