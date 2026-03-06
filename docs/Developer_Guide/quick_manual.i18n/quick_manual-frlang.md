## Attributs de règle avancés

En plus des champs standards, les règles peuvent être enrichies d'options spéciales :

### `only_in_windows` (Filtre de titre de fenêtre)
Malgré son nom, cet attribut est **indépendant du système d'exploitation**. Il filtre les règles en fonction du titre de la fenêtre actuellement active.

* **Fonction :** La règle n'est traitée que si le titre de la fenêtre active correspond à l'un des modèles fournis (Regex).
*   **Exemple:**
    ```python
    (
        '|', 
        r'\b(pipe|symbol)\b', 
        75, 
        {'only_in_windows': ['Terminal', 'Console', 'iTerm']}
    ),
    ```
*Dans ce cas, le remplacement n'a lieu que si l'utilisateur travaille dans une fenêtre de terminal.*

### `on_match_exec` (Exécution de script)
Permet de déclencher des scripts Python externes lorsqu'une règle correspond.

* **Syntaxe :** `'on_match_exec' : [CONFIG_DIR / 'script.py']`
* **Cas d'utilisation :** Idéal pour les actions complexes telles que les appels d'API, les tâches de système de fichiers ou la génération de contenu dynamique.