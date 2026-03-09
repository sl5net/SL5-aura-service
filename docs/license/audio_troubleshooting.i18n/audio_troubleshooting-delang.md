# Audio-Fehlerbehebung (Linux)

## Problem: Espeak / Fallback ist stumm
Wenn das Fallback-Audio (espeak) nicht hörbar ist, ist es wahrscheinlich im Soundmixer des Systems (z. B. PulseAudio oder PipeWire) stummgeschaltet.

### Der „Long-String-Trick“ zum Aufheben der Stummschaltung
Kurze Audiofragmente verschwinden oft zu schnell aus der Mixer-GUI, als dass sie manuell wieder stummgeschaltet werden könnten. Um dies zu beheben, erzwingen Sie einen langen Audiostream:

__CODE_BLOCK_0__