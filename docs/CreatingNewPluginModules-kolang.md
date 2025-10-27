## 새로운 플러그인 모듈 생성

우리 프레임워크는 강력한 자동 검색 시스템을 사용하여 규칙 모듈을 로드합니다. 이를 통해 모든 새 구성요소를 수동으로 등록할 필요 없이 새 명령 세트를 간단하고 깔끔하게 추가할 수 있습니다. 이 가이드에서는 사용자 정의 모듈을 생성, 구성 및 관리하는 방법을 설명합니다.

### 핵심 개념: 폴더 기반 모듈

모듈은 단순히 `config/maps/` 디렉토리 내의 폴더입니다. 시스템은 자동으로 이 디렉터리를 검색하고 각 하위 폴더를 로드 가능한 모듈로 처리합니다.

### 모듈 생성을 위한 단계별 가이드

예를 들어 특정 게임에 대한 매크로를 보관하는 새 모듈을 만들려면 다음 단계를 따르세요.

**1. 지도 디렉토리로 이동**
모든 규칙 모듈은 프로젝트의 `config/maps/` 폴더에 있습니다.

**2. 모듈 폴더 생성**
새 폴더를 만듭니다. 이름은 설명적이어야 하며 공백 대신 밑줄을 사용해야 합니다(예: `my_game_macros`, `custom_home_automation`).

**3. 언어 하위 폴더 추가(중요 단계)**
새 모듈 폴더 내에서 지원하려는 각 언어에 대한 하위 폴더를 만들어야 합니다.

* **명명 규칙:** 이러한 하위 폴더의 이름은 **유효한 언어-로캘 코드여야 합니다**. 시스템은 이러한 이름을 사용하여 활성 언어에 대한 올바른 규칙을 로드합니다.
* **올바른 예:** `de-DE`, `en-US`, `en-GB`, `pt-BR`
* **경고:** `german` 또는 `english_rules`와 같은 비표준 이름을 사용하는 경우 시스템은 폴더를 무시하거나 별도의 비언어별 모듈로 처리합니다.

**4. 규칙 파일 추가**
규칙 파일(예: `FUZZY_MAP_pre.py`)을 적절한 언어 하위 폴더에 넣습니다. 가장 쉬운 시작 방법은 기존 언어 모듈 폴더의 내용을 복사하여 템플릿으로 사용하는 것입니다.

### 디렉터리 구조 예

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### 구성에서 모듈 관리

시스템은 최소한의 구성만 필요하도록 설계되었습니다.

#### 모듈 활성화(기본값)

모듈은 **기본적으로 활성화되어 있습니다**. `config/maps/`에 모듈 폴더가 존재하는 한 시스템은 이를 찾아 해당 규칙을 로드합니다. **새 모듈을 활성화하기 위해 설정 파일에 항목을 추가할 필요가 없습니다.**

#### 모듈 비활성화

모듈을 비활성화하려면 설정 파일 내의 `PLUGINS_ENABLED` 사전에 해당 항목을 추가하고 해당 값을 `False`로 설정해야 합니다.

**예(`config/settings.py`):**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True. Not False means True.
    # "wannweil": False,

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### 중요한 디자인 노트

* **기본 동작: 'True'와 동일한 항목이 없습니다**
모듈이 'PLUGINS_ENABLED' 사전에 나열되어 있지 않으면 기본적으로 **활성**으로 간주됩니다. 이 디자인은 예외만 나열하면 되므로 구성 파일을 깨끗하게 유지합니다.

* **활성화의 약어**
또한 구성 시스템은 값 없이 모듈 키를 나열하면 모듈 키가 활성화되었음을 의미한다는 것을 이해합니다. 예를 들어 사전에 `"wannweil"`을 추가하는 것은 `"wannweil": True`를 추가하는 것과 같습니다. 이는 모듈 활성화에 대한 편리한 단축어를 제공합니다.

* **상위 모듈 비활성화:** 의도된 동작은 상위 모듈을 비활성화하면   를 수행해야 한다는 것입니다.
모든 하위 모듈과 언어 하위 폴더를 자동으로 비활성화합니다. 예를 들어 `"standard_actions": False`를 설정하면 `de-DE`와 `en-US`가 모두 로드되지 않습니다. (27.10.'25 월)
XSPACEbreakX
*   **목표**
목표는 이 시스템을 더욱 강화하는 것입니다. 예를 들어, 상위 모듈이 비활성화된 경우에도 하위 모듈 설정을 준수할 수 있는 방법을 제공하거나 더 복잡한 상속 규칙을 도입합니다. (27.10.'25 월)