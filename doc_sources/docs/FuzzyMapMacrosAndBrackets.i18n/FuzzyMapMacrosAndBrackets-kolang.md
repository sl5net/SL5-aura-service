# 퍼지 맵 매크로 및 브래킷 로직

Aura는 'FUZZY_MAP_pre.py' 파일에서 여러 사전 처리 규칙을 그룹화하여 '시작 규칙'이 트리거되면 응집력 있는 파이프라인으로 순차적으로 실행할 수 있도록 지원합니다. 이 문서에서는 이 기능의 디자인 철학, 구문 및 실행 흐름을 설명합니다.

## 핵심 디자인 원칙

1. **중복성 없음**: 그룹 내부의 규칙은 표준 Python 튜플로 유지됩니다.
`('replacement_text', r'regex_pattern', 임계값, flags_and_options)`
2. **이중 사용성**: 그룹 내의 개별 규칙은 완전히 기능하는 독립형 규칙입니다. 그룹이 트리거되지 않으면 상위 루프에서 정상적으로 평가됩니다.
3. **수동 종료 마커**: 그룹의 끝은 자체적으로는 일치하지 않는 수동 규칙 항목에 의해 정의됩니다. 이는 순전히 파서의 경계 표시 역할을 합니다.
4. **하이브리드 폴백(비일치 시 추가)**: 그룹이 활성화되면 모든 내부 규칙이 출력에 기여해야 합니다. 내부 규칙의 정규식이 텍스트와 일치하면 일반적인 대체가 발생합니다. 일치하지 않으면 대체 텍스트가 공백과 함께 현재 텍스트에 추가됩니다.

---

## 구문 및 구조

매크로 그룹은 `FUZZY_MAP_pre.py`의 **시작 규칙**과 **종료 규칙** 사이에 일련의 표준 규칙을 래핑하여 정의됩니다.

### 1. 시작 규칙
시작 규칙은 일치할 때 매크로를 트리거하는 표준 규칙입니다. 옵션 사전에 'group_start' 키가 포함되어 있습니다.
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. 내부 규칙
내부 규칙은 시작 규칙 뒤에 순차적으로 배치되는 표준 규칙입니다. 특별한 메타데이터가 필요하지 않습니다.
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. 종료 규칙(패시브 마커)
종료 규칙에는 옵션 사전에 `None` 대체, 빈 패턴 및 `'group_end'` 키가 있습니다.
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## 구체적인 예

다음은 `FUZZY_MAP_pre.py` 파일에 정의된 실제 테스트 사례입니다.

```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```

### 실행 흐름 시나리오:

* **시나리오 A(트리거된 매크로)**:
* 입력: `"start sandbox mit apfel"`
* 예상 흐름:
1. 시작 규칙은 `"start sandbox"`와 일치하여 이를 `"Sandbox:"` -> 현재 텍스트: `"Sandbox: mit apfel"`로 대체합니다.
2. `'sandbox_test'` 그룹이 트리거됩니다.
3. `"Sandbox: mit apfel"`에서 내부 규칙을 재귀적으로 실행합니다.
- 내부 규칙 1은 `"apfel"`과 일치하고 `"birne"`으로 대체됩니다. -> 현재 텍스트: `"Sandbox: mit birne"`.
- 내부 규칙 2는 `"banane"`과 일치하지 않습니다. 그룹이 활성화되어 있으므로 `"banane"`을 추가하는 것으로 대체됩니다. -> 현재 텍스트: `"Sandbox: mit birne banane"`.
4. 최종 텍스트 `"Sandbox: mit birne banane"`가 반환되고 LanguageTool에 의해 수정됩니다.
* 출력: `"샌드박스: mit Birne Banane"`

* **시나리오 B(트리거되지 않은 매크로 - 이중 유용성)**:
* 입력: `"ein apfel und eine kirsche"`
* 예상 흐름:
1. 시작 규칙이 일치하지 않습니다. ``sandbox_test'' 그룹은 비활성 상태로 유지됩니다.
2. 루프는 다음 규칙으로 진행됩니다.
3. **내부 규칙 1**: `"apfel"`과 일치하여 `"birne"`로 대체 -> 현재 텍스트: `"ein birne und eine kirsche"`.
4. **내부 규칙 2**: 일치하지 않습니다. 그룹이 트리거되지 않았으므로 규칙은 일반적인 독립형 규칙으로 작동하며 **아무 것도 추가되지 않습니다**.
5. 종료 규칙은 무시됩니다.
* 출력: `"ein birne und eine kirsche"`

---

## 기술 세부정보(고급설정)

* **격리된 재귀**: 그룹이 트리거되면 엔진은 `custom_rules=[inner_rule]`을 사용하여 `process_text_in_Background`를 반복적으로 호출합니다. 이를 통해 각 내부 규칙이 전체 동기 파이프라인 패스 내에서 실행될 수 있습니다.
* **성능 및 안정성 보호 장치**:
* **시퀀스 우회**: 내부 재귀 실행은 교착 상태 및 실행 지연을 방지하기 위해 `chunk_id` 시퀀스 큐를 우회합니다.
* **I/O 및 TTS 억제**: 재귀 실행은 중간 파일 쓰기 및 TTS 음성 출력을 억제하여 최종 안정화된 텍스트만 작성 및 음성화되도록 합니다.
* **안정성 보호**: 재귀 실행은 대체 추가 중에 무한 안정성 루프를 방지하기 위해 한 번의 반복 후에 엄격하게 중단됩니다.
* **안전한 종료**: 안정성 검사는 최대 반복 횟수(`MAX_ITERATIONS_FOR_SAFETY`)에 엄격하게 의존하여 무한 루프를 방지하고 합법적이고 느린 매크로 실행을 조기에 중단할 수 있는 시간 기반 조절을 우회합니다.
__CODE_BLOCK_4__