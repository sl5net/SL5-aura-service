# 녹화 오버레이(화면 표시)

녹음 오버레이는 받아쓰기 상태에 대한 즉각적인 크로스 플랫폼 시각적 표시기를 제공합니다. 이는 데스크톱 알림 데몬 및 "방해 금지" 필터와 독립적으로 작동하여 기본 화면에 직접 상태를 표시합니다.

## 시각적 예

| 왼쪽 아래(`bl`) | 오른쪽 상단(`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *어두운 패널과 시스템 트레이에 잘 어울림* | *밝거나 복잡한 창문에 비해 높은 대비* |

## 상태

- **녹음 중(`🔴`)**: 윤곽선이 강조 표시된 선명한 빨간색 원(`#181818`의 `#e62222`)은 활성 오디오 녹음을 나타냅니다.
- **유휴 상태**:
- `hidden`(기본값): 창이 완전히 닫혀 정상적인 상호 작용을 위한 데스크톱 공간이 확보됩니다.
- `pentagon`: 유휴 모드 동안 미묘한 기하학적 오각형 배지(`⬟`)를 표시합니다.

## 구성

설정은 `config/settings.py`에서 관리됩니다.

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

## 건축학

- Python 표준 라이브러리(`tkinter`)를 사용하여 구축되었으며 외부 C 종속성이 전혀 필요하지 않습니다.
- 스레드로부터 안전한 대기열 이벤트 처리를 통해 백그라운드 데몬 스레드에서 실행됩니다.
- 다중 디스플레이 환경에서 기본 모니터를 동적으로 감지합니다.

(s, 10.9.'26 14:41 목)