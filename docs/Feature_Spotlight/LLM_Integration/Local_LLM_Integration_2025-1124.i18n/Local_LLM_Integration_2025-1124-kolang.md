# 🧠 SL5 Aura 하이브리드 모드: 로컬 LLM 통합

**상태:** 실험적/안정적
**기술:** Ollama(Llama 3.2) + Python 하위 프로세스
**개인정보 보호:** 100% 오프라인

## 컨셉: "건축가 & 인턴"

전통적으로 Aura는 빠르고 정확하며 예측 가능한 결정론적 규칙(RegEx)을 사용합니다. **"건축가"**입니다. 그러나 사용자가 *"농담을 말해 보세요"* 또는 *"이 텍스트를 요약해 주세요"*와 같이 "모호한" 또는 창의적인 내용을 묻고 싶어하는 경우도 있습니다.

**로컬 LLM 플러그인**(**"인턴"**)이 여기에 포함됩니다.
1. **Aura(RegEx)**는 먼저 모든 엄격한 명령("조명 켜기", "앱 열기")을 확인합니다.
2. **AND**/ **또는** 특정 유발 단어(예: "Aura ...")와 일치하는 항목이 없으면 대체 규칙이 활성화됩니다.
3. 텍스트가 로컬 AI 모델(Ollama)로 전송됩니다.
4. 응답은 TTS 또는 텍스트 입력을 통해 삭제되고 출력됩니다.

---

## 🛠 전제 조건

플러그인을 사용하려면 머신에서 로컬로 작동하는 실행 중인 [Ollama](https://ollama.com/) 인스턴스가 필요합니다.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 구조 및 로드 순서

플러그인은 의도적으로 `z_fallback_llm` 폴더에 배치됩니다.
Aura는 플러그인을 **알파벳순으로** 로드하므로 이 이름을 지정하면 LLM 규칙이 **마지막** 로드됩니다. 인식할 수 없는 명령에 대한 "안전망" 역할을 합니다.

**경로:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. 지도(`FUZZY_MAP_pre.py`)

우리는 **높은 점수(100)**와 유발 단어를 사용하여 Aura가 스크립트에 제어권을 넘겨주도록 합니다.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. 핸들러(`ask_ollama.py`)

이 스크립트는 Ollama CLI와 통신합니다.
**중요:** `clean_text_for_typing` 함수가 포함되어 있습니다. 원시 LLM 출력에는 `xdotool` 또는 레거시 TTS 시스템과 같은 도구를 충돌시킬 수 있는 이모티콘(😂, 🚀)이나 특수 문자가 포함되는 경우가 많습니다.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ 사용자 정의 옵션

### 트리거 변경
"Aura"를 깨우기 단어로 사용하지 않으려면 `FUZZY_MAP_pre.py`에서 RegEx를 수정하세요.
* 진정한 Catch-All의 예(Aura가 모르는 모든 것): `r'^(.*)$'` (주의: 점수를 조정하세요!)

### 모델 교체
`ask_ollama.py`에서 모델을 쉽게 바꿀 수 있습니다(예: 더 많은 RAM이 필요하지만 더 복잡한 논리를 위해 `mistral`으로).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### 시스템 프롬프트(페르소나)
`system_instruction`을 조정하여 Aura에 개성을 부여할 수 있습니다.
> "당신은 공상과학 영화에 나오는 비꼬는 조수입니다."

---

## ⚠️ 알려진 제한 사항

1. **지연 시간:** 부팅 후 첫 번째 요청은 모델이 RAM에 로드될 때 1~3초 정도 걸릴 수 있습니다. 후속 요청이 더 빠릅니다.
2. **충돌:** 적절한 폴더 구조 없이 RegEx가 너무 광범위하면(`.*`) 표준 명령을 삼킬 수 있습니다. 알파벳 순서(`z_...`)가 필수적입니다.
3. **하드웨어:** 대략적인 요구 사항 Llama 3.2용 2GB의 여유 RAM.