31.12.25 18:25 Quarta

A lista de tarefas e a lista de tarefas para o Zukunft:

### Documentação: Versuch "Entrada de Áudio Unificada" (Mic + Desktop)
**Status:** Pausiert (Prova de conceito existente, mas não estável/desempenho).

**Erfahrungen / Resultados:**
* **Roteamento:** PipeWire/PulseAudio não permite que o Python-Stream (ALSA-Bridge) seja instalado no microfone padrão físico (Stream-Restore-Logik).
* **Desempenho:** A configuração de RMS, VAD e Vosk em um único Loop, combinada com aumento de `pactl` externo, é maior para CPU-Last (Lüfterdrehen).
* **Sinal:** O índice de dispositivo correto encontrado geralmente era um nível RMS de ~1,7 e havia um mapeamento falso entre ALSA e PipeWire.

---

### Lista de tarefas (Sprint futuro)
1. **[ ] Integração WirePlumber:** Configuração de regras nativas do PipeWire (`scripts`), um fluxo permanente e ganchos `pactl` para vincular.
2. **[ ] Otimização de desempenho:** O loop de áudio é conectado (por exemplo, verificações RMS seltener durchführen ou VAD-Parameter otimizado).
3. **[ ] Native Mono Sink:** Sicherstellen, dass der virtudelle Sink systemweit fest auf 16kHz Mono steht, um Resampling-Last zu vermeiden.
4. **[ ] Mapeamento robusto de dispositivos:** Um método estável encontrado para um monitor-sink virtual em `sounddevice` nomeado para endereço.

---

### Atualizar `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[PT] Resumo:**
Tentativa de mesclar o áudio do microfone e da área de trabalho usando um `null-sink` virtual. O roteamento estava instável devido à restauração de fluxo do PipeWire. Foi observada alta carga de CPU. A lógica agora está documentada para uma iteração futura.

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.