# Motivation : Pourquoi « Disk Wins » ?

## Le problème en mode grand-mère Aura

Dans [Aura Oma Mode](../../../GettingStarted.i18n/GettingStarted-frlang.md) (voir ligne 67), Aura fonctionne de manière largement autonome :
l'utilisateur prononce des commandes et Aura écrit seul dans les fichiers -
configurations, scripts, entrées de journal, texte généré.

Le scénario suivant se produit constamment :

1. L'utilisateur dispose d'un fichier ouvert sous l'éditeur (par exemple un fichier de règles ou un script).
2. Ils oublient que l'éditeur est toujours actif et prononcent une commande Aura.
3. Aura modifie le fichier sur le disque.
4. L'éditeur détecte le changement externe — et **demande**.

Cette invite est un **showstopper** en mode Oma :
- L'utilisateur peut être assis sur le canapé, en utilisant la saisie vocale,
et ne peut pas voir ou accéder à la boîte de dialogue.
- Ou bien ils ont accidentellement appuyé sur une touche de l'éditeur, le tampon est maintenant
"modifié", et chaque changement externe se bloque avec un
"Recharger ? / Rester local ?" dialogue.
- Le résultat : Aura continue de fonctionner, mais l'éditeur affiche une version obsolète.
L'utilisateur pense qu'il consulte le fichier actuel, mais le modifie en fonction
sur un vieil État, le chaos est garanti.

## Ce dont nous avons besoin

Comportement de l'éditeur qui **donne toujours la priorité au disque**.
Lorsqu'Aura (ou tout autre outil) modifie le fichier, l'éditeur doit
immédiatement et **sans aucune invite** affiche le nouveau contenu.
Les entrées non enregistrées dans l'éditeur peuvent être ignorées silencieusement - car dans
Mode Oma, Aura est la source de la vérité, pas la saisie humaine au clavier.

## Pourquoi les éditeurs standards échouent

Presque tous les éditeurs courants (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText prêts à l'emploi) disposent d'un mécanisme de protection :
dès que le tampon contient des modifications non enregistrées, ils demandent **toujours**
lorsqu'un changement externe se produit. Il s'agit d'une fonctionnalité normale
travail de développeur – mais un bug pour le mode Aura Oma.

Ce plugin comble exactement cette lacune pour CudaText.

## Public cible

- Les utilisateurs du mode Aura Oma qui visualisent des fichiers dans un éditeur en parallèle.
- Scénarios d'automatisation où un processus écrit des fichiers et un éditeur
sert uniquement de visionneuse en direct.
- Toute personne pour qui "le disque gagne toujours" est le comportement souhaité.