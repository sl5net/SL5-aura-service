## Guide du développeur : expressions régulières avancées de carte floue

Le système Fuzzy Mapping utilise des expressions régulières Python standard, permettant de puissants modèles de correspondance et d'exclusion, notamment via des **Negative Lookaheads (`(?!...)`)**.

### Utilisation d'anticipations négatives pour la liste blanche

Ce modèle vous permet de définir une règle qui s'applique à **tout SAUF** une liste spécifique de mots ou d'expressions. Ceci est particulièrement utile en combinaison avec le modèle `empty_all` pour créer des ensembles de règles cumulatifs et restreints.

| Objectif | Exemple de règle (`FUZZY_MAP`) | Explication |
| :--- | :--- | :--- |
| **Appliquer à tous sauf un mot** | `('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE})` | Cette règle appliquera un remplacement (ou une logique de saut, ici ``'`) à **tout texte** qui n'est *pas* exactement "Haus". `(?!Haus)` est l'anticipation négative, garantissant que le texte ne commence pas par « Haus ». |
| **Appliquer à tous sauf plusieurs mots** | `('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags' : re.IGNORECASE})` | Cette règle s'applique à **tout** qui ne commence pas par « Schach », « Matt », « bad » ou « Haus ». Utilisez le canal OR (`|`) dans le groupe d'analyse anticipée `(?!...)` pour mettre plusieurs termes sur liste blanche. |

***

### Utilisation d'anticipations positives pour les règles restreintes

L'approche standard utilise des anticipations positives ou de simples groupes de capture pour restreindre une règle à *uniquement* une liste spécifique de mots.

| Objectif | Exemple de règle (`FUZZY_MAP`) | Explication |
| :--- | :--- | :--- |
| **Appliquer uniquement à une liste spécifique** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags' : re.IGNORECASE})` | Cette règle ne s'applique que si le texte commence par l'un des mots répertoriés (Schach, Matt, bad ou Haus). Le texte correspondant est ensuite remplacé par la cible (« Schachmatt ») en fonction du seuil. |