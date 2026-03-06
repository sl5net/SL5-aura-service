# 🧠 SL5 Aura : Intégration LLM hors ligne simple

**Statut :** Société de production
**Moteur :** Ollama (Llama 3.2 3B)
**Latence :** Sofort (<0,1 s après cache hit) / ~ 20 s (génération du processeur)

## 1. La philosophie "Architekt & Praktikant"
Aura propose un modèle hybride, une **Präzision** et une **Flexibilität** à utiliser :
* **Der Architekt (RegEx/Python) :** Deterministische, sofortige Ausführung für Systembefehle ("Browser öffnen", "Lauter").
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. Wird nur aktiv, wenn keine strikte Regel greift.

---

## 2. Architecture de performance

Un LLM local sur des processeurs normaux (sans GPU) peut être utilisé pour les machines, définissant une stratégie à 3 niveaux :

### Niveau 1 : Le "Modus instantané" (Schlagworte)
* **Déclencheur :** Wörter comme "Instant", "Schnell", "Sofort".
* **Logique :** Umgeht das LLM komplett. Vergleicht Schlagworte der Eingabe directement avec la banque de données SQLite.
* **Latence :** **< 0,05 s**

### Étape 2 : Le cache intelligent (SQLite)
* **Logique :** Cette invite est utilisée (SHA256). Pour cette réponse, un Ollama sera utilisé par `llm_cache.db`.
* **Fonction « Variation active » :** Auch bei un cache-treffer generiert the system manchmal (20% Chance) proaktiv aine *new* Answer-Variante. Ziel: ~5 Variantes pro Frage für more Lebendigkeit.
* **Fonction « Hashing sémantique » :** Lors d'une longue période (> 50 fois), le LLM est extrait des mots-clés (par exemple, "lecture d'installation") et de ce hachage. Alors, "Qu'est-ce que tu as installé ?" et "Installationshilfe bitte" comme identisch erkannt.
* **Latence :** **~0,1 s**

### Étape 3 : La génération d'API (repli)
* **Logique :** Si un cache existe, vous pouvez utiliser l'API Ollama (`http://localhost:11434/api/generate`).
* **Optimisation :**
* **Limites strictes :** `num_predict=60` zwingt das Modell, nach ca. 40 Wörtern zu stoppen.
* **Input Piping :** Le gros texte (README) apparaît sur STDIN, un argument sur les limites des systèmes de gestion zu umgehen.
* **Durée :** **~15-25s** (sans CPU)

---

## 3. Mise à la terre du système (anti-halluzination)

Les LLM génériques proposent de nombreuses interfaces graphiques (boutons, menus). Nous vous invitons à utiliser cette fonction **`AURA_TECH_PROFILE`** :

1. **Keine GUI :** Aura est un logiciel CLI sans tête.
2. **Keine Config-Files :** La logique est le meilleur code Python, comme `.json`/`.xml`.
3. **Déclencheur :** Une gestion externe est effectuée via les événements du système de données (`touch /tmp/sl5_record.trigger`), pas via les API.
4. **Installation :** Durée réelle de 10 à 20 minutes avec 4 Go de téléchargements de modèles (vérifier de faux versions).

---

## 4. Die Clipboard Bridge (Sécurité Linux)

Les arrière-plans (systemd) ne peuvent souvent pas être connectés au réseau de sécurité (X11/Wayland).
* **Lusung:** Un script dans la session utilisateur (`clipboard_bridge.sh`) apparaît dans une date de disque RAM (`/tmp/aura_clipboard.txt`).
* **Aura :** Cette date est la plus importante et c'est le cas de tous les problèmes réels.

---

## 5. Selbst-Lernen (réchauffement du cache)

Nous utilisons le script `warm_up_cache.py` :
1. Voici le `README.md` des projets.
2. Es beauftragt das LLM, sich wahrscheinliche User-Fragen auszudenken.
3. Vous avez trouvé ces fragments et auras, la banque de données étant automatiquement remplie.