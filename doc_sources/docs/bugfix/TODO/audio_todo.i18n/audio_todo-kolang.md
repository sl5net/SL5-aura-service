31.12.'25 18:25 수

Zusammenfassung 및 Zukunft를 위한 To-Do Liste:

### 문서: Versuch "통합 오디오 입력"(마이크 + 데스크톱)
**상태:** Pausiert(개념 증명 존재, aber nicht stable/performant).

**Erfahrungen / 조사 결과:**
* **라우팅:** PipeWire/PulseAudio는 Python-Stream(ALSA-Bridge)에서 표준-Mikrofon zurückzusetzen(Stream-Restore-Logik)에 대한 물리적인 내용을 확인합니다.
* **성능:** Die Verarbeitung von RMS, VAD und Vosk in einem engen Loop, kombiniert mit externen `pactl`-Aufrufen, führt zu hoher CPU-Last(Lüfterdrehen).
* **신호:** Trotz korrektem Device-Index kam은 종종 RMS-Pegel von ~1.7에 속하며, zwischen ALSA 및 PipeWire Hindeutet의 매핑에 오류가 있었습니다.

---

### 할 일 목록(퓨처 스프린트)
1. **[ ] WirePlumber 통합:** Erforschung von Nativen PipeWire-Rules(`scripts`), 음 덴 스트림 영구 ohne `pactl`-Hooks zu binden.
2. **[ ] 성능 최적화:** Den Audio-Loop enlasten(z.B. RMS-Checks seltener durchführen oder VAD-Parameter optimieren).
3. **[ ] 네이티브 모노 싱크:** Sicherstellen, dass der德lle Sink systemweit fest auf 16kHz Mono steht, um Resampling-Last zu vermeiden.
4. **[ ] 강력한 장치 매핑:** 안정된 방법으로 'sounddevice'에 있는 Monitor-Sink를 찾을 수 있습니다.

---

### `config/settings.py` 업데이트
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[KO] 요약:**
가상 `null-sink`를 사용하여 마이크와 데스크탑 오디오를 병합하려고 시도했습니다. PipeWire의 스트림 복원으로 인해 라우팅이 불안정했습니다. 높은 CPU 부하가 관찰되었습니다. 이제 향후 반복을 위해 논리가 문서화되었습니다.

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer Performanteren Lösung(vielleicht direct über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.