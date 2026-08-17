### 마크다운 문서(`docs/AHK_SCRIPTS.md`)

# SL5-Aura-Service를 위한 AutoHotkey 인프라

Windows는 파일 잠금 및 시스템 단축키를 Linux와 다르게 처리하기 때문에 이 프로젝트에서는 AutoHotkey(v2) 스크립트 세트를 사용하여 Python STT 엔진과 Windows 사용자 인터페이스 간의 격차를 해소합니다.

## 스크립트 개요

### 1. `trigger-hotkeys.ahk`
* **목적:** 서비스 제어를 위한 기본 사용자 인터페이스입니다.
* **주요 기능:**
* 받아쓰기를 시작/중지하려면 **F10** 및 **F11**을 가로채세요.
* '키보드 후크'를 사용하여 기본 Windows 시스템 동작(예: 메뉴 표시줄을 활성화하는 F10)을 재정의합니다.
* **배포:** "최고 권한"으로 Windows 작업 스케줄러를 통해 등록되도록 설계되었으므로 사용자가 관리자 수준 응용 프로그램에서 작업하는 경우에도 단축키를 캡처할 수 있습니다.

### 2. `type_watcher.ahk`
* **목적:** STT 파이프라인에서 "소비자" 역할을 합니다.
* **주요 기능:**
* Python 엔진에서 생성된 수신 `.txt` 파일에 대한 임시 디렉터리를 감시합니다.
* **상태 머신(좀비 맵):** 각 파일이 정확히 한 번 입력되었는지 확인하기 위해 메모리 기반 맵을 구현합니다. 이는 중복된 Windows 파일 시스템 이벤트(추가/수정)로 인해 발생하는 "이중 입력"을 방지합니다.
* **안전한 입력:** `SendText`를 사용하여 모든 활성 편집기에서 특수 문자가 올바르게 처리되도록 합니다.
* **신뢰할 수 있는 정리:** Windows 파일 액세스 잠금을 처리하기 위해 재시도 논리로 파일 삭제를 관리합니다.

### 3. `scripts/ahk/sync_editor.ahk`
* **목적:** 디스크와 텍스트 편집기(예: Notepad++) 간의 원활한 동기화를 보장합니다.
* **주요 기능:**
* **요청 시 저장:** 엔진이 파일을 읽기 전에 편집기에서 `Ctrl+S`를 강제로 실행하기 위해 Python에 의해 트리거될 수 있습니다.
* **Dialog Automator:** "다른 프로그램에 의해 수정된 파일" 다시 로드 대화 상자를 자동으로 감지하고 확인하여 유연한 실시간 업데이트 환경을 만듭니다.
* **시각적 피드백:** 수정 사항이 적용되고 있음을 사용자에게 알리는 단기 알림 상자를 제공합니다.

### 4. `scripts/notification_watcher.ahk`
* **목적:** 백그라운드 프로세스에 대한 UI 피드백을 제공합니다.
* **주요 기능:**
* 특정 상태 파일이나 이벤트를 모니터링하여 사용자에게 알림을 표시합니다.
* 메시지를 "계산"하는 논리(Python)를 "표시"(AHK)에서 분리하여 기본 STT 엔진이 UI 상호 작용으로 차단되지 않도록 합니다.


---

### 비관리자 대체
관리자 권한 없이 애플리케이션을 실행하는 경우:
- **기능:** 서비스는 완전한 기능을 유지합니다.
- **핫키 제한 사항:** **F10**과 같은 시스템 예약 키는 여전히 Windows 메뉴를 트리거할 수 있습니다. 이 경우 단축키를 시스템 키가 아닌 키(예: `F9` 또는 `Insert`)로 변경하는 것이 좋습니다.
- **작업 스케줄러:** 관리자 설치 중에 "AuraDictation_Hotkeys" 작업이 생성된 경우 표준 사용자라도 높은 권한으로 스크립트가 실행됩니다. 그렇지 않은 경우 `start_dictation.bat`는 로컬 사용자 수준 인스턴스를 자동으로 시작합니다.

---

### 3. Warum "nervige Meldungen" erscheinen und wie man sie im AHK-Code stoppt
Um sicherzustellen, dass das Skript selbst niemals den Nutzer mit Popups stört, füge diese "Silent-Flags" oben in deine `.ahk` Dateien ein:

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. 단축키 전략(F10 대안)
Da F10 ohne Admin-Rechte unter Windows fast unmöglich sauber abzufangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Zusammenfassung der Verbesserungen:
1. **배치 날짜:** Nutzt `start "" /b`, um das schwarze Fenster zu vermeiden, und prüft vorher, ob der Admin-Task schon läuft.
2. **Transparenz:** Die Doku erklärt nun offen: "Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10".
3. **AHK 스크립트:** Nutzt `#SingleInstance Force`, um den "이전 인스턴스가 실행 중입니다."-Dialog zu unterdrücken.

Damit wirkt die Software viel professioneller("Smooth"), da sie im Hintergrund startet, ohne dass der Nutzer mit technischen 세부 정보 oder Bestätigungsfenstern konfrontiert wird.
XSPACEbreakX
XSPACEbreakX
---

### 이 문서가 중요한 이유:
**"좀비 맵"** 및 **"작업 스케줄러/관리자"** 요구 사항을 문서화함으로써 코드가 단순한 Linux 스크립트보다 더 복잡한 이유를 다른 개발자(및 미래의 자신)에게 설명할 수 있습니다. "이상한 해결 방법"을 "Windows 제한 사항에 대한 엔지니어링 솔루션"으로 바꿉니다.

(s,29.1.'26 11:02 목)