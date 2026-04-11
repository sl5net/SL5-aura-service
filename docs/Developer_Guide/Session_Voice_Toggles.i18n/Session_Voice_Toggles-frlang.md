# Gestion audio de session et bascules vocales

Aura implémente une boucle de traitement audio basée sur la session. Les commandes vocales pour la gestion de l'état ne sont actives que dans le cadre d'une session d'enregistrement établie.

##Configuration
Le comportement interne à la session est contrôlé par :
`ENABLE_WAKE_WORD = True/False` (dans `config/settings.py`)

## Logique opérationnelle
Contrairement à un écouteur persistant en arrière-plan, le moteur STT d'Aura (Vosk) ne traite l'audio que lorsqu'une session d'enregistrement a été déclenchée en externe (par exemple via Hotkey).

> **Aura est votre télescope 🔭 pour PC : contrôlez à distance !**


### La bascule en session ("Teleskop")
Lorsque `ENABLE_WAKE_WORD` est défini sur **True** :
1. **Déclencheur :** L'utilisateur démarre une session manuellement.
2. **Toggle :** Dire « Teleskop » pendant la session bascule entre les états **ACTIVE** et **SUSPENDED**.
3. **Comportement :** Cela permet à l'utilisateur de "mettre en pause" et de "reprendre" le traitement du texte à l'aide de commandes vocales sans mettre fin au flux audio.

### Confidentialité et efficacité
Lorsque `ENABLE_WAKE_WORD` est défini sur **False** (par défaut) :
- **STT Suppression :** Lorsqu'ils sont dans un état suspendu, les appels à `AcceptWaveform` et `PartialResult` sont complètement ignorés.
- **Confidentialité :** Aucune donnée audio n'est analysée sauf si le système est dans un état actif explicite.
- **Gestion des ressources :** L'utilisation du processeur est minimisée en contournant l'analyse du réseau neuronal pendant la suspension.

## Latence et performances
- **Reprise instantanée :** Étant donné que `RawInputStream` reste ouvert tout au long de la session, le passage de SUSPENDED à ACTIVE a **0 ms de latence supplémentaire**.
- **Loop Timing :** La boucle de traitement fonctionne à un intervalle d'environ 100 ms (`q.get(timeout=0.1)`), garantissant des temps de réponse quasi instantanés.