# Zip automatique sécurisé et documentation intégrée

## Concept
SL5 Aura surveille les dossiers privés commençant par `_` (par exemple, `_my_confidential_data`).
Lorsque des modifications sont détectées, Aura crée automatiquement une archive zip **cryptée**.

## Condition préalable critique : clé de cryptage
**Le cryptage est obligatoire.** Le processus de zip automatique nécessite strictement qu'un fichier de mot de passe soit présent dans la hiérarchie des répertoires (dossiers actuels ou parents).

* **Exigence relative au fichier :** Le fichier de mot de passe doit commencer par un point `.` (par exemple, `.archive_pass`, `.secret`).
* **Comportement :** Si aucun fichier dot avec un mot de passe n'est trouvé, le processus zip est **bloqué**. Cette sécurité garantit qu'aucune donnée non cryptée n'est jamais empaquetée.

## Le modèle "Documents intégrés"
Étant donné que le système de rechargement à chaud d'Aura écoute les **fichiers Python valides**, la mise à jour d'un simple fichier readme `.txt` ne déclenchera pas de re-zip.

Pour inclure des instructions pour les destinataires (par exemple, « Comment décompresser ») tout en garantissant le déclenchement du déclencheur, utilisez un **Fichier Docstring Python**.

### Mise en œuvre
Créez un fichier nommé « README_AUTOZIP.py » dans votre dossier surveillé.

__CODE_BLOCK_0__