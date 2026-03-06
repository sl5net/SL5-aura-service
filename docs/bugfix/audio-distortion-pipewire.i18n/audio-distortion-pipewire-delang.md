# Bugfix: Audioverzerrung und PipeWire-Hang (Linux)

In diesem Dokument wird beschrieben, wie Sie Audioverzerrungen („Kirren“), Roboter-Sprachartefakte und System-Audio-Hänger beheben können, die auftreten können, wenn **SL5-aura-service** zusammen mit anderen Medienanwendungen wie OBS, AnyDesk oder Hochfrequenz-TTS-Streams verwendet wird.

## Symptome
- Sprachausgabe/-eingabe klingt verzerrt, metallisch oder „klirrend“.
- System-Audio hängt mit der Meldung: „Verbindung zu PulseAudio wird hergestellt“ oder „Bitte warten“.
– Totaler Audioverlust nach hoher CPU-Last oder gleichzeitiger Stream-Nutzung.
- Journalprotokolle zeigen: „spa.alsa: hw:X: snd_pcm_status error: No such device“.

## Grundursache
Auf Manjaro und anderen modernen Linux-Distributionen verwaltet **PipeWire** Audio. Verzerrungen entstehen normalerweise durch:
1. **Pufferunterläufe:** Konflikt zwischen gleichzeitigen Streams (z. B. AnyDesk erfasst Audio, während TTS/OBS ausgeführt wird).
2. **Abweichung der Abtastrate:** Häufiges Umschalten zwischen 44,1 kHz und 48 kHz.
3. **USB-Timing-Probleme:** Hohe Buslast führt dazu, dass USB-Headsets (wie Plantronics/Poly) vorübergehend getrennt werden.

---

## Lösungen

### 1. Sofortige Wiederherstellung (der „nukleare“ Reset)
Wenn der Audiostapel eingefroren oder verzerrt ist, beenden Sie alle audiobezogenen Prozesse. Sie werden sofort automatisch neu gestartet.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. Präventions- und Stabilitätseinstellungen

#### Deaktivieren Sie AnyDesk Audio
AnyDesk versucht häufig, sich mit dem Audiogerät zu verbinden, was zu Hardwarekonflikten führt.
- **Aktion:** Öffnen Sie die AnyDesk-Einstellungen -> **Audio** -> Deaktivieren Sie **"Audio übertragen"** und **"Audio reproduzieren"**.

#### PipeWire-Abtastrate korrigieren (empfohlen)
Erzwingen Sie, dass PipeWire bei 48 kHz bleibt, um Resampling-Artefakte während der TTS-Wiedergabe zu vermeiden.

1. Erstellen Sie das Konfigurationsverzeichnis: „mkdir -p ~/.config/pipewire“.
2. Kopieren Sie die Standardkonfiguration: „cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/“.
3. Bearbeiten Sie „~/.config/pipewire/pipewire.conf“ und legen Sie Folgendes fest:
   ```conf
   default.clock.rate = 48000
   ```
4. Dienste neu starten:
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. Wiederherstellung nach der Produktion (FFmpeg)
Wenn Sie eine Sitzung aufgezeichnet haben und der Ton verzerrt ist („klirrt“), verwenden Sie die folgende „ffmpeg“-Filterkette, um die Datei zu reparieren.

### Empfohlener Reparaturbefehl
Dieser Befehl wendet einen Declipper, eine Rauschunterdrückung und einen Tiefpassfilter an, um hochfrequente digitale Artefakte zu entfernen, ohne das Video neu zu kodieren.

getestet und sehr gut:

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

vielleicht besser mit (nicht getestet):

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



nicht getestet:
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**Filteraufschlüsselung:**
- „adeclip“: Rundet digitale Clipping-Spitzen ab.
- „afftdn“: Reduziert FFT-basiertes digitales Rauschen.
- „lowpass=f=3500“: Schneidet Frequenzen über 3,5 kHz ab, bei denen das meiste „Klimpern“ auftritt (macht die Stimme klarer/wärmer).
- „volume=1.8“: Kompensiert den Volumenverlust während der Filterung.
- „-c:v copy“: Behält die ursprüngliche Videoqualität bei (extrem schnell).

---

## Debugging-Tools
So überwachen Sie den Audiozustand während der Entwicklung in Echtzeit:
- „pw-top“: Zeigt Echtzeitfehler (ERR-Spalte) und Pufferstatus an.
- „journalctl --user -u pipewire“: Überprüft, ob Hardware-Verbindungsabbrüche vorliegen.