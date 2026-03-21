# SL5 Aura – Tests de régression audio : rapport d'état

**Donnée :** 2026-03-14  
**Date :** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. C'était la vérité

Un système de test de :
1. Un segment audio sur une vidéo YouTube diffusé (via `yt-dlp` + `ffmpeg`)
2. La transcription automatique de YouTube pour chaque segment est générée automatiquement (via `youtube-transcript-api`)
3. Das Audio par Vosk transcrit
4. Facultatif, les éléments créés par le **tout Aura-Pipeline** sont coupés (`process_text_in_background`)
5. Le taux d'erreur de mots (WER) correspond à la sortie Aura et à la transcription YouTube.
6. Pour `pytest` comme test de régression automatique

Tous les téléchargements sont effectués (`scripts/py/func/checks/fixtures/youtube_clips/`), de bons tests de suivi sont également effectués.

---

## 2. Dateien

| Datei | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Dernière date de test |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gécacher des clips audio |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcriptions de Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Cache aus Git ausschließen |
| `conftest.py` (Repo-Racine) | Définir PYTHONPATH pour pytest |

---

## 3. Test-Modi

### Modus A – Vosk uniquement (référence)
```python
YoutubeAudioTestCase(
    test_id       = "mein_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Testez votre qualité professionnelle. Kein Aura. Schnell.

### Modus B – Volle Aura-Pipeline, WER-Vergleich
```python
YoutubeAudioTestCase(
    test_id            = "mein_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # strenger — Aura soll besser sein als Vosk
    test_aura_pipeline = True,
)
```
Schickt Vosk-Output par FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Mode C – Volle Aura-Pipeline, sortie plus précise
```python
YoutubeAudioTestCase(
    test_id            = "befehl_terminal_oeffnen",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",  # Aura muss genau das ausgeben
)
```
Für Segmente wo ein bekannter Befehl gesprochen wird. Test de Schärfster.

---

## 4. C'était wird getestet — ce n'était pas

| Était | Testé ? |
|---|---|
| Vosk STT-Qualité | ✅ |
| Pré-réglage FuzzyMap | ✅ (lorsqu'Aura se déclenche) |
| LanguageTool-Corrections | ✅ (lorsque LT est lancé) |
| FuzzyMap post-régulation | ✅ (lorsqu'Aura se déclenche) |
| Sortie clavier (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, keine Logik |
| Chargement du modèle Vosk | ❌ — Aura est la date de sortie la plus proche du nouveau modèle |

La sortie sera au `tts_output_*.txt` dans Temp-Verzeichnis gelesen — donc comme Aura est interne macht, pas au terminal.

---

## 5. Démarrage

### Normaler Testlauf (Aura muss bereits laufen) :
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Avec tout le journal :
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Nos meilleurs tests :
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT pour démarrer :
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

---

## 6. Quelle configuration

### Sprachcodes — deux systèmes différents !

| Système | Codes | Aperçu |
|---|---|---|
| Vosk-Modèle-Ordner | `de` | `models/vosk-model-de-0.21` |
| Commande Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| API de transcription YouTube | `de` | `api.fetch(..., langues=["de"])` |

**Lösung im Code:** `langue="de-DE"` défini. Le code est automatique :
- Pour Vosk : `"de-DE"` → `"de"` (split auf `-`)
- Pour YouTube : `"de-DE"` → `"de"` (split en `-`)
- Pour Aura : `"de-DE"` direkt

### Le traducteur automatique est désactivé pour les tests :
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sonst übersetzt Aura deutschen Text ins Englische — das verfälscht den WER.

---

## 7. Problèmes et problèmes rencontrés

| Problème | Ursache | Lecture |
|---|---|---|
| `SAUTÉ` | La transcription YouTube n'est pas financée | `api.list('video_id')` affiche une liste de lecture à voir |
| `SKIPPED` après audio | Le modèle Vosk n'est pas financé | `langue.split("-")[0]` Repli dans le code |
| `Trouvé 0 règles FUZZY_MAP_pre` | Falscher Sprachcode et Aura | `"de-DE"` au lieu de `"de"` utilisé |
| `Connexion refusée 8010` | LT n'est pas gestartet | Aura zuerst starten, guerre des années 60 |
| `zsh : terminé` | X11-Watchdog killt Prozess | `SDL_VIDEODRIVER=dummy` utilisé ; Watchdog-Schwellenwert erhöhen |
| YouTube `>>` Marqueur | Zweitsprecher dans la transcription | `re.sub(r'>>', '', text)` — nur `>>` entfernen, Wörter behalten |
| `AttributeError : get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` à la méthode classique |
| Cache enthält leeren Texte | Modifier la position avec les expressions Regex | `rm luminaires/youtube_clips/*.transcript.json` |

---

## 8. Ergebnisse bis jetzt

### Vidéo : `sOjRNICiZ7Q` (allemand), segment 5 à 20 s

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Beobachtungen:**
- Aura hat eine Regel angewendet: `zehn finger` → `10 finger` ✅
- Le statut LT indique ces instructions inconnues — Verbindung wurde verweigert
- Hoher WER liegt am Segment : YouTube-Transcript start mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um the genaue Sekunde zu finden wo klar gesprochen wird
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/linguals` avant le test
3. **Modus C Tests hinzufügen** — Segment wo bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – Tests de régression audio : rapport d'état

**Date :** 2026-03-14  
**Fichier :** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Ce qui a été construit

Un système de test qui :
1. Télécharge un segment audio à partir d'une vidéo YouTube (via `yt-dlp` + `ffmpeg`)
2. Récupère la transcription YouTube générée automatiquement pour le même segment (via `youtube-transcript-api`)
3. Transcrit l'audio via Vosk
4. Transmet éventuellement le résultat via le **pipeline Aura complet** (`process_text_in_background`)
5. Calcule le taux d'erreur de mots (WER) entre la sortie Aura et la transcription YouTube
6. S'exécute comme un test de régression automatisé via `pytest`

Tous les téléchargements sont mis en cache (`scripts/py/func/checks/fixtures/youtube_clips/`) afin que les exécutions ultérieures soient rapides.

---

## 2. Fichiers

| Fichier | Objectif |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Fichier de test principal |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Clips audio mis en cache |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcriptions mises en cache |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Exclure le cache de Git |
| `contest.py` (racine du dépôt) | Définit PYTHONPATH pour pytest |

---

## 3. Modes de test

### Mode A – Vosk uniquement (référence)
```python
YoutubeAudioTestCase(
    test_id       = "my_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Teste uniquement la qualité Vosk. Pas d'Aura. Rapide.

### Mode B – Pipeline Aura complet, comparaison WER
```python
YoutubeAudioTestCase(
    test_id            = "my_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # stricter — Aura should improve on Vosk
    test_aura_pipeline = True,
)
```
Envoie la sortie Vosk via FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Mode C – Pipeline Aura complet, correspondance exacte de la sortie
```python
YoutubeAudioTestCase(
    test_id            = "command_open_terminal",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",   # Aura must produce exactly this
)
```
Pour les segments contenant une commande vocale connue. Mode de test le plus strict.

---

## 4. Ce qui est testé — ce qui ne l'est pas

| Quoi | Testé ? |
|---|---|
| Qualité Vosk STT | ✅ |
| Règles pré-FuzzyMap | ✅ (quand Aura est en cours d'exécution) |
| Corrections de LanguageTool | ✅ (lorsque LT est en cours d'exécution) |
| Règles de publication de FuzzyMap | ✅ (quand Aura est en cours d'exécution) |
| Sortie clavier (AutoHotkey/CopyQ) | ❌ intentionnel — au niveau du système d'exploitation, pas de logique |
| Rechargement du modèle Vosk | ❌ — Aura lit le fichier de sortie, ne recharge pas le modèle |

La sortie est lue à partir de `tts_output_*.txt` dans un répertoire temporaire — exactement comme Aura le fait en interne, pas depuis le terminal.

---

## 5. Démarrer les commandes

### Test normal (Aura doit déjà être en cours d'exécution) :
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Avec journal complet :
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Tests spécifiques uniquement :
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Démarrez Aura + LT en premier :
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. Configuration importante

### Codes de langue — deux systèmes différents !

| Système | Codes | Exemple |
|---|---|---|
| Dossier modèle Vosk | `de` | `models/vosk-model-de-0.21` |
| Dossier Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| API de transcription YouTube | `de` | `api.fetch(..., langues=["de"])` |

**Solution dans le code :** définissez `langue="de-DE"`. Le code gère automatiquement :
- Pour Vosk : `"de-DE"` → `"de"` (split sur `-`)
- Pour YouTube : `"de-DE"` → `"de"` (divisé sur `-`)
- Pour Aura : `"de-DE"` directement

### Désactivez le traducteur automatique avant les tests :
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sinon, Aura traduit le texte allemand en anglais, ce qui corrompt la mesure WER.

---

## 7. Problèmes connus et solutions

| Problème | Parce que | Corriger |
|---|---|---|
| `SIPÉ` immédiatement | Transcription YouTube introuvable | Appelez `api.list('video_id')` pour voir les langues disponibles |
| `SKIPPED` après l'audio | Modèle Vosk introuvable | `langue.split("-")[0]` repli dans le code |
| `Trouvé 0 règles FUZZY_MAP_pre` | Mauvais code de langue transmis à Aura | Utilisez `"de-DE"` et non `"de"` |
| `Connexion refusée 8010` | LT n'a pas démarré | Démarrez Aura en premier, attendez 60 s |
| `zsh : terminé` | Le chien de garde X11 tue le processus | Utilisez `SDL_VIDEODRIVER=dummy` ; augmenter le seuil de surveillance |
| Marqueurs YouTube `>>` | Deuxième intervenant dans la transcription | `re.sub(r'>>', '', text)` — supprime `>>` uniquement, conserve les mots |
| `AttributeError : get_transcript` | youtube-transcript-api v1.x | Utilisez `api = YouTubeTranscriptApi(); api.fetch(...)` |
| Le cache contient du texte vide | Ancienne exécution avec regex cassée | `rm luminaires/youtube_clips/*.transcript.json` |

---

## 8. Résultats jusqu'à présent

### Vidéo : `sOjRNICiZ7Q` (allemand), segment 5 à 20 s

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Observations :**
- Aura a appliqué une règle : `zehn finger` → `10 finger` ✅
- L'état du LT pendant cette exécution n'est pas clair — la connexion a été refusée
- Un WER élevé est dû au choix du segment : la transcription YouTube commence par des mots que Vosk ne peut pas entendre (l'orateur n'est pas encore au micro)
- **Recommandation :** déplacer le segment vers une section avec un discours clair

---

## 9. Prochaines étapes recommandées

1. **Choisissez un meilleur segment** — utilisez « ffplay » pour trouver la seconde exacte où la parole est claire
2. **Vérifiez l'état de LT avant le test** — `curl http://localhost:8010/v2/linguals` avant d'exécuter
3. **Ajouter des tests en mode C** — segments contenant des commandes vocales connues (`expected_output`)