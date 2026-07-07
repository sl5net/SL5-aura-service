### 2. `Tilde_Shell_Hack.md`
*Diese Datei erläutert die Problemumgehung für Auras Beschränkung auf führende Sonderzeichen und dokumentiert sowohl die „Tilde/“-Ersetzung als auch das Zsh-Integrations-Widget.*

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
# ======================================================================
# Automatische „tilde/“ -> „~/“-Ersetzung bei Enter
# ======================================================================
Accept-line-override() {
BUFFER="${BUFFER//tilde\//~/}"
zle .accept-line
}
zle -N Accept-Line Accept-Line-Override
__CODE_BLOCK_1__