# Guide du développeur : génération du graphique des appels de service

Ce document décrit la méthode robuste et thread-safe pour générer un graphique d'appel visuel du `aura_engine.py` de longue durée. Nous utilisons le profileur `yappi` (pour le support multi-threading) et `gprof2dot` pour la visualisation.

### Prérequis

Assurez-vous que les outils nécessaires sont installés globalement ou dans votre environnement virtuel :

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### Étape 1 : Modification du service pour le profilage

Le script `aura_engine.py` doit être modifié pour démarrer manuellement le profileur `yappi` et enregistrer gracieusement les données de profilage en cas d'interruption (`Ctrl+C`).

**Changements clés dans `aura_engine.py` :**

1. **Importations et gestionnaire de signaux :** Importez `yappi` et définissez la fonction `generate_graph_on_interrupt` (telle qu'implémentée précédemment) pour appeler `yappi.stop()` et `stats.save(...)`.
2. **Start/Stop :** Ajoutez `yappi.start()` et `signal.signal(signal.SIGINT, ...)` dans le bloc `if __name__ == "__main__":` pour encapsuler l'exécution de `main(...)`.

### Étape 2 : Exécution du service et collecte des données

Exécutez directement le script modifié et laissez-le traiter les données pendant une durée suffisante (par exemple, 10 à 20 secondes) pour garantir que toutes les fonctions principales, y compris celles liées aux threads (comme la correction de LanguageTool), sont appelées.

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

Appuyez une fois sur **Ctrl+C** pour déclencher le gestionnaire de signal. Cela arrêtera le profileur et enregistrera les données brutes dans :

`\mathbf{yappi\_profile\_data.prof`

### Étape 3 : Génération et filtrage du graphique visuel

Nous utilisons `gprof2dot` pour convertir les données brutes `pstats` au format SVG. Étant donné que les options de filtrage avancées telles que `--include` et `--threshold` peuvent ne pas être prises en charge par notre environnement spécifique, nous utilisons le filtre de base **`--strip`** pour nettoyer les informations de chemin et réduire l'encombrement des composants internes du système.

**Exécutez la commande de visualisation :**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### Étape 4 : Documentation (Recadrage manuel)

Le fichier `yappi_call_graph_stripped.svg` (ou `.png`) résultant sera volumineux, mais il contient avec précision le flux d'exécution complet, y compris tous les threads.

À des fins de documentation, **recadrez manuellement l'image** pour vous concentrer sur la logique centrale (les 10 à 20 nœuds principaux et leurs connexions) afin de créer un graphique d'appel ciblé et lisible pour la documentation du référentiel.

### Archivage

Le fichier de configuration modifié et la visualisation finale du Call Graph doivent être archivés dans le répertoire source de la documentation :

| Artefact | Localisation |
| :--- | :--- |
| **Fichier de service modifié** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **Image recadrée finale** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **Données de profilage brutes** | *(Facultatif : doit être exclu de la documentation du référentiel final)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")