# 🧠 SL5 Aura : intégration avancée de LLM hors ligne

**Statut :** Prêt pour la production
**Moteur :** Ollama (Llama 3.2 3B)
**Latence :** Instantanée (<0,1 s en cas d'accès au cache) / ~ 20 s (génération sur CPU)

## 1. La philosophie "Architecte & Stagiaire"
Aura fonctionne sur un modèle hybride pour équilibrer **précision** et **flexibilité** :
* **The Architect (RegEx/Python) :** Exécution déterministe et instantanée des commandes système (par exemple, "Open Browser", "Volume Up").
* **Le stagiaire (Local LLM) :** Gère les requêtes floues, les résumés et les connaissances générales. Il n'est déclenché que si aucune correspondance de règle stricte ou aucun mot-clé spécifique n'est utilisé.

---

## 2. Architecture des performances

Pour rendre un LLM local utilisable sur des processeurs standards sans accélération GPU, nous avons mis en œuvre une **stratégie de performances à 3 couches** :

### Couche 1 : Le « Mode instantané » (Mots clés)
* **Déclencheur :** Des mots comme "Instant", "Schnell", "Sofort".
* **Logique :** Contourne entièrement le LLM. Il compare les mots-clés saisis par l'utilisateur à la base de données SQLite locale à l'aide d'une intersection définie.
* **Latence :** **< 0,05 s**

### Couche 2 : Le Smart Cache (SQLite)
* **Logique :** Chaque invite est hachée (SHA256). Avant de demander à Ollama, nous vérifions `llm_cache.db`.
* **Fonction « Variation active » :** Même s'il existe un résultat dans le cache, le système génère parfois (20 % de chances) une *nouvelle* variante pour apprendre différentes formulations pour la même question. Idéalement, nous stockons environ 5 variantes par question.
* **Fonction "Hashing sémantique" :** Pour les questions longues (> 50 caractères), nous utilisons le LLM pour extraire d'abord les mots-clés (par exemple, "guide d'installation") et les hacher au lieu de la phrase complète. Cela correspond à « Comment puis-je installer ? » avec "Instructions d'installation s'il vous plaît".
* **Latence :** **~0,1 s**

### Couche 3 : La génération d'API (repli)
* **Logique :** Si aucun cache n'existe, nous appelons l'API Ollama (`http://localhost:11434/api/generate`).
* **Optimisation :**
* **Limites strictes :** `num_predict=60` force le modèle à s'arrêter après environ 40 mots.
* **Input Piping :** Les textes volumineux (README) sont transmis via STDIN pour éviter les limites d'arguments du système d'exploitation.
* **Latence :** **~15-25 s** (en fonction du processeur)

---

## 3. Mise à la terre du système (anti-hallucination)

Les LLM génériques ont tendance à inventer des éléments GUI (boutons, menus). Nous injectons un **`AURA_TECH_PROFILE`** strict dans chaque invite système :

1. **Pas d'interface graphique :** Aura est un service CLI sans tête.
2. **Aucun fichier de configuration :** La logique est du code Python, pas `.json`/`.xml`.
3. **Déclencheurs :** Le contrôle externe fonctionne via la création de fichiers (`touch /tmp/sl5_record.trigger`), et non via les API.
4. **Installation :** Prend 10 à 20 minutes en raison des téléchargements de modèles de 4 Go (évite les mensonges "Il s'installe en 3 secondes").

---

## 4. Le pont du Presse-papiers (sécurité Linux)

Les services d'arrière-plan (systemd) ne peuvent pas accéder directement au presse-papiers X11/Wayland en raison de l'isolement de sécurité.
* **Solution :** Un script de session utilisateur (`clipboard_bridge.sh`) reflète le contenu du presse-papiers dans un fichier du disque RAM (`/tmp/aura_clipboard.txt`).
* **Aura :** Lit ce fichier, en contournant tous les problèmes d'autorisation.

---

## 5. Auto-apprentissage (réchauffement du cache)

Nous fournissons un script `warm_up_cache.py`.
1. Il lit le projet `README.md`.
2. Il demande au LLM d'inventer des questions probables des utilisateurs sur le projet.
3. Il simule ces questions contre Aura pour pré-remplir la base de données.