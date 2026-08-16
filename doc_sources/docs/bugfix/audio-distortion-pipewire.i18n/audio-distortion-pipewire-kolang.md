# 버그 수정: 오디오 왜곡 및 PipeWire 중단(Linux)

이 문서에서는 OBS, AnyDesk 또는 고주파수 TTS 스트림과 같은 다른 미디어 애플리케이션과 함께 **SL5-aura-service**를 사용할 때 발생할 수 있는 오디오 왜곡("klirren"), 로봇 음성 아티팩트 및 시스템 오디오 중단을 해결하는 방법을 설명합니다.

## 증상
- 음성 출력/입력 소리가 왜곡되거나 금속성 또는 "클리링"으로 들립니다.
- 'PulseAudio 연결 설정 중' 또는 '잠시 기다려주세요'라는 메시지와 함께 시스템 오디오가 중단됩니다.
- 높은 CPU 부하 또는 동시 스트림 사용 후 총 오디오 손실.
- 저널 로그에는 `spa.alsa: hw:X: snd_pcm_status error: No such device`가 표시됩니다.

## 근본 원인
Manjaro 및 기타 최신 Linux 배포판에서는 **PipeWire**가 오디오를 관리합니다. 왜곡은 일반적으로 다음에서 비롯됩니다.
1. **버퍼 언더런:** 동시 스트림 간의 충돌(예: TTS/OBS가 실행되는 동안 AnyDesk가 오디오를 캡처함)
2. **샘플링 속도 불일치:** 44.1kHz와 48kHz 사이를 자주 전환합니다.
3. **USB 타이밍 문제:** 높은 버스 부하로 인해 USB 헤드셋(예: Plantronics/Poly)의 연결이 일시적으로 끊어집니다.

---

## 솔루션

### 1. 즉시 복구("핵" 재설정)
오디오 스택이 고정되거나 왜곡되면 모든 오디오 관련 프로세스를 종료합니다. 즉시 자동으로 다시 시작됩니다.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. 예방 및 안정성 설정

#### AnyDesk 오디오 비활성화
AnyDesk는 종종 오디오 장치에 연결하려고 시도하여 하드웨어 충돌을 일으킵니다.
- **작업:** AnyDesk 설정 열기 -> **오디오** -> **"오디오 전송"** 및 **"오디오 재생"**을 비활성화합니다.

#### PipeWire 샘플링 속도 수정(권장)
TTS 재생 중에 리샘플링 아티팩트를 방지하려면 PipeWire를 48kHz로 유지하세요.

1. 구성 디렉터리를 생성합니다: `mkdir -p ~/.config/pipewire`
2. 기본 구성 `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`를 복사합니다.
3. `~/.config/pipewire/pipewire.conf`를 편집하고 다음을 설정합니다.
   ```conf
   default.clock.rate = 48000
   ```
4. 서비스 다시 시작:
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. 제작 후 복구(FFmpeg)
세션을 녹음했는데 오디오가 왜곡("클리링")된 경우 다음 `ffmpeg` 필터 체인을 사용하여 파일을 복구하세요.

### 권장 복구 명령
이 명령은 디클리퍼, 노이즈 감소 및 저역 통과 필터를 적용하여 비디오를 다시 인코딩하지 않고도 고주파수 디지털 아티팩트를 제거합니다.

테스트를 거쳤으며 매우 좋습니다.

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

다음을 사용하면 더 나을 수 있습니다(테스트되지 않음).

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



테스트되지 않음:
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**필터 분석:**
- `adeclip`: 디지털 클리핑 스파이크를 반올림합니다.
- `afftdn`: FFT 기반 디지털 노이즈를 줄입니다.
- `lowpass=f=3500`: 대부분의 "클리링"이 발생하는 3.5kHz 이상의 주파수를 차단합니다(목소리를 더 선명하고/따뜻하게 만듭니다).
- `volume=1.8`: 필터링 중 볼륨 손실을 보상합니다.
- `-c:v copy`: 원본 비디오 품질을 유지합니다(매우 빠름).

---

## 디버깅 도구
개발 중에 실시간으로 오디오 상태를 모니터링하려면:
- `pw-top`: 실시간 오류(ERR 열) 및 버퍼 상태를 표시합니다.
- `journalctl --user -u Pipewire`: 하드웨어 연결 끊김을 확인합니다.