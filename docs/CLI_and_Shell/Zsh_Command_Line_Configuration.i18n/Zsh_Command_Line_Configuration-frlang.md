Ce document résume la configuration Zsh finale et vérifiée pour interagir avec votre service Python via la ligne de commande.

La configuration propose trois méthodes distinctes pour accéder au service, allant de la sortie sécurisée à l'exécution immédiate.

## Résumé de la configuration de la ligne de commande Zsh

### 1. Fichier de configuration

Tout le code ci-dessous doit être collé dans votre fichier **`~/.zshrc`**. N'oubliez pas de **`source ~/.zshrc`** ou d'ouvrir une nouvelle session de terminal après avoir apporté des modifications.

### 2. Le bloc de code final

Ce bloc définit les trois fonctions requises. Il inclut les commandes « unalias » nécessaires pour éviter l'erreur de conflit que nous avons rencontrée précédemment.

```bash
# ===================================================================
# == 1. sl: Output Only (Safe Mode - Just prints the result)
# ===================================================================

# Unalias 'sl' in case it was previously defined as a simple alias
unalias sl 2>/dev/null
sl() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/scripts/py/cli_client.py "$*" --lang "de-DE"
}
# source ~/.zshrc


# ===================================================================
# == 2. slz: Zsh Line Insertion (Safe Prep Mode - Paste output to prompt)
# ===================================================================

# Unalias 'slz' in case it was previously defined as an alias
unalias slz 2>/dev/null
slz() {
    if [ $# -eq 0 ]; then
        echo "Usage: slz <your question whose result should be pasted to the line>"
        return 1
    fi

    # 1. Execute the client and capture the output (the command string)
    # "$*" ensures all arguments are passed as a single string to the CLI client.
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Use 'print -z' to paste the captured command into the current prompt line.
    print -z "$COMMAND"
}
# source ~/.zshrc

# ===================================================================
# == 3. slxXsoidfuasdzof: Immediate Execution (DANGEROUS MODE)
# ===================================================================

# Unalias the long name in case it was previously defined
unalias slxXsoidfuasdzof 2>/dev/null
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Usage: slx <your question whose result will be executed immediately>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Check if any output was received
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        echo "--> Executing command: $COMMAND"
        # DANGER: 'eval' executes the command string immediately
        eval "$COMMAND"
    else
        echo "No command output received from the service."
    fi
}
# source ~/.zshrc

```

---

### 3. Utilisation des trois commandes

| Commande | Fonctionnalité | Niveau de sécurité | Exemple |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Sortie standard :** Exécute le service et imprime l'intégralité de la sortie directement sur la console. | **SÛR** | `sl Qu'est-ce qu'une maison` (Impressions : "Une maison est...") |
| **`slz`** | **Safe Execution Prep :** exécute le service et colle le résultat (par exemple, une commande shell) dans la ligne d'entrée Zsh, prêt à être révisé ou exécuté. | **SÛR/PRÉPARATION** | `slz git` (Colle : `git add . && git commit...` **mais ne l'exécute pas**.) |
| **`slxXsoidfuasdzof`** | **Exécution immédiate :** Exécute le service et exécute immédiatement la sortie en tant que commande shell. Utilisez le nom énigmatique comme mesure de sécurité. | **DANGEREUX** | `slxXsoidfuasdzof git` (Exécute immédiatement la commande `git add...`.) |