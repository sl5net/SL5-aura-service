# Pleins feux sur les fonctionnalités : intégration de l'interface de ligne de commande (CLI)

**Dédié à mon ami très important, Lub.**

La nouvelle interface de ligne de commande (CLI) basée sur FastAPI offre un moyen propre et synchrone d'interagir avec notre service de traitement de texte principal en cours d'exécution à partir de n'importe quel shell local ou distant. Il s'agit d'une solution robuste conçue pour intégrer la logique de base dans les environnements shell.

---

## 1. Architecture et concept CLI synchrone

Le service est alimenté par le serveur **Uvicorn/FastAPI** et utilise un point de terminaison personnalisé (`/process_cli`) pour fournir un résultat synchrone (bloquant) à partir d'un processus en arrière-plan intrinsèquement asynchrone basé sur des fichiers.

### Stratégie de sondage en attente et lecture

1. **Remplacement de sortie unique :** L'API crée un répertoire temporaire unique pour chaque requête.
2. **Démarrage du processus :** Il appelle `process_text_in_background` pour exécuter la logique principale dans un thread non bloquant, en écrivant le résultat dans un fichier `tts_output_*.txt` dans ce dossier unique.
3. **Attente synchrone :** La fonction API **bloque** et interroge le dossier unique jusqu'à ce que le fichier de sortie soit créé ou qu'un délai d'attente soit atteint.
4. **Livraison du résultat :** L'API lit le contenu du fichier, effectue le nettoyage nécessaire (suppression du fichier et du répertoire temporaire) et renvoie le texte final traité dans le champ « result_text » de la réponse JSON.

Cela garantit que le client CLI ne reçoit une réponse *une fois* le traitement du texte terminé, garantissant une expérience shell fiable.

## 2. Accès à distance et mappage des ports réseau

Pour permettre l'accès à partir de clients distants comme le terminal de Lub, la configuration réseau suivante était requise, répondant à la contrainte courante de disponibilité limitée des ports externes :

### Solution : Mappage des ports externes

Étant donné que le service s'exécute en interne sur le **Port 8000** et que notre environnement réseau limite l'accès externe à une plage de ports spécifique (par exemple, « 88__-8831 »), nous avons implémenté le **Mappage de ports** sur le routeur (Fritz!Box).

| Point de terminaison | Protocole | Port | Descriptif |
| :--- | :--- | :--- | :--- |
| **Externe/Public** | TCP | `88__` (Exemple) | Le port que le client (Lub) doit utiliser. |
| **Interne/Local** | TCP | « 8 000 » | Le port sur lequel le service FastAPI écoute réellement (`--port 8000`). |

Le routeur traduit toute connexion entrante sur le port externe (`88__`) vers le port interne (`8000`) de la machine hôte, rendant le service globalement accessible sans modifier la configuration du serveur principal.

## 3. Utilisation du client CLI

Le client doit être configuré avec l'adresse IP publique, le port externe et la clé API correcte.

### Syntaxe de la commande finale

__CODE_BLOCK_0__