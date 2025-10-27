# 고급 규칙 작업: Python 스크립트 실행

이 문서에서는 사용자 정의 Python 스크립트를 실행하여 간단한 텍스트 교체 규칙의 기능을 확장하는 방법을 설명합니다. 이 강력한 기능을 사용하면 동적 응답을 만들고, 파일과 상호 작용하고, 외부 API를 호출하고, 음성 인식 워크플로 내에서 직접 복잡한 논리를 구현할 수 있습니다.

## 핵심 개념: `on_match_exec`

단순히 텍스트를 바꾸는 대신, 이제 패턴이 일치할 때 하나 이상의 Python 스크립트를 실행하도록 규칙에 지시할 수 있습니다. 이는 규칙의 옵션 사전에 `on_match_exec` 키를 추가하여 수행됩니다.

스크립트의 주요 작업은 일치 항목에 대한 정보를 받고, 작업을 수행하고, 새 텍스트로 사용될 최종 문자열을 반환하는 것입니다.

### 규칙 구조

스크립트 작업이 포함된 규칙은 다음과 같습니다.

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**핵심 사항:**
- `on_match_exec` 값은 **목록**이어야 합니다.
- 스크립트는 맵 파일과 동일한 디렉터리에 위치하므로 `CONFIG_DIR / 'script_name.py'`가 경로를 정의하는 데 권장되는 방법입니다.

---

## 실행 가능한 스크립트 만들기

시스템이 스크립트를 사용하려면 다음 두 가지 간단한 규칙을 따라야 합니다.
1. 유효한 Python 파일(예: `my_script.py`)이어야 합니다.
2. `execute(match_data)`라는 함수를 포함해야 합니다.

### `execute(match_data)` 함수

이는 모든 실행 가능한 스크립트의 표준 진입점입니다. 규칙이 일치하면 시스템이 자동으로 이 함수를 호출합니다.

- **`일치_데이터`(dict):** 일치에 대한 모든 컨텍스트를 포함하는 사전입니다.
- **반환 값(str):** 함수는 **반드시** 문자열을 반환해야 합니다. 이 문자열은 새로 처리된 텍스트가 됩니다.

### `match_data` 사전

이 사전은 기본 애플리케이션과 스크립트 사이의 다리 역할을 합니다. 여기에는 다음 키가 포함되어 있습니다.

* ``original_text'` (str): 현재 규칙의 대체가 적용되기 *전* 전체 텍스트 문자열입니다.
* ``text_after_replacement'` (str): 규칙의 기본 대체 문자열이 적용된 *이후* 텍스트이지만 스크립트가 호출되기 *이전*입니다. (대체 항목이 `None`인 경우 `original_text`와 동일합니다.)
* ``regex_match_obj'` (re.Match): 공식 Python 정규식 일치 개체입니다. 이는 **캡처 그룹**에 액세스하는 데 매우 강력합니다. `match_obj.group(1)`, `match_obj.group(2)` 등을 사용할 수 있습니다.
* ``rule_options'`(dict): 스크립트를 트리거한 규칙에 대한 전체 옵션 사전입니다.

---

## 예

### 예시 1: 현재 시간 가져오기(동적 응답)

이 스크립트는 하루 중 시간을 기준으로 개인화된 인사말을 반환합니다.

**1. 규칙(지도 파일에 있음):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. 스크립트(`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**용법:**
> **입력:** "지금은 몇 시야?"
> **출력:** "안녕하세요! 현재 14시 30분입니다."

### 예 2: 간단한 계산기(캡처 그룹 사용)

이 스크립트는 정규식의 캡처 그룹을 사용하여 계산을 수행합니다.

**1. 규칙(지도 파일에 있음):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2. 스크립트(`calculator.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**용법:**
> **입력:** "55 더하기 10을 계산하세요"
> **출력:** "결과는 65입니다."

### 예시 3: 영구 쇼핑 목록(파일 I/O)

이 예에서는 사용자의 원본 텍스트를 검사하여 하나의 스크립트가 여러 명령(추가, 표시)을 처리하는 방법과 파일에 기록하여 데이터를 유지하는 방법을 보여줍니다.

**1. 규칙(지도 파일에 있음):**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2. 스크립트(`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**용법:**
> **입력 1:** "쇼핑 목록에 우유 추가"
> **출력 1:** "알겠습니다. 쇼핑 목록에 '우유'를 추가했습니다."
>
> **입력 2:** "쇼핑 목록 표시"
> **출력 2:** "당신이 가지고 있는 목록에는 우유가 있습니다."

---

## 모범 사례

- **스크립트당 하나의 작업:** 스크립트의 초점을 단일 작업에 유지합니다(예: `calculator.py`는 계산만 합니다).
- **오류 처리:** 전체 애플리케이션이 충돌하는 것을 방지하려면 항상 스크립트의 논리를 'try...out' 블록으로 감싸세요. `제외` 블록에서 사용자에게 친숙한 오류 메시지를 반환합니다.
- **외부 라이브러리:** 외부 라이브러리(예: `requests` 또는 `wikipedia-api`)를 사용할 수 있지만 Python 환경(`pip install <library-name>`)에 설치되어 있는지 확인해야 합니다.
- **보안:** 이 기능은 모든 Python 코드를 실행할 수 있다는 점에 유의하세요. 신뢰할 수 있는 소스의 스크립트만 사용하세요.