# Correção de bug: distorção de áudio e travamento do PipeWire (Linux)

Este documento descreve como resolver distorções de áudio ("klirren"), artefatos de voz robótica e travamentos de áudio do sistema que podem ocorrer ao usar o **SL5-aura-service** junto com outros aplicativos de mídia como OBS, AnyDesk ou fluxos TTS de alta frequência.

## Sintomas
- A saída/entrada de voz soa distorcida, metálica ou "cliring".
- O áudio do sistema trava com a mensagem: `Estabelecendo conexão com PulseAudio` ou `Aguarde`.
- Perda total de áudio após alta carga de CPU ou uso de stream simultâneo.
- Os registros do diário mostram: `spa.alsa: hw:X: snd_pcm_status error: Esse dispositivo não existe`.

## Causa raiz
No Manjaro e em outras distribuições Linux modernas, o **PipeWire** gerencia o áudio. A distorção geralmente decorre de:
1. **Buffer Underruns:** Conflito entre streams simultâneos (por exemplo, AnyDesk capturando áudio enquanto o TTS/OBS está em execução).
2. **Incompatibilidade de taxa de amostragem:** Troca frequente entre 44,1kHz e 48kHz.
3. **Problemas de temporização de USB:** Alta carga de barramento fazendo com que fones de ouvido USB (como Plantronics/Poly) se desconectem temporariamente.

---

## Soluções

### 1. Recuperação Imediata (A Reinicialização "Nuclear")
Se a pilha de áudio estiver congelada ou distorcida, elimine todos os processos relacionados ao áudio. Eles serão reiniciados automaticamente imediatamente.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. Configurações de prevenção e estabilidade

#### Desativar áudio AnyDesk
AnyDesk frequentemente tenta se conectar ao dispositivo de áudio, causando conflitos de hardware.
- **Ação:** Abra Configurações do AnyDesk -> **Áudio** -> Desative **"Transmitir áudio"** e **"Reproduzir áudio"**.

#### Corrigir taxa de amostragem do PipeWire (recomendado)
Force o PipeWire a permanecer em 48kHz para evitar artefatos de reamostragem durante a reprodução do TTS.

1. Crie o diretório de configuração: `mkdir -p ~/.config/pipewire`
2. Copie a configuração padrão: `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. Edite `~/.config/pipewire/pipewire.conf` e defina:
   ```conf
   default.clock.rate = 48000
   ```
4. Reinicie os serviços:
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. Recuperação pós-produção (FFmpeg)
Se você gravou uma sessão e o áudio está distorcido ("cliring"), use a seguinte cadeia de filtros `ffmpeg` para reparar o arquivo.

### Comando de reparo recomendado
Este comando aplica um descortador, redução de ruído e um filtro passa-baixa para remover artefatos digitais de alta frequência sem recodificar o vídeo.

testado e muito bom:

__CODE_BLOCO_3__

pode ser melhor com (não testado):

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```



não testado:
__CODE_BLOCO_5__




**Detalhamento do filtro:**
- `adeclip`: Arredonda os picos de recorte digital.
- `afftdn`: Reduz o ruído digital baseado em FFT.
- `lowpass=f=3500`: Corta frequências acima de 3,5kHz onde ocorre a maior parte do "cliring" (torna a voz mais clara/quente).
- `volume=1.8`: Compensa a perda de volume durante a filtragem.
- `-c:v copy`: Mantém a qualidade original do vídeo (extremamente rápido).

---

## Ferramentas de depuração
Para monitorar a integridade do áudio em tempo real durante o desenvolvimento:
- `pw-top`: Mostra erros em tempo real (coluna ERR) e status do buffer.
- `journalctl --user -u pipewire`: Verifica se há desconexões de hardware.