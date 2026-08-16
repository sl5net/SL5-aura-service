### 2. `Tilde_Shell_Hack.md`
*이 파일은 `물결표/` 대체와 Zsh 통합 위젯을 모두 문서화하여 Aura의 선행 특수 문자 제한에 대한 해결 방법을 설명합니다.*

```markdown
# Aura Special Character Restriction & Tilde Workaround

## The Limitation
Certain voice-recognition setups and macro engines (including early configurations of the Aura service) restrict or reject outputting special characters like `~` (tilde) or `/` at the very beginning of a simulated keystroke string. 

Because paths like `~/.config/0ad/` or `~/.local/share/0ad/` must start with a tilde, a workaround is required to allow hands-free directory navigation.

---

## The Workaround: The `tilde/` Prefix
To bypass this limitation, Aura uses the literal word `tilde/` at the beginning of its fuzzy map replacements:

* Instead of sending `~/.config/0ad/config/`, Aura outputs `tilde/.config/0ad/config/`.
* Instead of sending `~/.local/share/0ad/mods`, Aura outputs `tilde/.local/share/0ad/mods`.

---

## Automatic Terminal Expansion in Zsh

To prevent you from having to manually replace `tilde/` with `~/` every time you trigger a command, you can configure your shell to rewrite the input line automatically when you press the **Enter** key.

Add the following shell widget to the end of your **`~/.zshrc`** configuration file:

```bash
# =====================================================================
# Enter 키를 누르면 자동으로 "물결표/" -> "~/" 대체
# =====================================================================
수락 라인 재정의() {
BUFFER="${BUFFER//물결 기호\//~/}"
zle .accept-line
}
zle -N 수락-라인 수락-라인-재정의
__CODE_BLOCK_1__