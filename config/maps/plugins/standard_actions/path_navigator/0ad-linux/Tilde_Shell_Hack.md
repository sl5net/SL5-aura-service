### 2. `Tilde_Shell_Hack.md`
*This file explains the workaround for Aura's restriction on leading special characters, documenting both the `tilde/` substitution and the Zsh integration widget.*

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
# =========================================================================
# Automatic "tilde/" -> "~/" substitution on Enter
# =========================================================================
accept-line-override() {
    BUFFER="${BUFFER//tilde\//~/}"
    zle .accept-line
}
zle -N accept-line accept-line-override
```

### How it works under the hood:
1. When you speak a command (e.g. *"0ad config"*), Aura writes `cd tilde/.config/0ad/config/` into your active terminal.
2. The Zsh line editor (ZLE) intercepts the Enter key press.
3. The custom `accept-line-override` function replaces every instance of `tilde/` with `~/` in the command buffer instantly.
4. Zsh executes the corrected command `cd ~/.config/0ad/config/` natively.


