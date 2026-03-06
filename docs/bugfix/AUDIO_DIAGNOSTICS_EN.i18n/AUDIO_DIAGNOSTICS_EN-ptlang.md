# AUDIO_DIAGNOSTICS_EN.md

# Diagnóstico de áudio Linux para Aura


### 1. Identificação de dispositivos
Liste todos os dispositivos de áudio vistos pelo ambiente Python:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **O que procurar:** Anote o **Número de índice** e **ID de hardware (hw:X,Y)** do seu microfone.

### 2. Quem está usando o hardware?
Se você receber erros de "Dispositivo ocupado" ou "Tempo limite", verifique qual processo (PID) está bloqueando o hardware de áudio:
```bash
fuser -v /dev/snd/*
```
* **Dica:** Se você vir `pipewire` ou `wireplumber`, o servidor de som está gerenciando o dispositivo. Se você vir um PID `python3` ou `obs` diretamente em um dispositivo PCM, eles podem estar bloqueando outros.

### 3. Monitoramento em tempo real (PipeWire)
Se o seu sistema usa PipeWire (padrão no Manjaro moderno), esta é a melhor ferramenta para diagnóstico ao vivo:
```bash
pw-top
```
* **O que procurar:** Verifique se há falhas na coluna `ERR` e verifique se Aura (16.000 Hz) e OBS (48.000 Hz) não estão causando sobrecarga de reamostragem na CPU.

### 4. Monitoramento de eventos de áudio
Veja atualizações ao vivo quando os microfones são desativados ou ativados ou quando novas transmissões são criadas:
__CODE_BLOCO_3__
* **Uso:** Execute isto e então inicie o Aura. Se você vir muitos eventos `remove` imediatamente, um processo está travando ou sendo rejeitado.

### 5. Teste de desvio de hardware
Teste se o seu microfone funciona em nível de hardware bruto (ignorando PulseAudio/PipeWire). Isso grava 5 segundos de áudio:
```bash
pactl subscribe
```
* **Resultado:** Se isso funcionar, mas o Aura não, o problema está na configuração do Sound-Server, não no hardware.

### 6. Reinicialização de emergência
Se o sistema de áudio estiver travado:
__CODE_BLOCO_5__


**sugestão de fluxo de trabalho mais fácil:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` e então. 🌵🚀