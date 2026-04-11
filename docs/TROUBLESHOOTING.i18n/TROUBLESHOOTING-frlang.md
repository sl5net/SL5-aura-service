# Dépannage SL5 Aura

## Diagnostic rapide

Commencez toujours ici :

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## Problème : Aura ne démarre pas

**Symptôme :** Aucun son de démarrage, aucun processus visible dans `pgrep`.

**Vérifiez le journal :**
```bash
tail -30 log/aura_engine.log
```

**Causes courantes :**

| Erreur dans le journal | Corriger |
|---|---|
| `ModuleNotFoundError` | Exécutez à nouveau le script d'installation : `bash setup/manjaro_arch_setup.sh` |
| `Aucun module nommé 'objgraph'` | `.venv` a été recréé — réinstallez : `pip install -r Requirements.txt` |
| `Adresse déjà utilisée` | Tuer l'ancien processus : `pkill -9 -f aura_engine` |
| `Modèle introuvable` | Réexécutez l'installation pour télécharger les modèles manquants |
| `pygame.mixer non disponible` | Voir « Aucun son au démarrage » ci-dessous |

---

## Problème : Pas de son au démarrage (pygame.mixer)

**Symptôme :** Avertissement ou erreur concernant `pygame.mixer` non disponible. L'aura commence
mais ne joue aucun son.

**Cause :** La version Pygame de votre système n'inclut pas la prise en charge audio ni SDL2.
les bibliothèques audio manquent.

**Correction sur Arch/Manjaro :**
```bash
sudo pacman -S sdl2_mixer
pip install pygame-ce --upgrade
```

**Correction sur Ubuntu/Debian :**
```bash
sudo apt install libsdl2-mixer-2.0-0
pip install pygame-ce --upgrade
```

Aura continuera à fonctionner sans son — ce n'est pas une erreur fatale.

---

## Problème : Aura plante après la première dictée

**Symptôme :** Fonctionne une fois, puis meurt silencieusement.

**Vérifiez stderr :**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**Si vous voyez `Segmentation Fault` ou `double free` :**

Il s'agit d'un problème connu sur les systèmes avec glibc 2.43+ (CachyOS, Arch plus récent).

```bash
sudo pacman -S mimalloc
```

mimalloc est automatiquement utilisé par le script de démarrage s'il est installé. Confirmez qu'il est actif — vous devriez voir ceci au démarrage :
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## Problème : la touche de déclenchement ne fait rien

**Symptôme :** Vous appuyez sur la touche de raccourci, mais rien ne se passe : pas de son, pas de texte.

**Vérifiez si l'observateur de fichiers est en cours d'exécution :**
```bash
pgrep -a type_watcher
```

Si rien n'apparaît, redémarrez Aura :
```bash
./scripts/restart_venv_and_run-server.sh
```

**Vérifiez si le fichier de déclenchement est en cours de création :**
```bash
ls -la /tmp/sl5_record.trigger
```

Si le fichier n'est jamais créé, votre raccourci clavier ne fonctionne pas – voir ci-dessous.

---

## Problème : le raccourci clavier ne fonctionne pas sur Wayland

**Symptôme :** CopyQ est installé et configuré, mais appuyer sur la touche de raccourci le fait
rien sur une session Wayland.

**Cause :** Les raccourcis clavier globaux CopyQ ne fonctionnent pas de manière fiable sur Wayland sans
configuration supplémentaire. Cela affecte KDE Plasma, GNOME et autres
Compositeurs Wayland.

### Option 1 : Paramètres système KDE (recommandé pour KDE Plasma)

1. Ouvrez **Paramètres système → Raccourcis → Raccourcis personnalisés**
2. Créez un nouveau raccourci de type **Command/URL**
3. Définissez la commande sur :
   ```bash
   touch /tmp/sl5_record.trigger
   ```
4. Attribuez votre combinaison de touches préférée (par exemple « F9 » ou « Ctrl+Alt+Espace »)

### Option 2 : dotool (fonctionne sur n'importe quel compositeur Wayland)

```bash
# Install dotool:
sudo pacman -S dotool        # Arch/Manjaro
# or
sudo apt install dotool      # Ubuntu (if available)
```

Utilisez ensuite le gestionnaire de raccourcis de votre bureau pour exécuter :
```bash
touch /tmp/sl5_record.trigger
```

### Option 3 : ydotool

```bash
sudo pacman -S ydotool
sudo systemctl enable --now ydotool
```

Configurez ensuite votre raccourci pour qu'il s'exécute :
```bash
touch /tmp/sl5_record.trigger
```

### Option 4 : GNOME (en utilisant les paramètres dconf / GNOME)

1. Ouvrez **Paramètres → Clavier → Raccourcis personnalisés**
2. Ajoutez un nouveau raccourci avec la commande :
   ```bash
   touch /tmp/sl5_record.trigger
   ```
3. Attribuez une combinaison de touches

### Option 5 : CopyQ avec le correctif Wayland

Certains compositeurs Wayland permettent à CopyQ de fonctionner s'il est démarré avec :
```bash
QT_QPA_PLATFORM=xcb copyq
```

Cela oblige CopyQ à utiliser XWayland, qui prend en charge les raccourcis clavier globaux.

---

## Problème : le texte apparaît mais sans corrections

**Symptôme :** La dictée fonctionne mais tout reste en minuscules, aucune correction grammaticale.

**Vérifiez si LanguageTool est en cours d'exécution :**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

Si cela renvoie une erreur, LanguageTool n'est pas en cours d'exécution. Aura devrait le démarrer
automatiquement — vérifiez le journal pour les erreurs liées à LanguageTool :

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**Vérifiez le journal LanguageTool :**
```bash
cat log/languagetool_server.log | tail -20
```

---

## Problème : Aura se bloque dans DEV_MODE

**Symptôme :** Avec `DEV_MODE = 1`, Aura se bloque après le premier déclenchement et s'arrête
répondant.

**Cause :** Un volume de journaux élevé provenant de plusieurs threads surcharge le système de journalisation.

**Correction :** Ajoutez un filtre de journal dans `config/filters/settings_local_log_filter.py` :

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

Enregistrez le fichier — Aura recharge automatiquement le filtre. Aucun redémarrage nécessaire.

---

## Problème : plugins.zip grandit sans fin / CPU élevé

**Symptôme :** CPU à 100 %, ventilateurs à pleine vitesse, `plugins.zip` se développe sans s'arrêter.

**Cause :** Le packer sécurisé reconditionne les fichiers dans une boucle infinie.

**Correction :** Assurez-vous que les fichiers `.blob` et `.zip` sont exclus de l'analyse d'horodatage.
Vérifiez `scripts/py/func/secure_packer_lib.py` autour de la ligne 86 :

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

Si cette ligne est manquante, ajoutez-la.

---

## Problème : les règles ne se déclenchent pas

**Symptôme :** Vous dictez une phrase déclencheur mais la règle ne fait rien.

**Liste de contrôle:**

1. La règle est-elle dans le bon fichier ? (`FUZZY_MAP_pre.py` = avant LanguageTool,
`FUZZY_MAP.py` = après)
2. Le fichier cartographique est-il enregistré ? Aura se recharge lors de la sauvegarde - vérifiez le journal pour
« Rechargé avec succès ».
3. Le modèle correspond-il à ce que Vosk transcrit réellement ? Vérifiez le journal pour
la transcription brute :
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. `only_in_windows` est-il défini et la mauvaise fenêtre est active ?
5. Une règle plus générale correspond-elle en premier ? Les règles sont traitées de haut en bas :
faire passer les règles spécifiques avant les règles générales.

---

## Collecte des journaux pour les rapports de bogues

Lorsque vous signalez un problème, veuillez inclure :

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

Publier à : [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)