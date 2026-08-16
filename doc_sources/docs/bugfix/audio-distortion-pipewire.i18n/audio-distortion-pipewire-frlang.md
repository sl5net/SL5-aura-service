# Correction de bug : distorsion audio et blocage de PipeWire (Linux)

Ce document décrit comment résoudre la distorsion audio (« klirren »), les artefacts vocaux robotiques et les blocages audio du système qui peuvent survenir lors de l'utilisation du **SL5-aura-service** avec d'autres applications multimédias telles qu'OBS, AnyDesk ou des flux TTS haute fréquence.

## Symptômes
- Les sons de sortie/entrée vocale sont déformés, métalliques ou "clirring".
- L'audio du système se bloque avec le message : « Établissement de la connexion à PulseAudio » ou « Veuillez patienter ».
- Perte audio totale après une charge CPU élevée ou une utilisation simultanée de flux.
- Les journaux du journal affichent : "spa.alsa : hw:X : erreur snd_pcm_status : aucun périphérique de ce type".

## Cause première
Sur Manjaro et d'autres distributions Linux modernes, **PipeWire** gère l'audio. La distorsion provient généralement de :
1. **Buffer Underruns :** Conflit entre des flux simultanés (par exemple, AnyDesk capturant l'audio pendant l'exécution de TTS/OBS).
2. **Inadéquation de la fréquence d'échantillonnage :** Commutation fréquente entre 44,1 kHz et 48 kHz.
3. **Problèmes de synchronisation USB :** Charge de bus élevée provoquant la déconnexion temporaire des casques USB (comme Plantronics/Poly).

---

##Solutions

### 1. Récupération immédiate (la réinitialisation « nucléaire »)
Si la pile audio est gelée ou déformée, supprimez tous les processus liés à l'audio. Ils redémarreront automatiquement immédiatement.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. Paramètres de prévention et de stabilité

#### Désactiver l'audio AnyDesk
AnyDesk essaie souvent de se connecter au périphérique audio, provoquant des conflits matériels.
- **Action :** Ouvrez les paramètres AnyDesk -> **Audio** -> Désactivez **"Transmettre l'audio"** et **"Reproduire l'audio"**.

#### Correction du taux d'échantillonnage de PipeWire (recommandé)
Forcez PipeWire à rester à 48 kHz pour éviter de rééchantillonner les artefacts pendant la lecture TTS.

1. Créez le répertoire de configuration : `mkdir -p ~/.config/pipewire`
2. Copiez la configuration par défaut : `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. Modifiez `~/.config/pipewire/pipewire.conf` et définissez :
   ```conf
   default.clock.rate = 48000
   ```
4. Redémarrez les services :
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. Récupération post-production (FFmpeg)
Si vous avez enregistré une session et que l'audio est déformé ("clirring"), utilisez la chaîne de filtres `ffmpeg` suivante pour réparer le fichier.

### Commande de réparation recommandée
Cette commande applique un dé-écrêteur, une réduction du bruit et un filtre passe-bas pour supprimer les artefacts numériques haute fréquence sans réencoder la vidéo.

testé et très bon :

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

peut être mieux avec (non testé) :

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



non testé :
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**Répartition des filtres :**
- `adeclip` : Arrondit les pointes d'écrêtage numérique.
- `afftdn` : réduit le bruit numérique basé sur la FFT.
- `lowpass=f=3500` : coupe les fréquences supérieures à 3,5 kHz là où se produisent la plupart des "clirring" (rend la voix plus claire/plus chaude).
- `volume=1.8` : Compense la perte de volume lors du filtrage.
- `-c:v copy` : Conserve la qualité vidéo originale (extrêmement rapide).

---

## Outils de débogage
Pour surveiller la santé audio en temps réel pendant le développement :
- `pw-top` : affiche les erreurs en temps réel (colonne ERR) et l'état du tampon.
- `journalctl --user -u pipewire` : vérifie les déconnexions matérielles.