# Abschlussbericht: SL5 Aura – Déclencher un test de bout en bout

**Donnée :** 2026-03-15  
**Date :** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Le plan

Un véritable test de bout en bout du problème potentiel est le suivant :
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

La solution de test :
1. Une date WAV et une expérience de microphone virtuelle
2. Aura pour démarrer `touch /tmp/sl5_record.trigger` — comme dans une véritable description
3. Avec deux éléments d'arrêt de la gâchette
4. La sortie avec la transcription YouTube est disponible
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Était-ce une erreur ✅

- Aura réagit au déclencheur corrigé
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` trouve la date `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` prend en charge la correction du texte de référence
- Le grundlegende Testaufbau est solide et fonctionnel.

---

## 3. Le problème ungelöste 🔴

### Kern-Problem : `manage_audio_routing` est expliqué partout

Beim Session-Start ruft Aura stagiaire auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Cette fonction fonctionne comme la première :
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Ensuite, vous aurez un nouveau Sink avec `mode == 'SYSTEM_DEFAULT'` (pas `MIC_AND_DESKTOP`).

### Recherche de détails

| Versuch | Problème |
|---|---|
| Création de la source virtuelle PulseAudio | PipeWire ignore `module-virtual-source` |
| `settings_local.py` auf `MIC_AND_DESKTOP` défini | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Marquer le bloc de remplacement et afficher la fin | Aura ne permet pas de régler correctement les paramètres avant le déclenchement |
| `_create_mic_and_desktop_sink()` directement dans le test | Wird von `manage_audio_routing` lors du démarrage de session |
| `pw-bouclage` | Erscheint als Source aber Aura hört nicht darauf |

### Le paramètre `settings_local.py` Override n'est pas fonctionnel

`dynamic_settings.py` surveille la date et se trouve à chaque instant — pendant un intervalle. Der Trigger kommt zu schnell nach dem Schreiben. Aura démarre la session maintenant avec d'autres valeurs `SYSTEM_DEFAULT`.

Au lieu de cela : lorsque Aura `MIC_AND_DESKTOP` apparaît, le Sink est d'abord au **nächsten** Session-Start — pas si fort.

---

## 4. Mögliche Lösungswege

### Option A — Durées de conservation jusqu'à la configuration des paramètres
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risque : Nicht zuverlässig, timing-abhängig.

### Option B — L'aura ne démarre plus après la configuration des paramètres
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
Nachteil: Testez pendant 1 minute. Aber zuverlässig.

### Option C — `manage_audio_routing` directement dans le test effectué
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
Alors le Sink existe avant le déclencheur — et `manage_audio_routing` au démarrage de session fonctionne `is_mic_and_desktop_sink_active() == True` et est activé lors de la configuration.

Das ist wahrscheinlich die **sauberste Lösung**.

### Option D — `process_text_in_background` directement affiché (un déclencheur)
Comme dans `test_youtube_audio_regression.py` — Vosk-Output directement dans le pipeline, sans le véritable mécanisme de déclenchement. Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes.

### Option E — Aura avec `run_mode_override=TEST` démarrée
Falls Aura est un mode de test qui a été utilisé pour le routage audio.

---

## 5. Utilisation

**Option C** à tester — un test d'importation effectué :

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

Lorsque la fonction est effectuée :
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Ensuite, Aura est créé au démarrage de session `is_mic_and_desktop_sink_active() == True` et le dernier Sink est activé.

---

## 6. Ce test a-t-il été longfristig apporté

Sobald er läuft, kann man:
- `SPEECH_PAUSE_TIMEOUT` a été testé (1.0, 2.0, 4.0s) et apparaît à la lecture du mot abgeschnitten wird
- Optimisation des paramètres `transcribe_audio_with_feedback.py`
- La régression est possible lorsque la gestion audio est effectuée
- Beweisen dass ein Fix wirklich hilft

---

---

# Rapport final : SL5 Aura – Déclencher un test de bout en bout

**Date :** 2026-03-15  
**Fichier :** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Le plan

Un véritable test de bout en bout pour investiguer le problème connu :
**Dans certains enregistrements, le dernier mot est coupé dans la sortie.**

Le test doit :
1. Alimentez un fichier WAV comme microphone virtuel
2. Démarrez Aura via `touch /tmp/sl5_record.trigger` — exactement comme une utilisation réelle
3. Arrêtez avec un deuxième déclencheur
4. Comparez la sortie avec la transcription YouTube
5. Détecter s'il manque un mot à la fin

---

## 2. Ce qui a été réalisé ✅

- Aura répond correctement au déclencheur
- LT est en cours d'exécution et accessible (`http://127.0.0.1:8082`)
- `_wait_for_output()` trouve le fichier `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` récupère correctement le texte de référence
- La structure de test de base est solide et fonctionne conceptuellement

---

## 3. Le problème non résolu 🔴

### Problème principal : `manage_audio_routing` écrase tout

Au début de la session, Aura appelle en interne :
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Cette fonction fait d'abord :
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Il supprime tout récepteur que nous avons créé au préalable.**

Ensuite, il ne crée aucun nouveau récepteur car `mode == 'SYSTEM_DEFAULT'` (pas `MIC_AND_DESKTOP`).

### Tentatives de solutions

| Tentative | Problème |
|---|---|
| Créer une source virtuelle PulseAudio | PipeWire ignore `module-virtual-source` |
| Définissez `settings_local.py` sur `MIC_AND_DESKTOP` | Le fichier a été corrompu avec plusieurs entrées |
| Écrire le bloc de remplacement marqué à la fin du fichier | Aura ne recharge pas les paramètres assez rapidement avant le déclenchement du déclencheur |
| `_create_mic_and_desktop_sink()` directement dans test | Supprimé par `manage_audio_routing` au début de la session |
| `pw-bouclage` | Apparaît comme source mais Aura ne l'écoute pas |

---

## 4. Prochaine étape recommandée

Appelez `manage_audio_routing` directement depuis le test avant le déclenchement :

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Lorsqu'Aura démarre la session, il vérifie `is_mic_and_desktop_sink_active()` — si `True`, il ignore la configuration et laisse le récepteur tranquille. C'est la solution la plus propre.

---

## 5. Ce que ce test permettra à long terme

Une fois exécuté :
- Testez les valeurs `SPEECH_PAUSE_TIMEOUT` (1.0, 2.0, 4.0s) et détectez la coupure des mots
- Optimiser les paramètres `transcribe_audio_with_feedback.py`
- Détecter les régressions lorsque la gestion audio change
- Prouver qu'un correctif fonctionne réellement