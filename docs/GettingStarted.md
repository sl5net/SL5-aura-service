# Getting Started with SL5 Aura

> **Prerequisites:** You have completed the setup script and configured your hotkey.
> If not, see the [Installation section in README.md](../README.md#installation).

---

## Step 0: Configure Your Hotkey

Choose your platform:

**Linux/macOS** — Install [CopyQ](https://github.com/hluk/CopyQ) and create a command with a global shortcut:
```bash
touch /tmp/sl5_record.trigger
```

**Windows** — Use [AutoHotkey v2](https://www.autohotkey.com/) or CopyQ. The setup script installs both automatically.
The trigger file is: `c:\tmp\sl5_record.trigger`

> Full details: [README.md#configure-your-hotkey](../README.md#configure-your-hotkey)

## Step 1: Your First Dictation

1. Start Aura (if not already running):
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
   Wait for the startup sound — that means Aura is ready.

2. Click into any text field (editor, browser, terminal).
3. Press your hotkey, say **"Hello World"**, press the hotkey again.
4. Watch the text appear.

> **Nothing happened?** Check `log/aura_engine.log` for errors.
> Common fix for CachyOS/Arch: `sudo pacman -S mimalloc`

---

## Step 2: Write Your First Rule

The fastest way to add a personal rule:

1. Open `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Add a rule inside `FUZZY_MAP_pre = [...]`:
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **Save** — Aura reloads automatically. No restart needed.
4. Dictate `hello world` and watch it become `Hello World`.

> See `docs/FuzzyMapRuleGuide.md` for the full rule reference.

### The Oma-Modus (Beginner Shortcut)

Don't know regex yet? No problem.

1. Open any empty `FUZZY_MAP_pre.py` in the sandbox
2. Write just a plain word on its own line (no quotes, no tuple):
   ```
   raspberry
   ```
3. Save — the Auto-Fix system detects the bare word and automatically
   converts it into a valid rule entry.
4. You can then edit the replacement text manually.

This is called **Oma-Modus** — designed for users who want results without
learning regex first .

---

## Step 3: Learn with Koans

Koans are small exercises that each teach one concept.
They live in `config/maps/koans_deutsch/` and `config/maps/koans_english/`.

Start here:

| Folder | What you learn |
|---|---|
| `00_koan_oma-modus` | Auto-Fix, first rule without regex |
| `01_koan_erste_schritte` | Your first rule, pipeline basics |
| `02_koan_listen` | Working with lists |
| `03_koan_schwierige_namen` | Fuzzy matching for hard-to-recognize names |
| `04_koan_kleine_helfer` | Useful shortcuts |

Each koan folder contains a `FUZZY_MAP_pre.py` with commented examples.
Uncomment a rule, save, dictate the trigger phrase — done.

---

## Step 4: Go Further

| What | Where |
|---|---|
| Full rule reference | `docs/FuzzyMapRuleGuide.md` |
| Create your own plugin | `docs/CreatingNewPluginModules.md` |
| Run Python scripts from rules | `docs/advanced-scripting.md` |
| DEV_MODE + log filter setup | `docs/Developer_Guide/dev_mode_setup.md` |
| Context-aware rules (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |

