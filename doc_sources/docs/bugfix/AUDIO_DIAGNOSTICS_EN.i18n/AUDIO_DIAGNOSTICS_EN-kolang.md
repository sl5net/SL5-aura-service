# AUDIO_DIAGNOSTICS_EN.md

# Aura용 Linux 오디오 진단


### 1. 장치 식별
Python 환경에 표시되는 모든 오디오 장치를 나열합니다.
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **찾을 사항:** 마이크의 **색인 번호** 및 **하드웨어 ID(hw:X,Y)**를 기록해 두세요.

### 2. 하드웨어는 누가 사용하고 있나요?
"장치 사용 중" 또는 "시간 초과" 오류가 발생하는 경우 현재 오디오 하드웨어를 잠그고 있는 프로세스(PID)를 확인하세요.
```bash
fuser -v /dev/snd/*
```
* **팁:** `pipewire` 또는 `wireplumber`가 표시되면 사운드 서버가 장치를 관리하고 있는 것입니다. PCM 장치에 `python3` 또는 `obs` PID가 직접 표시되면 해당 장치가 다른 장치를 차단하고 있을 수 있습니다.

### 3. 실시간 모니터링(PipeWire)
시스템이 PipeWire(최신 Manjaro의 표준)를 사용하는 경우 실시간 진단을 위한 최고의 도구입니다.
```bash
pw-top
```
* **찾을 사항:** `ERR` 열에서 드롭아웃을 확인하고 Aura(16000Hz) 및 OBS(48000Hz)가 CPU에 리샘플링 과부하를 일으키지 않는지 확인하세요.

### 4. 오디오 이벤트 모니터링
마이크가 음소거되거나 음소거 해제되거나 새 스트림이 생성되면 실시간 업데이트를 확인하세요.
```bash
pactl subscribe
```
* **사용법:** 이것을 실행한 다음 Aura를 시작하세요. 즉시 많은 '제거' 이벤트가 표시되면 프로세스가 중단되거나 거부되는 것입니다.

### 5. 하드웨어 바이패스 테스트
마이크가 원시 하드웨어 수준에서 작동하는지 테스트합니다(PulseAudio/PipeWire 우회). 5초 동안 오디오를 녹음합니다.
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **결과:** 이것이 작동하지만 Aura가 작동하지 않으면 문제는 하드웨어가 아닌 사운드 서버 구성에 있는 것입니다.

### 6. 긴급 재설정
오디오 시스템이 멈춘 경우:
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**더 쉬운 작업 흐름 힌트:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀