docker build -t stt-service .

docker run -it --rm --name stt-container stt-service

docker exec stt-container touch /tmp/sl5_record.trigger


Essayer de conteneuriser l'application avec Docker est une étape « sophistiquée » fantastique. C'est le moyen ultime de résoudre le problème « ça fonctionne sur ma machine » en regroupant l'application et toutes ses dépendances dans une seule image portable.

Cependant, nous allons rencontrer quelques défis fondamentaux car cette application est conçue pour interagir avec le bureau de l'hôte (audio, clavier). C'est quelque chose que Docker est explicitement conçu pour *empêcher*.

### Comment créer et exécuter l'image Docker

1. **Créez l'image :** Ouvrez un terminal à la racine de votre projet et exécutez :
    ```bash
    docker build -t stt-service .
    ```
2. **Exécutez le conteneur :**
    ```bash
    docker run -it --rm --name stt-container stt-service
    ```

### Le résultat : ce qui fonctionne et ce qui (essentiellement) ne fonctionne pas

Avec un peu de chance, le conteneur sera construit et exécuté. Vous devriez voir la sortie du journal de « aura_engine.py » indiquant qu'il a démarré, chargé les modèles et qu'il est maintenant en attente.

**C'est un succès partiel !** L'application principale Python et ses dépendances s'exécutent dans un environnement parfaitement isolé.

**CEPENDANT, l'application est désormais fondamentalement cassée en raison de la conception de Docker :**

1. **AUCUN accès au microphone :** Le conteneur est isolé du matériel de votre hôte. La bibliothèque `sounddevice` échouera lorsqu'elle tentera de trouver un périphérique d'entrée.
* *Solution de contournement (Linux uniquement) :* Vous pouvez essayer de monter le périphérique audio de l'hôte dans le conteneur en ajoutant `--device /dev/snd` à votre commande `docker run`. Ceci est complexe et spécifique à l’hôte.

2. **AUCUNE sortie de saisie (`xdotool`) :** Le conteneur n'a pas accès à l'environnement de bureau ou aux fenêtres de votre hôte. Il ne peut pas « saisir » du texte dans une autre application. Cette fonctionnalité est complètement interrompue par la conception.

3. **AUCUNE notification sur le bureau (« notify-send ») :** Comme ci-dessus. Le conteneur ne peut pas envoyer de notifications sur le bureau de votre hôte.

4. **AUCUN déclencheur de fichier (`inotify`) :** Le déclencheur de fichier basé sur `inotify` ne fonctionnera pas comme prévu. Vous ne pouvez pas simplement « toucher /tmp/sl5_record.trigger » sur votre machine hôte. Vous devrez utiliser une commande distincte pour créer le fichier *à l'intérieur* du conteneur en cours d'exécution :
    ```bash
    docker exec stt-container touch /tmp/sl5_record.trigger
    ```

### Conclusion : "Fantastique" mais fondamentalement incompatible

La création de ce Dockerfile prouve que la **logique principale** de l'application peut être empaquetée. Cependant, cela prouve également que la conception actuelle de l'application, qui repose sur une interaction directe entre le matériel (micro) et le bureau (saisie, notifications), est **fondamentalement incompatible avec la conteneurisation.**

Pour que cela fonctionne réellement dans Docker, l'application devrait être réorganisée :
* Au lieu d'écouter un micro local, il faudrait qu'il accepte un flux audio sur le réseau (par exemple via une API Web).
* Au lieu de taper du texte avec `xdotool`, il faudrait renvoyer le texte transcrit via cette même API Web.