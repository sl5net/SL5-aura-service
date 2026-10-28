> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# Element ↔ Threema Beta GUI Relay

A small daemon that mirrors messages between **Element Desktop** (Matrix) and
**Threema Beta** (the Threema desktop client) on Linux/X11 by driving both
Windows like a user would: Keyboard shortcuts, the clipboard and a few mouse clicks.

No API, no tokens, no extra Python libraries. Only standard X11 command-line tools.

## What it does

| Direction | What happens |
|---|---|
| **Element → Threema** | The last message *you* wrote in Element is read and, if it is new, pasted into Threema Beta and sent. |
| **Threema → Element** | The last *incoming* message of the open Threema chat is copied via its context menu and, if it is new, pasted into Element and sent. |

Typical use: dictate or type into an Element room (for example with Aura's)
speech-to-text) and have the text arrive in a Threema chat, and see the
Threema replies appear in the same Element room.

Both windows must be open, logged in, and displaying the chat/room you want to relay.

## Loop protection

A naive two-way mirror would bounce every message back and forth forever. The relay
prevents this with a short-lived history (`relay_history.py`):

1. Every text the relay forwards is remembered **before** it is sent, for 180 seconds.
2. If a text shows up on the other side that is in this history, it is our own
   echo: it is marked as seen but **not** forwarded again.
3. A text that is new *and* unknown is a genuine message and is forwarded.

Texts are compared with whitespace collapsed, so line-break differences from
copy/paste do not defeat the guard. Because entries die, you can send the
Same text (for example "ok") again after the window has passed.

On start-up the current last message of each side is read as a **baseline** and is
*not* forwarded. Only messages that arrive after the start are relayed.

## Requirements

- Linux with **X11** (X11 must print X11). Wayland is not supported.
- `xdotool`, `xclip`, `wmctrl`, and `xset` (optional, used to disable the screensaver)
- Element Desktop (WM class `element.Element`)
- Threema Beta (WM class `threema beta.Threema Beta`, e.g. the Flatpak
  `ch.threema.threema-desktop`)
- Python 3 with the project's virtual environment
- `zsh` for the one-time calibration script

## Setup: one-time calibration

Threema Beta draws its own context menu that cannot be operated with the keyboard,
so the relay clicks "Copy Message" with the mouse at positions relative to the
Threema window. Measure them once:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

The script asks for three mouse positions, each with a countdown (do not touch the
Keyboard, do not move or resize the window:

1. **Right-click** the last *incoming* message (a bubble on the left side) and leave
   The menu open.
2. Move the mouse, without clicking, onto **"Copy Message"**.
3. Move the mouse onto the **message input field**.

The result is stored in `~/.config/threema-relay.conf`:

| Key | Meaning |
|---|---|
| `FX` | Horizontal click position as a fraction of the window width |
| `BOTTOM` | Click position, pixels above the window's bottom edge |
| `DX`, `DY` | Offset from the click point to "Copy Message" |
| `INPUT_FX`, `INPUT_BOTTOM` | Position of the message input field |
| `DELAY_MENU`, `DELAY_COPY` | Optional waits in seconds (defaults 0.30 / 0.20) |

Check the calibration with a fresh incoming message as the last one in the chat:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

It prints the copied text without forwarding it. Calibration relies on the window
geometry: if you change the Threema window size a lot, calibrate again.

## Usage

From the repository root:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

Options:

| Option | Effect |
|---|---|
| `--poll SECONDS` | Poll interval (default `2.0`) |
| `--no-threema-to-element` | Relay only Element → Threema |
| `--no-element-enter` | Paste Threema messages into Element's input field but do **not** send them (safe test mode) |

Stop with `Ctrl+C`.

Recommended first run: use `--no-element-enter`, send yourself a message in Threema
and check that it appears in Element's input field. Then run without the option.

Example log:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

## How it works

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- *Up* in Element's composer edits your last own message; *Ctrl+A / Ctrl+C* copies
  it and *Escape* leaves the edit mode. This is why only **your own** last element
  message is relayed to Threema.
- For Threema a **sentinel string** is put into the clipboard first. If it is still
  there afterwards, nothing was copied (for example because your own message is the
  Last one and the click hit no bubble) and the attempt is ignored.

## Files

| File | Purpose |
|---|---|
| `matrix_threema_relay.py` | Main loop, CLI, decision logic (`classify_candidate`) |
| `read_last_element_message.py` | Read Element's last own message |
| `send_to_threema_window.py` | Pastes text into Threema Beta |
| `read_last_threema_message.py` | Reads Threema's last incoming message, loads calibration |
| `send_to_element_window.py` | Pastes text into Element |
| `relay_history.py` | Loop protection |
| `threema-relay.zsh` | Calibration and manual test tool (`calibrate`, `test`) |
| `test_threema_relay.py` | Unit tests (no X11 required) |

Run the tests with:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

## Limitations

- **The relay uses your mouse and keyboard focus. *** During each poll the Threema and
  Element Windows are focused and the mouse jumps briefly (it is restored). Do not
  type while a poll runs, or use a longer `--poll`.
- Overwrites the clipboard on every poll.
- **Own message last in Threema:** when your own message is the last in the Threema
  Chat, a reply that arrived just before it is not seen.
- **Only the last message** is read per poll. If several messages arrive within one
  interval, only the newest is relayed.
- **Text only.** Images, files, reactions and edits are not relayed.
- **One chat pair.** Whatever chat/room is open in each window is used.
- **A draft in Element's input field** will be combined with the next pasted
  message.
- **X11 only.** Wayland blocks synthetic input and window focus changes.
- The relay disables the X11 screensaver and DPMS on start (`xset s off -dpms`);
  They stay off until you re-enable them or log in again.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `Threema window ... not found` | Check `xdotool search --class "Threema Beta"` and `xprop WM_CLASS` (click the window). |
| `Nothing copied` / no Threema → Element | Re-run `calibrate`; run `test` with an incoming message as the last one. Increase `DELAY_MENU`/`DELAY_COPY` in the config on a slow machine. |
| Text arrives in Threema but is not sent | Input field not focused; check `INPUT_FX`/`INPUT_BOTTOM` from calibration. |
| Threema text appears in Element but is not sent | The relay was started with `--no-element-enter`. |
| Decimal numbers like `0,9353` in the config | Written by an older script version under a German locale. The Python code accepts them; Calibrating again with the current script writes dots. |
