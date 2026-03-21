# 규칙 속성: `only_in_windows` 및 `exclude_windows`

이 두 속성은 **규칙이 실행될 수 있는 활성 창**을 제어합니다.
규칙의 '옵션' 사전 내에 정의되며 **정규식 패턴 목록**을 허용합니다.
현재 활성 창 제목(`_active_window_title`)과 일치합니다.

---

## `windows 내에서만`

규칙은 **활성 창 제목이 지정된 패턴 중 **적어도 하나**와 일치하는 경우에만 실행됩니다.
다른 모든 창은 무시됩니다.

**사용 사례:** 규칙을 특정 애플리케이션으로 제한합니다.


> 이 규칙은 Firefox 또는 Chromium이 활성 창일 때만 **만** 실행됩니다.

---

## `exclude_windows`

활성 창 제목이 주어진 패턴 중 **적어도 하나**와 일치하지 않는 **경우** 규칙이 실행됩니다.
일치하는 창을 건너뜁니다.

**사용 사례:** 특정 애플리케이션에 대한 규칙을 비활성화합니다.

예

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



일치는 **대소문자를 구분하지 않으며** Python **정규 표현식**을 사용합니다.

---

## 요약

| 속성 | 다음과 같은 경우에 발생합니다... |
|------|------------------|
| `only_in_windows` | 창 제목 **일치** 패턴 중 하나 |
| `제외_창` | 창 제목이 어떤 패턴과도 **일치하지 않습니다** |

---

## 참고하세요

- `scripts/py/func/process_text_in_Background.py` — 라인 ~1866 및 ~1908
- `scripts/py/func/get_active_window_title.py` — 창 제목을 검색하는 방법