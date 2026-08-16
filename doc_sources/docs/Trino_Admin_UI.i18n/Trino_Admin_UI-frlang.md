# Interface utilisateur d'administration Aura

L'interface utilisateur d'administration vous permet d'afficher et de modifier les paramètres Aura dans votre navigateur sans aucun coût en ressources inactives. Le serveur de tableau de bord ne s'exécute pas au démarrage ; il est démarré à la demande uniquement sur demande.

## Comment ouvrir (à la demande)

Vous pouvez lancer et ouvrir le tableau de bord d'administration de manière dynamique en utilisant l'une des trois méthodes suivantes :

### 1. Commande vocale
Parlez simplement dans votre microphone :
* *"administration de l'aura"

### 2. Commande Terminal / Console
Si vous travaillez dans le terminal, exécutez cette commande pour déclencher directement le lanceur :
```bash
s aura administration
```

*⚠️ **Remarque sur la plate-forme pour les utilisateurs Windows/macOS :** Le court wrapper de commande `s` est principalement configuré pour les environnements Linux. Veuillez lire la doc pour cela. Si vous utilisez Windows ou macOS, la commande « s » peut ne pas fonctionner immédiatement. Veuillez vous référer à notre documentation officielle de configuration CLI pour savoir comment configurer et implémenter l'alias de commande `s` pour votre système d'exploitation.*


### 3. Raccourci sur le bureau
Pour créer une icône de bureau spécifique à la plate-forme, exécutez une fois ce script de configuration :
```bash
python scripts/py/chat/install_shortcut.py
```
Ensuite, double-cliquez simplement sur l'icône **Aura Admin Dashboard** sur votre bureau.

---

## Accès direct au navigateur
Une fois le serveur lancé via l'une des méthodes à la demande ci-dessus, vous pouvez à tout moment accéder à l'interface directement dans votre navigateur :

http://localhost:8084

*(N'hésitez pas à ajouter ce lien à vos favoris dans votre navigateur !)*

---

## Ce que vous pouvez faire

- Voir l'état de la traduction pour chaque interface (parole, terminal, web).
- Activer ou désactiver la traduction par interface.
- Choisissez la langue cible (anglais, français, espagnol, etc.).

##Interfaces

| Interfaces | Descriptif |
|-----------|------------------------------------|
| discours | Entrée vocale (microphone) |
| borne | Ligne de commande (commande `s`) |
| Internet | Chat Web rationalisé (port 8831) |

## Exemple

Pour traduire uniquement les utilisateurs Web vers l'anglais, laissez la parole et le terminal désactivés, activez le Web avec la langue « en ».