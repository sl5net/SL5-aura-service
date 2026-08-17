# Plugin CudaText : "Disk Wins" (Forcer le rechargement automatique en cas de changement externe)

CudaText n'a pas d'option intégrée qui recharge silencieusement un fichier au moment où il
modifications sur le disque — chaque mode intégré « modifié sur le disque » en affiche toujours
sorte d'invite (modale ou sans modal) avant de recharger
(voir `ui_notif_confirm` dans `default.json`, valeurs `0`-`4`, qui sont toutes
demander). Ce plugin comble cette lacune : **le disque gagne toujours**, jamais d'invite.

Archivé ici afin que personne n'ait besoin de rediriger l'API du plugin CudaText pour cela
encore. La source de vérité pour le plugin lui-même réside dans
[`cuda_disk_wins/`](.././cuda_disk_wins/) dans ce dossier.

## Ce que ça fait

- Interroge chaque fichier ouvert et nommé une fois par seconde (configurable via
`TIMER_INTERVAL` dans `__init__.py`).
- Si l'heure mtime d'un fichier sur le disque change, le plugin le relit et appelle
`Editor.set_text_all()` — ** écrasant toutes les modifications non enregistrées dans le
onglet éditeur sans demander**.
- Efface ensuite le flag "modifié" (`PROP_MODIFIED = False`), donc le
L'onglet semble propre, comme si rien n'avait jamais divergé.
- Au mieux, restaure la position du curseur et la ligne supérieure visible après
recharger.
- Ajoute deux commandes sous `Plugins → Disk Wins` :
- `Activer/Désactiver le rechargement automatique`
- « Vérifier maintenant » (vérification manuelle ponctuelle)

## Pourquoi un plugin au lieu d'un paramètre

Le propre observateur de fichiers de CudaText (`ui_notif`) ne propose que des comportements « demander » :

| `ui_notif_confirm` | Comportement |
|---------------------|----------------------------------------------------|
| 0 | invite sans modale, toujours |
| 1 | invite sans modale, si l'éditeur est modifié ou si Annuler n'est pas vide |
| 2 | invite sans modale, si l'éditeur est modifié |
| 3 | invite modale, toujours |
| 4 | invite modale, si l'éditeur est modifié |

Il n'y a aucune valeur qui signifie "recharger automatiquement, pas d'invite, continuer".
D'où ce petit plugin, qui exécute sa propre boucle d'interrogation et recharge
directement via l'API Python.

##Installation

```bash
mkdir -p ~/.config/cudatext/py
cp -r cuda_disk_wins ~/.config/cudatext/py/
```

Redémarrez CudaText.

**Important :** désactivez également la boîte de dialogue de notification de modification de CudaText afin
ça ne se bat pas avec le plugin. Dans
`~/.config/cudatext/settings/user.json` :

```json
{
    "ui_notif": false
}
```

(Équivalent à « Options → Paramètres – configuration utilisateur » dans l'interface utilisateur.) Redémarrer
CudaText à nouveau après ce changement.

## Mises en garde

- Ceci est intentionnellement destructeur : les modifications non enregistrées de l'éditeur sont ignorées.
silencieusement au moment où le fichier change en externe. C'est tout
point du plugin — ne l'installez pas si vous souhaitez parfois conserver
les modifications locales par rapport aux modifications externes.
- Réagit uniquement aux changements dans le mtime du fichier ; taper dans l'éditeur lui-même
ne déclenche pas de rechargement (pas de boucle de rétroaction).
- Si le fichier est supprimé en externe, le plugin ne fait rien jusqu'à ce qu'il
réapparaît (pas de crash, pas de tentatives de rechargement répétées).
- L'encodage est lu via `PROP_ENC` et mappé au codec Python le plus proche ;
étendez `ENC_MAP` dans `__init__.py` si vous n'utilisez pas déjà un encodage
répertorié.

## Origine

Conçu pour "préférer toujours les modifications du système de fichiers à l'éditeur non enregistré".
tampons, aucune confirmation" exigence discutée lors de la configuration de CudaText
via `yay -S cudatext-qt6-bin python` sur Arch.