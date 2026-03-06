# 시스템 작업 흐름의 정확한 동작을 명확히 합니다.
XSPACEbreakX
### 통합 워크플로에 대한 설명 수정

**입력 변환** 및 **레이블링**에 대한 첫 번째 규칙은 두 번째 규칙에 의해 최종 검색 작업이 실행되기 전입니다.

#### 1. 입력: "was ist ein haus"

#### 2. 규칙 1: 라벨링/변환

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **조치:** 사용자 입력 `"was ist ein haus"`가 성공적으로 일치되었습니다.
* **결과(내부):** 시스템은 `"was ist ein haus (Begriffsklärung)"` 출력/라벨을 생성합니다.
* **계속:** `fullMatchStop`이 `skip_list`에 있으므로 규칙 일치는 **중지되지 않습니다**. 프로세스는 *변형된* 또는 *레이블이 지정된* 콘텐츠를 전달하는 다음 규칙으로 계속됩니다.

#### 3. 규칙 2: 일반 조치/실행

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **조치:** 이제 시스템은 이전 단계의 **현재 결과/라벨**, 즉 `"was ist ein haus (Begriffsklärung)"`과 일치할 가능성이 높습니다(또는 원래 입력과 일치하지만 실행된 스크립트는 변환된 라벨을 우선시합니다).
* **접두사 일치:** 접두사(`was ist`)는 여전히 일치합니다.
* **캡처 그룹:** 캡처 그룹 `(?P<search>.*)`는 문자열의 나머지 부분을 캡처합니다.
* 시스템이 **규칙 1 출력을 새 입력**으로 사용하는 경우 **`haus (Begriffsklärung)`**(또는 실행 스크립트에 의해 구문 분석되는 전체 변환 문자열)을 캡처합니다.
* **실행:** `wikipedia_local.py` 스크립트가 실행됩니다.

#### 4. 최종 조치:

* `wikipedia_local.py` 스크립트는 특별히 수정된 검색어/라벨을 받습니다.
* 스크립트는 의도된 용어 **`haus (Begriffsklärung)`**에 대한 Wikipedia 검색을 수행합니다.

**결론:**

이 설정은 모호하거나 일반적인 쿼리를 처리하는 우아한 방법입니다. 특정 규칙으로 입력을 수정하거나 대상 레이블을 생성한 다음 프로세스가 일반 검색 규칙을 계속하도록 함으로써 Wikipedia 검색이 일반적인 "haus"가 아닌 특정하고 명확한 항목인 **`haus (Begriffsklärung)`**에 대해 실행되도록 할 수 있습니다.

이는 범용 실행 규칙에 의해 실행되기 전에 첫 번째 규칙이 쿼리를 사전 처리하고 강화할 수 있도록 `fullMatchStop` 제외가 **필수**임을 확인합니다.

(sl5,4.12.'25 12:24 목)