# Versão alemã: `AUDIO_DIAGNOSTICS_DE.md`

# Diagnóstico de áudio Linux para Aura

A ativação do Aura Service pode incluir controle de áudio (tempos limite, "dispositivo ocupado" ou controle de taxa de amostragem). Diese Befehle helfen bei der Fehlersuche.

### 1. Geräte identifizieren
Zeigt alle Audio-Geräte aus Sicht der Python-Ugebung an:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ziel:** Notifique o **Número de índice** e o **ID de hardware (hw:X,Y)** deines Mikrofons.

### 2. Você perdeu o hardware?
Se você estiver usando "Device Busy" ou "Timeout", verifique se o processo (PID) do hardware está bloqueado:
```bash
fuser -v /dev/snd/*
```
* **Dica:** Se `pipewire` ou `wireplumber` for instalado, o servidor de som é usado. Quando um `python3` ou `obs` PID diretamente em um dispositivo PCM é instalado, ele bloqueia esse evtl. den Zugriff para outros.

### 3. Monitoramento de Echtzeit (PipeWire)
Para o sistema Manjaro moderno com PipeWire é a ferramenta mais importante:
```bash
pw-top
```
* **Ziel:** Verifique o intervalo `ERR` em Fehler e stelle sicher, dass Aura (16000Hz) e OBS (48000Hz) sem duração de CPU durante a reamostragem.

### 4. Supervisão de eventos de áudio
Transmita ao vivo quando o microfone estiver bloqueado ou novos fluxos forem incluídos:
__CODE_BLOCO_3__
* **Anwendung:** Starte morre e dann Aura. Quando houver `remove`-Events com sucesso, abra um processo ab ou oder wird vom System abgewiesen.

### 5. Teste direto de hardware
Testado, o Mikrofon tem funcionalidade de hardware (incluindo PulseAudio/PipeWire). Até 5 segundos depois:
```bash
pactl subscribe
```
* **Ergebnis:** Se o funcionamento for executado, Aura não é, como o problema na configuração dos servidores de som, não no hardware.

### 6. Redefinição de não queda
Quedas do sistema de áudio completo:
__CODE_BLOCO_5__

---

**Dicas para o fluxo de trabalho:** Para começar diretamente no Kate, escolha um `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` e o primeiro. 🌵🚀