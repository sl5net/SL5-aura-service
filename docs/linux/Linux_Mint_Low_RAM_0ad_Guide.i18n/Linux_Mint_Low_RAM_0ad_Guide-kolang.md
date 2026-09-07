# RAM이 적은 시스템에서 Aura 음성 제어로 0 A.D. 실행(Linux Mint)

이 가이드는 레거시 또는 메모리가 제한된 Linux Mint 하드웨어에서 **0 A.D.**와 함께 **sl5net Aura** 음성 제어를 실행하기 위한 설정 및 메모리 최적화를 문서화합니다.

## 대상 하드웨어 및 시스템 프로필
- **장치**: Lenovo ThinkPad T520(노트북)
- **CPU**: Intel Core i7-2620M(듀얼 코어 @ 2.70GHz - 3.40GHz)
- **메모리**: 5.67GiB RAM
- **스왑**: 4GiB 유효 스왑
- **운영 체제**: Linux Mint 21.3 Virginia(64비트)
- **데스크톱 환경**: Cinnamon 6.0.5 (X11 디스플레이 서버)
- **적용대상** : 서기 0년 (Empires Ascendant)

## 메모리 관리 및 아키텍처
6GiB RAM 이하의 시스템에서 무거운 데스크톱 환경, 3D RTS 게임(A.D.) 및 음성 인식을 동시에 실행하려면 엄격한 메모리 보호가 필요합니다.

1. **Vosk 음성 모델 우선순위**:
- 낮은 메모리 공간(~300-500MB)을 위해 `vosk-model-small-de`(또는 이에 상응하는 언어)를 사용합니다.
- 게임 플레이 중 실시간 명령 응답성을 보장하기 위해 Vosk 모델 보존이 우선시됩니다.

2. **자동 언어 도구 제거**:
- LanguageTool의 Java 프로세스는 ~1.34 GiB RSS를 사용할 수 있습니다.
- 사용 가능한 RAM이 'CRITICAL_THRESHOLD_MB'(2.0GiB) 아래로 떨어지면 Aura의 'model_manager'는 즉시 LanguageTool을 종료하여 게임에 ~1.3GiB RAM을 확보합니다.
- 5분의 쿨다운(`set_언어_tool_cooldown`)은 활성 게임플레이 중에 LanguageTool이 다시 시작되거나 메모리가 스래싱되는 것을 방지합니다.

## 확인 명령
시스템 메모리 및 프로세스 상태를 검사하려면:
# 메모리 및 스왑 사용량 확인
```bash
free -h
```

# LanguageTool 프로세스가 제거되었는지 확인
```bash
ps aux | grep -i "[l]anguagetool"
```