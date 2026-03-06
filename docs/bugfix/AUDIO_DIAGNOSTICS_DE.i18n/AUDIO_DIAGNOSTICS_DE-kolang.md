# 독일어 버전: `AUDIO_DIAGNOSTICS_DE.md`

# Aura에 대한 Linux 오디오 진단

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten(Timeouts, "Device Busy" oder Sample-Rate-Konflikte). Diese Befehle helfen bei der Fehlersuche.

### 1. 식별 정보 확인
Zeigt alle Audio-Geräte aus Sicht der Python-Umgebung 및:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ziel:** Notiere die **Index-Nummer** 및 die **Hardware-ID(hw:X,Y)**는 Mikrofons를 정의합니다.

### 2. 하드웨어를 소홀히 했나?
Wenn Fehler는 "Device Busy" 또는 "Timeout"을 통해 PID(welcher Prozess) 다이 하드웨어 차단 기능을 제공합니다.
```bash
fuser -v /dev/snd/*
```
* **팁:** Wenn `pipewire` oder `wireplumber` erscheint, verwaltet der Sound-Server das Gerät. Wenn eine `python3` oder `obs` PID direkt auf einem PCM-Gerät erscheint, blockieren diese evtl. den Zugriff für andere.

### 3. Echtzeit 모니터링(PipeWire)
PipeWire ist dies das wichtigste 도구를 통해 현대적인 Manjaro 시스템을 위한 도구:
```bash
pw-top
```
* **Ziel:** Prüfe die Spalte `ERR` auf Fehler und stelle sicher, dass Aura(16000Hz) 및 OBS(48000Hz) keine CPU-Überlastung durch Resampling verursachen.

### 4. Überwachung von 오디오 이벤트
Verfolge live, wenn Mikrofone stummgeschaltet werden oder neue Streams entstehen:
```bash
pactl subscribe
```
* **안웬둥:** 스타테가 죽고 아우라가 죽습니다. Wenn sofort viele `remove`-이벤트 kommen, bricht ein Prozess ab oder wird vom System abgewiesen.

### 5. 하드웨어 직접 테스트
Testet, Ob das Mikrofon auf Hardware-Ebene 기능(PulseAudio/PipeWire). Nimmt 5 Sekunden auf:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Ergebnis:** Wenn dies funktioniert, Aura aber nicht, liegt das Problem in der Konfiguration des Sound-Servers, nicht an der Hardware.

### 6. 낙하 재설정
Falls das Audio-System 구성 요소:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**작업 흐름에 대한 팁:** Um Ausgaben은 Kate zu betrachten, hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` 및 den Befehl an에서 지시합니다. 🌵🚀