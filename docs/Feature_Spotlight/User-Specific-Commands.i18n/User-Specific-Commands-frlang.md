# Commandes vocales spécifiques à l'utilisateur

Aura vous permet de définir des commandes personnalisées qui ne sont **actives que pour vous** (ou pour des membres spécifiques de l'équipe). Cela empêche que des raccourcis personnels ou des fonctionnalités expérimentales soient déclenchés par d'autres utilisateurs.

## Installation

Vous pouvez appliquer ces règles dans n'importe quel fichier de mappage, tel que `FUZZY_MAP_pre.py` (entrée brute) ou `FUZZY_MAP.py` (après correction).

Fichier cible : `config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py`

### Exemple de code

Ajoutez ce bloc à la fin du fichier :

__CODE_BLOCK_0__