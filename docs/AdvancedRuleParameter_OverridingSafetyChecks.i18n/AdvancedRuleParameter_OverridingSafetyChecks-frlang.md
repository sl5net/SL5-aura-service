# Documentation du moteur de règles Aura SL5

## Paramètre de règle avancé : remplacement des contrôles de sécurité

Dans certains scénarios (par exemple, des commandes internes très fiables ou des entrées simples et de haute confiance), les utilisateurs peuvent vouloir forcer l'exécution d'étapes de post-traitement (comme les « fuzzyRules »), même si la confiance du système dans la reconnaissance vocale initiale est faible.

Par défaut, SL5 Aura utilise un garde-corps de sécurité : si les changements d'entrées sont élevés (`LT_SKIP_RATIO_THRESHOLD`), les outils de post-traitement sont ignorés pour éviter des corrections/hallucinations peu fiables et pour des raisons de performances.


Pour désactiver ce contrôle de sécurité pour une règle spécifique, ajoutez l'identifiant au paramètre `skip_list` :

__CODE_BLOCK_0__