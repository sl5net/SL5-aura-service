# Notes : problème de clé bloquée type_watcher.sh (dotool)

## Symptôme
Peu de temps après un redémarrage de Manjaro, lors de la première dictée après `sl5net Aura`
démarré automatiquement, un seul caractère est resté bloqué et répété à l'infini
(par exemple "n" répété des centaines de fois) jusqu'à ce que la touche de déclenchement soit enfoncée
encore une fois comme solution de contournement manuelle.

Observé une fois le 21/07/2026 ~ 09:44 (mardi), texte : "Die Ideen niemand wird
mehr gefragt, mais es soll trotzdem genauso sein wie...nnnnn...".

## Chronologie (prouvée via des journaux)
- 09:29:17 - `type_watcher.sh` démarré (log/type_watcher.log)
- 09:41:56 - dictée "ideen niemand wird mehr gefragt..." reçue
(log/aura_engine.log, fil de discussion 13/14)
- 09:42:03 - traitement du texte terminé (`meilleur score flou : 0%`),
vraisemblablement écrit dans un fichier `tts_output_*.txt`
- ~09:42:04-09:42:09 - `type_watcher.sh` s'est écrasé (déduit : chien de garde
l'intervalle d'interrogation est de 5 s, voir ci-dessous)
- 09:42:09 - journal de surveillance (log/type_watcher_keep_alive.log) :
"WATCHDOG : 'type_watcher.sh' n'est pas en cours d'exécution. Démarrez-le maintenant."
- 09:42:13 - `type_watcher.sh` redémarré (log/type_watcher.log)
- Aucune entrée `contenu typé de ...` pour le fichier "ideen niemand..." n'a été
jamais trouvé dans log/type_watcher.log - la saisie de ce spécifique
le texte n’a jamais été complété/enregistré.

## Statut de la cause première
- CONFIRMÉ : `type_watcher.sh` plantait entre la fin du texte
traitement (09:42:03) et le chien de garde le détecte comme n'étant pas en cours d'exécution
(09:42:09). Le chien de garde (`type_watcher_keep_alive.sh`) tue uniquement
et redémarre lors d'un changement d'horodatage du fichier de configuration (`ts1`/`ts2`,
confirmé inchangé dans cet incident) ou redémarre automatiquement lorsque
`pgrep -f "type_watcher.sh"` ne trouve aucun processus — c'est-à-dire que c'était très
probablement un auto-crash, pas une tuerie externe.
- HYPOTHÈSE (non prouvée) : `set -euo pipefail` (type_watcher.sh ligne 5)
a provoqué la fermeture du script sur un code de sortie non nul à l'intérieur du
pipeline, peut-être pendant que le tube `dotool` de `do_type()` (ligne 125) était
à mi-chemin. Si le processus bash s'arrête lors de la diffusion dans `dotool`,
le démon `dotoold` séparé (qui continue de fonctionner indépendamment)
peut être laissé avec une clé dans un état « bas » sans jamais correspondre à « up »
reçu, provoquant une répétition de clé au niveau du système d'exploitation.
- PAS ENCORE PROUVÉ : la commande/ligne exacte qui a provoqué le non-zéro
quittez sous `set -euo pipefail`. Pas de stderr du crash
Le processus `type_watcher.sh` a été capturé (le chien de garde l'appelle
sans aucune redirection de sortie, `type_watcher_keep_alive.sh` ligne 79).
- La clé affectée n'était PAS toujours le même caractère dans différents
occurrences de ce bug (rapport utilisateur : auparavant "t" également).

## Déjà enquêté et exclu
- Pas de redémarrage déclenché par un changement de configuration (confirmé par l'utilisateur : config
inchangé, et la vérification `ts1_old != ts1_new` enregistrerait "Config modifiée").
- Pas de démarrage automatique en double de `type_watcher.sh` chevauchant
lui-même (une seule entrée "Bonjour de Watcher" a précédé le crash).
- L'appel `dotool type` de `do_type()` est atomique par invocation et ne
n'envoie pas lui-même une touche par caractère vers le bas/vers le haut - excluant `type_watcher.sh`
logique d'application comme source directe d'une clé bloquée dans des conditions normales
(sans crash).

## Correctif déjà appliqué (repli/atténuation, pas correctif de cause première)
`cleanup()` dans `type_watcher.sh` et `do_cleanup()` dans
`keep-keys-up.sh` précédemment publié uniquement les touches de modification (shift, ctrl,
alt, etc.) via `dotool`/`xdotool`. Cela n'a rien fait pour un habitué coincé
clé (lettre, chiffre, ponctuation).

- `type_watcher.sh` : `cleanup()` envoie désormais `dotool key <name>:up` pour
toutes les lettres, chiffres et touches de ponctuation/espaces communes, pas
juste des modificateurs.
- `type_watcher.sh` : `INPUT_METHOD` est maintenant exporté après détection, donc
d'autres scripts peuvent voir quel backend (`dotool` / `xdotool`) est actif.
- `keep-keys-up.sh` : `do_cleanup()` a gagné une branche `dotool` (en utilisant le
verbe `keyup`, pas de délai par touche, pour les performances) actif uniquement lorsque
`INPUT_METHOD=dotool`, reflétant l'appel `xdotool keyup` existant
pour les modificateurs.

Cela ne résout pas le crash sous-jacent de `type_watcher.sh` ; c'est seulement
garantit que si le crash se reproduit, une clé bloquée est libérée sur
la prochaine passe de nettoyage (`--cleanup`, appelée après chaque `do_type()`, et
via le gestionnaire `trap cleanup EXIT INT TERM`) au lieu de répéter
indéfiniment jusqu'à ce que vous appuyiez manuellement sur la touche de déclenchement.

## Prochaines étapes si cela se reproduit
- Capturez le stderr de `type_watcher.sh` en cas de crash. Actuellement
La ligne 79 de `type_watcher_keep_alive.sh` l'appelle sans redirection, donc
tout message d'erreur bash est perdu (il est envoyé au système de surveillance
stdout/stderr, partout où cela est demandé par le mécanisme de démarrage automatique).
- Considérez un mode débogage, par ex. `bash -x scripts/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`, basculé via une variable d'environnement telle que
`TYPE_WATCHER_DEBUG=1`, pour capturer la ligne défaillante exacte sur le prochain
accident.
- Vérifiez ce qui démarre `type_watcher_keep_alive.sh` au démarrage de Manjaro
(fichier de démarrage automatique `.desktop`, unité systemd `--user`, etc.) et si
ses stdout/stderr sont capturés n'importe où.
- Si reproductible, testez si l'accident est en corrélation avec
`dotoold` s'initialise toujours juste après le démarrage (voir le `sleep 0.1`
à type_watcher.sh ligne 8 et la boucle de démarrage `dotooled` aux lignes
102-110).