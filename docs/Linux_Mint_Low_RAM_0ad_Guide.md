# Running 0 A.D. with Aura Voice Control on Low-RAM Systems (Linux Mint)

This guide documents the setup and memory optimization for running **sl5net Aura** voice control alongside **0 A.D.** on legacy or memory-constrained Linux Mint hardware.

## Target Hardware & System Profile
- **Device**: Lenovo ThinkPad T520 (Laptop)
- **CPU**: Intel Core i7-2620M (Dual-Core @ 2.70GHz - 3.40GHz)
- **Memory**: 5.67 GiB RAM
- **Swap**: 4 GiB effective swap
- **Operating System**: Linux Mint 21.3 Virginia (64-bit)
- **Desktop Environment**: Cinnamon 6.0.5 (X11 Display Server)
- **Application Target**: 0 A.D. (Empires Ascendant)

## Memory Management & Architecture
On systems with ≤ 6 GiB RAM, running a heavy desktop environment, a 3D RTS game (0 A.D.), and speech recognition simultaneously requires strict memory protection:

1. **Vosk Speech Model Priority**:
   - Uses `vosk-model-small-de` (or language equivalent) for low memory footprint (~300-500 MB).
   - Vosk model retention is prioritized to ensure real-time command responsiveness during gameplay.

2. **Automatic LanguageTool Eviction**:
   - LanguageTool's Java process can consume ~1.34 GiB RSS.
   - When available RAM drops below `CRITICAL_THRESHOLD_MB` (2.0 GiB), Aura's `model_manager` immediately terminates LanguageTool to free ~1.3 GiB RAM for the game.
   - A 5-minute cooldown (`set_language_tool_cooldown`) prevents LanguageTool from restarting and thrashing memory during active gameplay.

## Verification Commands
To inspect system memory and process states:
```bash
# Check memory and swap usage
free -h

# Check if LanguageTool process is evicted
ps aux | grep -i "[l]anguagetool"
