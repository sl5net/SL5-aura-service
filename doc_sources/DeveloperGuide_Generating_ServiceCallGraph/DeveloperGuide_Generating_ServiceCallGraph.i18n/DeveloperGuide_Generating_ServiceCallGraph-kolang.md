# 개발자 가이드: 서비스 호출 그래프 생성

이 문서에서는 장기 실행 `aura_engine.py`의 시각적 호출 그래프를 생성하기 위한 강력하고 스레드로부터 안전한 방법을 설명합니다. 우리는 'yappi' 프로파일러(멀티스레딩 지원용)와 시각화를 위해 'gprof2dot'를 사용합니다.

### 전제 조건

전역적으로 또는 가상 환경에 필요한 도구가 설치되어 있는지 확인하세요.

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### 1단계: 프로파일링을 위한 서비스 수정

`yappi` 프로파일러를 수동으로 시작하고 중단 시 프로파일링 데이터를 정상적으로 저장하려면(`Ctrl+C`) `aura_engine.py` 스크립트를 수정해야 합니다.

**`aura_engine.py`의 주요 변경 사항:**

1. **가져오기 및 신호 처리기:** `yappi`를 가져오고 `generate_graph_on_interrupt` 함수(이전에 구현된 대로)를 정의하여 `yappi.stop()` 및 `stats.save(...)`를 호출합니다.
2. **시작/중지:** `if __name__ == "__main__":` 블록 내에 `yappi.start()` 및 `signal.signal(signal.SIGINT, ...)`를 추가하여 `main(...)` 실행을 래핑합니다.

### 2단계: 서비스 실행 및 데이터 수집

수정된 스크립트를 직접 실행하고 충분한 시간(예: 10-20초) 동안 데이터를 처리하여 스레드된 기능(예: LanguageTool 수정)을 포함한 모든 핵심 기능이 호출되도록 합니다.

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

**Ctrl+C**를 한 번 눌러 신호 처리기를 트리거합니다. 이렇게 하면 프로파일러가 중지되고 원시 데이터가 다음 위치에 저장됩니다.

`\mathbf{yappi\_profile\_data.prof`

### 3단계: 시각적 그래프 생성 및 필터링

우리는 `gprof2dot`을 사용하여 원시 `pstats` 데이터를 SVG 형식으로 변환합니다. `--include` 및 `--threshold`와 같은 고급 필터링 옵션은 특정 환경에서 지원되지 않을 수 있으므로 기본 **`--strip`** 필터를 사용하여 경로 정보를 정리하고 시스템 내부의 혼란을 줄입니다.

**시각화 명령을 실행합니다:**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### 4단계: 문서화(수동 자르기)

결과 `yappi_call_graph_stripped.svg`(또는 `.png`) 파일은 크지만 모든 스레드를 포함한 전체 실행 흐름을 정확하게 포함합니다.

문서화 목적으로 **이미지를 수동으로 잘라서** 중앙 논리(10~20개 핵심 노드 및 해당 연결)에 초점을 맞춰 저장소 문서화에 대한 집중적이고 읽기 쉬운 호출 그래프를 만듭니다.

### 아카이빙 중

수정된 구성 파일과 최종 호출 그래프 시각화는 문서 소스 디렉터리에 보관되어야 합니다.

| 유물 | 위치 |
| :--- | :--- |
| **수정된 서비스 파일** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **최종 자른 이미지** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **원시 프로파일링 데이터** | *(선택사항: 최종 저장소 문서에서 제외되어야 함)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")