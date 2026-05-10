# Notifications de flux de travail (alertes audio)

Pour améliorer la productivité, vous pouvez configurer un alias Git local qui transmet votre code et vous alerte automatiquement (via la voix ou le son) dès que le workflow GitHub Actions est terminé. Cela évite la « fatigue liée à l'observation de GitHub » et vous permet de vous concentrer sur d'autres tâches.

### Prérequis

Vous avez besoin de **GitHub CLI** et d'un moteur de synthèse vocale ou d'un lecteur audio installés sur votre système.

**Pour Manjaro/Arch Linux :**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### Installation

Exécutez la commande suivante dans votre terminal pour créer un alias Git global appelé « pushsound » :

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### Utilisation

Au lieu de `git push`, exécutez simplement :
```bash
git pushsound
```
Votre terminal attendra la fin du workflow, puis annoncera : *"tout le workflow github est terminé"*.

---

### Personnalisation et alternatives

Selon vos préférences, vous souhaiterez peut-être utiliser un autre nom d'alias ou une autre méthode de notification.

#### 1. Noms d'alias recommandés
Si « pushsound » est trop long à saisir, envisagez ces alternatives :
* `git pw` (Push & Watch) — **Recommandé pour la vitesse.**
* `git sync` (implique d'appuyer et d'attendre le "feu vert")
* `git palert` (alerte push)

#### 2. Styles de notifications
Vous pouvez échanger la partie `espeak-ng` contre d'autres types d'alertes :

* **Notifications sur le bureau :**
`... && notify-send "Action GitHub" "Workflow terminé !"`
* **Son du système (cloche) :**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **Combinaison (Son + Voix) :**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Terminé"`

#### 3. Avancé : version Team-Safe
Si plusieurs développeurs poussent simultanément vers le même référentiel, la commande par défaut peut suivre la mauvaise exécution. Utilisez cette version « Branch-Safe » pour surveiller uniquement votre propre branche actuelle :

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'

git config --global alias.pushsound '!git push && sleep 3 && (gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") --exit-status && espeak-ng "workflow successful" || espeak-ng "workflow failed")'

```

### Dépannage
* **"Aucune exécution trouvée":** Nous incluons un "sleep 3" car GitHub prend un moment pour enregistrer le push et démarrer le flux de travail. Si votre connexion est très lente, vous devrez peut-être l'augmenter à « veille 5 ».
* **Bips du terminal :** Si `espeak-ng` ne fonctionne pas, assurez-vous que votre audio n'est pas coupé et que le package est correctement installé.