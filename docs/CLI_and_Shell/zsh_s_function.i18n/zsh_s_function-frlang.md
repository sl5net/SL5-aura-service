# Fonction Zsh : s() - KI-Client avec délai d'attente adaptatif

Anglais (anglais)
But

Cette ou ces fonctions Zsh agissent comme un wrapper pour le client Python (cli_client.py) et implémentent une gestion robuste des erreurs et une stratégie de délai d'attente adaptative. Il est conçu pour détecter rapidement les erreurs de connexion au service et garantir la capture complète des réponses de l’IA (jusqu’à 70 secondes).
Logique clé

La fonction s'appuie sur deux fonctionnalités du shell pour plus de robustesse :

timeout : empêche le script de se bloquer indéfiniment et permet une détection rapide des erreurs.

mktemp / Fichiers temporaires : contourne les problèmes de mise en mémoire tampon de sortie du shell en lisant la sortie du script à partir d'un fichier après la fin.

Usage
codeBash

  
s <texte de votre question>
# Exemple : s Ordinateur Guten Morgen

  
  
### source
__CODE_BLOCK_0__