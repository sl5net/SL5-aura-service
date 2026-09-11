# Recording Overlay (On-Screen Display)

The Recording Overlay provides an immediate, cross-platform visual indicator of dictation status. It operates independently of desktop notification daemons and "Do Not Disturb" filters, displaying the state directly on the primary screen.

## Visual Examples

| Bottom-Left (`bl`) | Top-Right (`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](images/recording_overlay_1.png) | ![Top-Right Overlay 2](images/recording_2.png) |
| *Blends into dark panels and system trays* | *High contrast over light or complex windows* |

## States

- **Recording (`🔴`)**: A vivid red circle with a highlighted outline (`#e62222` on `#181818`) signals active audio recording.
- **Idle**:
  - `hidden` (default): The window is completely withdrawn, freeing desktop space for normal interaction.
  - `pentagon`: Displays a subtle geometric pentagon badge (`⬟`) during idle mode.

## Configuration

Settings are managed in `config/settings.py`:

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

## Architecture

- Built using the Python standard library (`tkinter`), requiring zero external C-dependencies.
- Executes in a background daemon thread with thread-safe queue event handling.
- Dynamically detects the primary monitor in multi-display environments.

(s, 10.9.'26 14:41 Thu)
