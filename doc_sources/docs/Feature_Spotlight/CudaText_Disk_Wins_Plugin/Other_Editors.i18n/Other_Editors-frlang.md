# Rechargement automatique dans d'autres éditeurs

Ce document décrit comment mettre en place le rechargement automatique sur
modifications de fichiers dans les éditeurs courants - et pourquoi cela n'est souvent **pas suffisant**
en mode Aura Oma.

---

## Kate (KDE)

### Installation

1. **Paramètres → Configurer Kate → Ouvrir/Enregistrer → Avancé**
2. Activez :
- **"Recharger automatiquement les fichiers"**

### Ce qui fonctionne

- Lorsque le tampon est **inchangé**, Kate recharge immédiatement le fichier.
- C'est suffisant pour le mode visualisation pure.

### Qu'est-ce qui ne fonctionne **pas** (et pourquoi cela échoue en mode Oma)

- Dès que vous appuyez sur **une seule touche** dans le buffer (même juste un
espace ou frappe accidentelle), le tampon est considéré comme "modifié".
- À partir de ce moment, Kate demande **toujours** à chaque changement externe :
> "Le fichier a été modifié en externe. Voulez-vous le recharger ?"
- En mode Oma, l'utilisateur peut ne pas être devant l'ordinateur ou ne pas voir le
dialogue — Aura continue d'écrire, mais l'éditeur reste sur l'ancienne version.
- **Kate n'a aucun paramètre** qui ignore silencieusement les modifications de tampon non enregistrées
en faveur de la version disque.

> **En résumé :** Kate ne convient pas au mode Oma dès que l'utilisateur
> tape accidentellement dans l'éditeur.

---

## VSCode

### Installation

Dans `settings.json` :

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

### Limites

- `autoSave` enregistre le tampon — il écrase les modifications d'Aura avec le
version locale, et non l'inverse.
- Une invite apparaît toujours pour les modifications non enregistrées.
- Aucune option pour "le disque gagne toujours".

---

##Emacs

```elisp
(global-auto-revert-mode t)
```

### Limites

- Ne se recharge automatiquement que lorsque le tampon est inchangé.
- Demande quand le tampon est modifié.

---

## Vim / Néovim

```vim
set autoread
au FocusGained,BufEnter,CursorHold * :checktime
```

### Limites

- `autoread` ne se recharge que lorsque le tampon est inchangé.
- N'écrase pas automatiquement un tampon « modifié ».

---

## CudaText (sans plugin)

Dans `user.json` :

```json
{
    "ui_notif": true,
    "ui_notif_confirm": 0
}
```

### Limites

- Toutes les valeurs de `ui_notif_confirm` (0–4) affichent une forme d'invite —
modal ou sans modal.
- Il n'y a **aucune** valeur qui signifie : "Recharger immédiatement, ne jamais demander."
- Le plugin `cuda_disk_wins` est donc requis.

---

## Aperçu

| Editeur | Rechargement automatique (inchangé) | Rechargement automatique (modifié) | Licence |
|--------|-------------------------|--------------|---------|
| Kate | Oui | Invite toujours | Ouvert |
| Code VS | Oui | Invite toujours | Ouvert |
| Texte sublime | Oui | Invite toujours | Propriétaire |
| Emacs | Oui | Invite toujours | Ouvert |
| Vim | Oui | Invite toujours | Ouvert |
| CudaText (pas de plugin) | Oui | Invite toujours | Ouvert |
| **CudaText + Gains de disque** | Oui | **Aucune invite** | Ouvert |

---

## Pourquoi aucun éditeur ne peut faire cela directement

Supprimer silencieusement les modifications non enregistrées est considéré comme une ** perte de données massive
bug** dans le développement de logiciels. Aucun éditeur sérieux ne propose de paramétrage
"écraser mon tampon sans demander". C'est exact et important...
pour le travail normal du développeur.

En mode Aura Oma, cependant, la priorité est inversée : Aura est la source
de vérité, et le tampon de l'éditeur humain est secondaire. Par conséquent un
une intervention explicite du plugin est nécessaire pour appliquer ce comportement pour
ce cas d’utilisation spécifique.