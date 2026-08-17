# 🧠 SL5 Aura 하이브리드 모드: 로컬 LLM 및 클립보드 통합

**상태:** 안정적
**기술:** Ollama(Llama 3.2) + 파일 브리지 아키텍처
**개인정보 보호:** 100% 오프라인

## 컨셉: "건축가 & 인턴"

전통적으로 Aura는 빠르고 정확한 결정론적 규칙(RegEx)을 사용합니다. **"건축가"**입니다.
**로컬 LLM 플러그인**은 **"인턴"** 역할을 합니다. 퍼지 요청을 처리하고 텍스트를 요약하며 일반적인 질문에 답변합니다.

## 🛠 아키텍처: 클립보드 브리지

Linux(Wayland/X11)의 보안 제한으로 인해 백그라운드 프로세스(예: Aura)가 클립보드에 직접 액세스할 수 없는 경우가 많습니다. 우리는 **브리지 아키텍처**를 사용하여 이 문제를 해결했습니다.

1. **제공자(사용자 세션):** 작은 쉘 스크립트(`clipboard_bridge.sh`)가 사용자 세션에서 실행됩니다. 클립보드를 관찰하고 그 내용을 임시 파일(`/tmp/aura_clipboard.txt`)에 미러링합니다.
2. **소비자(Aura):** Python 플러그인이 이 파일을 읽습니다. 파일 액세스는 보편적이므로 권한 문제는 우회됩니다.

---

## 🚀 설정 가이드

### 1. 올라마 설치하기
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. 브리지 스크립트 설정
`~/clipboard_bridge.sh`를 생성하고 실행 가능하게 만듭니다.

```bash
#!/bin/bash
# Mirrors clipboard to a file in RAM
FILE="/tmp/aura_clipboard.txt"
while true; do
    if command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    else
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    fi
    sleep 1.5
done
```

**중요:** 이 스크립트를 시스템 자동 시작에 추가하세요!

### 3. 플러그인 로직(`ask_ollama.py`)

스크립트는 `config/maps/plugins/z_fallback_llm/de-DE/`에 있습니다.
* **트리거:** "컴퓨터", "Aura", "클립보드", "요약"과 같은 단어를 감지합니다.
* **메모리:** 컨텍스트를 기억하기 위해 `conversation_history.json`을 유지합니다(예: "내가 방금 무엇을 물었나요?").
* **신속한 엔지니어링:** 환각을 방지하기 위해 과거 대화 내용보다 현재 클립보드 데이터에 우선순위를 둡니다.

---

## 📝 사용 예

1. **텍스트 요약:**
* *조치:* 긴 이메일이나 웹사이트 텍스트를 복사하세요(Ctrl+C).
* *음성 명령:* "컴퓨터, 클립보드에 있는 텍스트를 요약해 주세요."

2. **번역/분석:**
* *조치:* 코드 조각을 복사하세요.
* *음성 명령:* "컴퓨터야, 클립보드에 있는 코드가 무슨 일을 하는 거야?"

3. **일반 채팅:**
* *음성 명령:* "컴퓨터야, 프로그래머에 관한 농담을 들려줘."

4. **메모리 재설정:**
* *음성 명령:* "컴퓨터야, 모든 걸 잊어버려." (JSON 기록을 지웁니다).
XSPACEbreakX