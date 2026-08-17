En plus des nombreuses options de recherche, il existe probablement une recherche en texte intégral dans votre environnement de développement. Vous pouvez également utiliser :

scripts/search_rules/search_rules.sh

Cela vous permet de rechercher dans les cartes existantes ou dans le code source ou la documentation. et ensuite vous pouvez ouvrir la paix que vous avez trouvée dans votre éditeur préféré ou l'ouvrir sur github ou… veuillez configurer le script selon vos besoins.

MAPS_DIR est configurable via un argument positionnel ou une variable d'environnement

Le script conserve sa valeur par défaut codée en dur mais autorise les remplacements :

- Priorité : 1) premier paramètre de position ($1), 2) variable d'environnement MAPS_DIR existante,
3) "$SL5NET_AURA_PROJECT_ROOT/config/maps" par défaut codé en dur.
- Améliore la flexibilité pour CI, les remplacements locaux et les tests sans modifier le script.
- Ajoute des guillemets et une vérification de l'existence du répertoire pour échouer plus tôt si le chemin n'est pas valide.

Exemple d'utilisation :
- ./search_rules.sh utilise la valeur par défaut
- ./search_rules.sh ./docs utilise le chemin fourni
- MAPS_DIR=/env/maps ./search_rules.sh

Cela préserve la compatibilité ascendante tout en rendant la configuration explicite.

Il existe également une version pour PC Windows (dans ce dossier) qui permet de faire un peu moins : search_rules.ps1


(s, 28.3.'26 23:07 samedi)