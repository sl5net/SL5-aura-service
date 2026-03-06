prévu de ne pas fonctionner pour le moment sans mot de passe sur les dossiers quelque part. les fichiers de mots de passe doivent commencer par un point "."


# Flux de travail auto-zip et documentation intégrée

## Concept
SL5 Aura surveille automatiquement les dossiers commençant par `_` (par exemple, `_my_application`). Lorsque des modifications sont détectées, Aura compresse automatiquement le dossier dans une archive zip.

**Contrainte critique :**
Le système de « rechargement à chaud » et de surveillance d'Aura écoute spécifiquement les modifications dans les **fichiers Python valides**. Une simple mise à jour d'un fichier texte (`.txt`) ne déclenchera **pas** le processus de zip automatique.

## Le modèle "Documents intégrés"
Pour inclure des instructions pour les destinataires non techniques (par exemple, RH, clients) tout en garantissant qu'Aura détecte le changement et met à jour le zip, nous utilisons un **fichier Python Docstring**.

Ce fichier est techniquement un script Python valide (satisfaisant l'analyseur d'Aura) mais apparaît visuellement comme un document texte standard pour l'utilisateur.

### Mise en œuvre
Créez un fichier nommé « README_AUTOZIP.py » dans votre dossier surveillé.

**Guide de style :**
1. Utilisez `# Documentation` comme première ligne (au lieu d'un nom de script technique) pour être accueillant.
2. Utilisez une Docstring Triple-Quote (""""`) pour le contenu.
3. Aucun autre code n'est requis.

### Exemple de code

__CODE_BLOCK_0__