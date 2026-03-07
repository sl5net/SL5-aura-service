# SL5 Aura 시작하기

## SL5 아우라란 무엇인가요?

SL5 Aura는 음성을 텍스트(STT)로 변환하고 구성 가능한 규칙을 적용하여 출력을 정리, 수정 및 변환하는 오프라인 우선 음성 도우미입니다.

GUI 없이 작동합니다. 모든 것이 CLI 또는 콘솔을 통해 실행됩니다.

## 작동 방식

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk**는 음성을 원시 텍스트로 변환합니다.
2. **사전 지도** 맞춤법 검사 전에 텍스트를 정리하고 수정합니다.
3. **LanguageTool**은 문법과 철자를 수정합니다.
4. **포스트 맵**은 최종 변환을 적용합니다.
5. **출력**은 최종 깨끗한 텍스트(및 선택적으로 TTS)입니다.

## 첫 번째 단계

### 1. 아우라를 시작하세요
```bash
python main.py
```

### 2. 콘솔 입력으로 테스트
`s` 다음에 텍스트를 입력하세요.
```
s hello world
```

### 3. 실제 규칙 보기
`config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`를 엽니다.

내부 규칙의 주석 처리를 해제하고 다시 테스트하세요. 무슨 일이 일어나나요?

## 규칙 이해하기

규칙은 `FUZZY_MAP_pre.py` 또는 `FUZZY_MAP.py`라는 Python 파일의 `config/maps/`에 있습니다.

규칙은 다음과 같습니다.
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

**출력**이 먼저 나옵니다. 즉, 규칙이 생성하는 내용을 즉시 확인할 수 있습니다.

규칙은 **위에서 아래로** 처리됩니다. 첫 번째 전체 일치(`^...$`)는 모든 것을 중지합니다.

## Koans – 실천을 통한 학습

Koans는 `config/maps/koans_deutsch/` 및 `config/maps/koans_english/`의 작은 연습입니다.

각 공안은 하나의 개념을 가르칩니다.

| 고안 | 주제 |
|---|---|
| 01_koan_erste_schritte | 첫 번째 규칙, 전체 일치, 파이프라인 중지 |
| 02_koan_listen | 목록, 여러 규칙 |
| 03_koan_schwierige_namen | 어려운 이름, 발음 일치 |

Koan 01로 시작하여 작업을 진행하세요.

## 팁

- `FUZZY_MAP_pre.py`의 규칙은 철자 검사 **전에** 실행됩니다. - STT 오류 수정에 좋습니다.
- `FUZZY_MAP.py`의 규칙은 철자 검사 **후** 실행 – 형식 지정에 적합
- 변경 전에 백업 파일(`.peter_backup`)이 자동으로 생성됩니다.
- AI가 자동으로 koans를 처리하도록 하려면 `peter.py`를 사용하십시오.