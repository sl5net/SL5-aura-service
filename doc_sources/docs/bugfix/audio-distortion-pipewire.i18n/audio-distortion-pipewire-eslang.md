# Corrección de errores: distorsión de audio y bloqueo de PipeWire (Linux)

Este documento describe cómo resolver la distorsión de audio ("klirren"), artefactos de voz robótica y bloqueos de audio del sistema que pueden ocurrir al usar **SL5-aura-service** junto con otras aplicaciones multimedia como OBS, AnyDesk o transmisiones TTS de alta frecuencia.

## Síntomas
- La salida/entrada de voz suena distorsionada, metálica o "chirriante".
- El audio del sistema se bloquea con el mensaje: "Estableciendo conexión con PulseAudio" o "Espere".
- Pérdida total de audio después de una carga alta de CPU o uso simultáneo de transmisión.
- Los registros del diario muestran: `spa.alsa: hw:X: snd_pcm_status error: No existe tal dispositivo`.

## Causa principal
En Manjaro y otras distribuciones modernas de Linux, **PipeWire** gestiona el audio. La distorsión suele deberse a:
1. **Insuficiencia del búfer:** Conflicto entre transmisiones simultáneas (p. ej., AnyDesk captura audio mientras se ejecuta TTS/OBS).
2. **Frecuencia de muestreo no coincidente:** Cambio frecuente entre 44,1 kHz y 48 kHz.
3. **Problemas de sincronización USB:** La alta carga del bus hace que los auriculares USB (como Plantronics/Poly) se desconecten temporalmente.

---

## Soluciones

### 1. Recuperación Inmediata (El Reinicio "Nuclear")
Si la pila de audio está congelada o distorsionada, elimine todos los procesos relacionados con el audio. Se reiniciarán automáticamente inmediatamente.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. Configuración de prevención y estabilidad

#### Deshabilitar el audio de AnyDesk
AnyDesk a menudo intenta conectarse al dispositivo de audio, lo que provoca conflictos de hardware.
- **Acción:** Abra la configuración de AnyDesk -> **Audio** -> Deshabilite **"Transmitir audio"** y **"Reproducir audio"**.

#### Arreglar la frecuencia de muestreo de PipeWire (recomendado)
Fuerce a PipeWire a permanecer en 48 kHz para evitar artefactos de remuestreo durante la reproducción TTS.

1. Cree el directorio de configuración: `mkdir -p ~/.config/pipewire`
2. Copie la configuración predeterminada: `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. Edite `~/.config/pipewire/pipewire.conf` y configure:
   ```conf
   default.clock.rate = 48000
   ```
4. Reiniciar los servicios:
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. Recuperación de posproducción (FFmpeg)
Si grabó una sesión y el audio está distorsionado ("clirring"), use la siguiente cadena de filtros `ffmpeg` para reparar el archivo.

### Comando de reparación recomendado
Este comando aplica un eliminador de recortes, reducción de ruido y un filtro de paso bajo para eliminar artefactos digitales de alta frecuencia sin volver a codificar el vídeo.

probado y muy bueno:

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

puede ser mejor con (no probado):

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



no probado:
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**Desglose del filtro:**
- `adeclip`: Redondea los picos de recorte digital.
- `afftdn`: Reduce el ruido digital basado en FFT.
- `lowpass=f=3500`: Corta las frecuencias superiores a 3,5 kHz donde se produce la mayor parte del "clic" (hace que la voz sea más clara/cálida).
- `volume=1.8`: Compensa la pérdida de volumen durante el filtrado.
- `-c:v copy`: Mantiene la calidad del vídeo original (extremadamente rápido).

---

## Herramientas de depuración
Para monitorear el estado del audio en tiempo real durante el desarrollo:
- `pw-top`: Muestra errores en tiempo real (columna ERR) y el estado del buffer.
- `journalctl --user -u pipewire`: comprueba si hay desconexiones de hardware.